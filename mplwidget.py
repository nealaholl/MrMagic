"""
A widget for PyQt4 that displays images using Matplotlib

:class:`mplwidget.startColorMapUi`
    Brings up a dialog to select the plots colormap.

:py:class:`mplwidget.mplCanvas`
    A Qt4 widget used to embed a matplotlib plot in a GUI. Specifically
    designed for use with image data.
    
"""
from PyQt4 import QtGui, QtCore
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.patches as pch
import matplotlib.pyplot as plt

from contrast import Ui_ContrastSettings
from ColorMap import Ui_CMapDialog


class startColorMapUi(QtGui.QDialog, Ui_CMapDialog):
    """
    Class for the color map selector UI. It displays a combo box of all
    available maps, shows the current map as a color bar, and has accept/reject
    buttons.
    
    .. warning:: This is not intended to be used outside of the mplCanvas
    """
    returnData = QtCore.pyqtSignal(str)
    def __init__(self, CMap='gray', parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.CMap = CMap
        # Obtain a list of the available colormaps
        self.maps = [m for m in plt.cm.datad if not m.endswith("_r")]
        self.maps.sort()  # organize them in alphabetical order
        #populate the combo boxes
        self.ComboBox.addItems(self.maps)
        self.ComboBox.setCurrentIndex(self.ComboBox.findText(CMap))
        #initial draw of the color bar
        self.drawBar()

        #connect the UI elements to their functions
        self.ComboBox.activated.connect(self._drawBar)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.accepted.connect(self._dataCarrier)

    @QtCore.pyqtSlot()
    def _drawBar(self):
        """ QT slot that draws a bar showing the current colormap. """
        colors = np.outer(np.arange(0, 1, 0.01), np.ones(20)).T
        index = self.ComboBox.currentIndex()
        self.CMap = self.maps[index]
        self.colorbar.ax.clear()
        self.colorbar.ax.set_axis_off()
        self.colorbar.ax.imshow(colors, cmap=self.maps[index], aspect='auto')
        self.colorbar.ax.set_position([0, 0, 1, 1])
        self.colorbar.draw()

    @QtCore.pyqtSlot()
    def _dataCarrier(self):
        """ QT slot that sends a QT signal with the selected colormap. """
        self.returnData.emit(self.CMap)


class _startContrastUI(QtGui.QDialog, Ui_ContrastSettings):
    """ 
    Popup window for adjusting contrast
    
    .. warning:: This is not intended to be used outside of hte mplConavas
    
    """
    def __init__(self, Parent=None):
        QtGui.QDialog.__init__(self, Parent)
        self.setupUi(self)

        self.autoRange.stateChanged.connect(self._autoRangeSlot)

    @QtCore.pyqtSlot(int)
    def _autoRangeSlot(self, State):
        """ Handles enabling and disabling the spinboxes for autoranging"""
        if State == 2:
            self.minSB.setEnabled(False)
            self.maxSB.setEnabled(False)
        if State == 0:
            self.minSB.setEnabled(True)
            self.maxSB.setEnabled(True)


class mplCanvas(FigureCanvasQTAgg):
    """
    Base class for displaying the images. Conatins most of the information
    needed to show the image and mark it up.

    """
    # Signal to emit when clearing marks. Has to be here, not sure why?
    clearMarks = QtCore.pyqtSignal()
    setMark = QtCore.pyqtSignal(mpl.backend_bases.MouseEvent, tuple, tuple)
    toggleMask = QtCore.pyqtSignal()

    def __init__(self, Maskable=False):
        QtCore.QObject.__init__(self)
        # Member elements for storing image formatting parameters
        self.circles = []
        self.cadj = lambda x: x
        self.filterstack = []
        self.CMap = 'gray'
        self.data = []
        self.im = None
        self.cbar = None
        self.aspectRatio = None
        self.minMax = None
        self.mask = None
        self.maskable = Maskable
        # Setup the canvas and axes
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.ax.set_axis_off()

        # Need to understand what this actually does....
        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

        self.fig.canvas.mpl_connect('button_press_event', self._plotClick)

    def addMarker(self, Coord):
        """ Draws a small circle at the supplied data coordinates """
        for circ in self.circles:
            circ.remove()
            self.circles.pop()

        self.circles.append(pch.Circle(Coord,
                                       radius=1,
                                       lw=0.25,
                                       ec='yellow',
                                       fc='none'))

        self.ax.add_patch(self.circles[-1])
        self.draw()

    def clearMarkers(self):
        """ Removes the markers from the canvas and from the class """
        for circ in self.circles:
            circ.remove()
            self.circles.pop()
        self.draw()     

    def _cMapPicker(self):
        """ Start the UI to select a colormap for the display. """
        self.subwindow = startColorMapUi(self.CMap)
        self.subwindow.returnData.connect(self.setCMap)
        if self.subwindow.exec_():  # on exit, set the new color maps
            return

    @QtCore.pyqtSlot()
    def _contrastSlot(self):
        """ Control function for changing the contrast."""
        if self.subwindow.radioGamma.isChecked():
            # Lambda function that corrisponds to a gamma transform
            self.cadj = lambda x:\
                x**(self.subwindow.gammaSldr.value()/10.0)
        elif self.subwindow.radioLog.isChecked():
            # Lambda function for a log transform
            self.cadj = lambda x: np.log10(1.0+x)
        else:
            # Lambda function for no contrast adjustment
            self.cadj = lambda x: x
        self.imshow()
        
    def contextMenuEvent(self, Event):
        """ Construct a context menu for adjusting the widget. """
        menu = QtGui.QMenu(self)
        # Setup the menu
        clearMarkersAction = menu.addAction("Clear Markers")
        setCMapAction = menu.addAction("Set CMap")
        setContrastAction = menu.addAction("Set Contrast")
        saveImageAction = menu.addAction("Save Image")
        toggleCBarAction = menu.addAction("Colorbar")
        toggleCBarAction.setCheckable(True)
        if self.cbar is not None:
            toggleCBarAction.setChecked(True)
        if self.maskable is True:
            maskAction = menu.addAction("Mask")
            maskAction.setCheckable(True)
            if self.mask is not None:
                maskAction.setChecked(True)
        # Switch on the action clicked
        action = menu.exec_(self.mapToGlobal(Event.pos()))
        if action == clearMarkersAction:
            self.clearMarks.emit()
        elif action == setCMapAction:
            self._cMapPicker()
        elif action == setContrastAction:
            self.setContrast()
        elif action == saveImageAction:
            self.saveImage()
        elif action == toggleCBarAction:
            self.toggleCBar()
        elif self.maskable is True and action == maskAction:
            self.toggleMask.emit()

    def imshow(self, Data=None, CMap=None, Aspect=None, Mask=None,
               MinMax=None):
        """
        Shows the data supplied, maintining the aspect ratio.
        
        **Args:**
            - Data (array): the image to be shown
            - CMap (str): name of the mpl colormap to be used
            - Aspect (float): aspect ratio of the image
            - Mask (array): binary array used to mask the image
            - MinMax (tuple): minimum and maximum values for windowing the 
                image
        
        **Argument Behaviours**
        Arguments that are not supplied default to None.
        
        *Data:* If a Data matrix is not supplied, then the last shown image
        (stored in self.data) will be used. If self.data == None, and new Data
        has not been supplied, then the function will return. If new Data is
        supplied, then it is stored in self.data.
        
        *CMap:* If a colormap name is not supplied, then the currently stored
        colormap is used. If a colormap is supplied, then it is stored in the
        class member CMap.
        
        *Aspect:* If no aspect ratio is supplied and no previous value was
        stored, then the ratio is guess from the resolution. If a previous
        value was set, then it is used. If a value is supplied, then is stored
        in the class member aspectRatio. 
        
        *Mask:* If a binary mask is not supplied, then the previous mask is
        used. If it is supplied, then the mask is stored in the class member
        mask.
        
        *MinMax:* If a tuple of two elements is not supplied, then the class
        member minMax is used to set the display range. If no min or max has 
        been supplied the the plot will autorange. If a tuple is given the it
        will be stored in the class member minMax.

        .. seealso:: :meth:`refresh` to quickly refresh the image display
        """
        configs = {}

        if Data is not None:
            self.data = Data.T
        elif self.data is None:
            return

        if CMap is not None:
            self.CMap = CMap

        mask = 1
        if Mask is not None:
            self.mask = Mask
            mask = Mask
        elif Mask is None and self.mask is not None:
            mask = self.mask

        # Set the aspect ratio, default to a square
        if Aspect is None and self.aspectRatio is None:
            configs['aspect'] = (min(np.shape(self.data)) /
                                 max(np.shape(self.data)))
        elif Aspect is None:
            configs['aspect'] = self.aspectRatio
        else:
            self.aspectRatio = Aspect
            configs['aspect'] = Aspect

        # Set the min/max cutoffs, default to auto ranging
        if MinMax is not None:
            self.minMax = MinMax
            configs['vmin'] = MinMax[0]
            configs['vmax'] = MinMax[1]
        elif self.minMax is not None:
            configs['vmin'] = self.minMax[0]
            configs['vmax'] = self.minMax[1]
        # Clean up anything that was already displayed, and go again
        self.ax.clear()
        self.ax.set_axis_off()
        self.im = self.ax.imshow(X=self.cadj(self.data*mask),
                                 cmap=self.CMap,
                                 **configs)
        self.ax.set_position([0, 0, 1, 1])
        self.refresh()

    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(int)
    def _minMaxSlot(self, State=2):
        """ 
        QT slot to set the display limits for the image.
        
        **Args:**
            State(int): Indicates if the min/max values should be updated
            or removed. The call signature of the slot is overloaded so 
            that the connected signal may include either the integer (a 
            value of 2 clears minMax, 0 updates with the spinbox values) or 
            no data, in which case minMax is cleared.

        .. seealso::
            :meth:`setMinMax` which does that actual work of setting 
            the minMax value.
            
            :meth:`removeMinMax` which is used to clear the value
            
        .. todo:: Change this to send the values via the signal.
        
        """
        if State == 0:
            self.setMinMax(self.subwindow.minSB.value(),
                           self.subwindow.maxSB.value())
        elif State == 2:
            self.removeMinMax()

    def refresh(self):
        """      
        Redraws any markers that are in the list.
        
        """
        for circ in self.ax.findobj(match=pch.Circle):
            circ.remove()
        for circ in self.circles:
            self.ax.add_patch(circ)
        self.draw()

    def removeMask(self):
        """ Convenience function to unmask the image. """
        self.mask = None
        self.imshow()
        
    def removeMinMax(self):
        """ Convenience function to set the image to autorange. """
        self.minMax = None
        self.imshow()
 
    def setCMap(self, CMap='gray'):
        """ Set the colormap for the image"""
        self.CMap = CMap
        if self.im is not None:
            self.im.set_cmap(CMap)
        self.refresh()
        
    def setContrast(self):
        """ Change the contrast function for the plot. """
        self.subwindow = _startContrastUI()

        self.subwindow.minSB.setValue(self.im.get_clim()[0])
        self.subwindow.maxSB.setValue(self.im.get_clim()[1])

        self.subwindow.radioGamma.toggled.connect(self._contrastSlot)
        self.subwindow.radioLog.toggled.connect(self._contrastSlot)
        self.subwindow.radioConstant.toggled.connect(self._contrastSlot)
        self.subwindow.gammaSldr.valueChanged.connect(self._contrastSlot)
        self.subwindow.minSB.valueChanged.connect(self._minMaxSlot)
        self.subwindow.maxSB.valueChanged.connect(self._minMaxSlot)
        self.subwindow.autoRange.stateChanged.connect(self._minMaxSlot)
        if self.subwindow.exec_():
            return
            
    def setMinMax(self, Min, Max):
        """ Set the display limits for the image"""
        self.minMax = (Min, Max)
        self.im.set_clim(Min, Max)
        self.draw()

    def _plotClick(self, Event):
        """ Matplotlib click handling to place markers on plots
        
        .. todo:: This is fairly restrictive, probably need to generalize to
            make it possible to SNR boxes, more marks, distance measures, etc.
        
        """
        if Event.button != 1:
            return
        # TODO: Figure out if this means I've reversed indexing somewhere.
        dataCoord = (Event.ydata, Event.xdata)
        plotCoord = (Event.xdata, Event.ydata)

        self.setMark.emit(Event, dataCoord, plotCoord)
        self.addMarker(plotCoord)

    def setMask(self, Mask):
        """ Create and apply a mask for the image"""
        self.mask = Mask
        self.imshow()

    def saveImage(self):
        """ Save the image being shown to a file.
        
        .. todo:: Fix the file type list, it's not what I really want.
        
        """
        self.subwindow = QtGui.QFileDialog()
        svf = self.subwindow.getSaveFileName(self, "Save Image", "C:/",
                                             "Images (*.png *.jpg)")
        self.fig.savefig(svf, bbox_inches='tight', pad_inches=0)
        
    def toggleCBar(self):
        """ Turn on and off the color bar for the plot. """
        if self.im and self.cbar is None:
            self.cbar = self.fig.colorbar(self.im)
            self.refresh()
        elif self.im:
            #ugly hack to rebuild the plot correctly
            self.fig.clear()
            self.cbar = None
            self.ax = self.fig.add_subplot(111, aspect='equal')
            self.ax.set_axis_off()
            self.imshow()
