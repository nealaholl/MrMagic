"""
General purpose MRI image display.

**Classes:**

    * MainWindow: Core GUI element for MR Magic.

**Dependencies:**

    **Standard modules:**
    
    * numpy: Primary math and processing
    * nmrglue: Varian FID importer, needs to be the modified version
    * PyQt4: The GUI is built on this
    
    **Custom modules, general purpose:**
    
    * filters:  Builds the various filters and masks used to process images
    
    **GUI element modules:**
    
    * main_window: Machine generated class for the main windos
    * startCMPUI: GUI for setting the colormaps of the images
    * filter_config_class: GUI to create and manage the filter stack
    
.. moduleauthor:: Neal Hollingsworth

Main MR Magic todo List
_______________________ 
.. todo:: Add procpar explorer

.. todo:: Add GE pFile importer

.. todo:: Add SNR comutation

.. todo:: Add configuration window

.. todo:: Add save configuration

"""



import sys
import os
import platform

import numpy as np
import nmrglue as ng
from PyQt4 import QtGui, QtCore

import filters as filt
from main_window import Ui_MainWindow
import startCMPUI
from filter_config_class import FilterConfig


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    The primary GUI element

    """
    dic = []  # sequence descriptor
    data = []  # raw data
    datafilt = []  # filtered data
    image = []  # filtered reconstructed image
    aspectRatio = 1  # aspect ratio of the image
    subwindow = None  # dummy for any popup menus
    filterStack = []  # stack of filters

    # color maps for the different images
    CMaps = {'kspace': 'gray',
             'kphase': 'gist_rainbow',
             'mag': 'gray',
             'phase': 'gist_rainbow'}

    def __init__(self, Parent=None):
        """
        Setup the main window GUI
        """
        QtGui.QMainWindow.__init__(self, Parent)
        self.setupUi(self)

        # connect the open and colormap menu items
        self.actionFID.triggered.connect(self._openFID)
        self.actionColor_Maps.triggered.connect(self._setCMaps)
        self.actionConfigureFilters.triggered.connect(self._filtConfigure)
        self.actionKspace.triggered.connect(self.kspace.setContrast)
        self.actionKspace_Phase.triggered.connect(self.kspacePhase.setContrast)
        self.actionMagnitude.triggered.connect(self.magnitudeImage.setContrast)
        self.actionPhase_Map.triggered.connect(self.phaseImage.setContrast)
        self.actionExit.triggered.connect(self.exitProg)
        # Connect the show/hide control for the sub-windows
        self.actionData_Explorer.triggered.connect(self.dataExplorerToggle)
        self.actionMagnitude_Image.triggered.connect(self.magnitudeImageToggle)
        self.actionPhase_Image.triggered.connect(self.phaseImageToggle)
        self.actionK_space.triggered.connect(self.kspaceToggle)
        self.actionK_space_Phase.triggered.connect(self.kphaseToggle)
        # Connect control for marking the plots
        self.clearIButton.clicked.connect(self.clearImageMarkers)
        self.clearKButton.clicked.connect(self.clearKspaceMarkers)
        self.magnitudeImage.clearMarks.connect(self.clearImageMarkers)
        self.phaseImage.clearMarks.connect(self.clearImageMarkers)
        self.kspace.clearMarks.connect(self.clearKspaceMarkers)
        self.kspacePhase.clearMarks.connect(self.clearKspaceMarkers)

        # Connect the click signals from the plots
        self.magnitudeImage.setMark.connect(self._plotClick)
        self.phaseImage.setMark.connect(self._plotClick)
        self.kspace.setMark.connect(self._plotClick)
        self.kspacePhase.setMark.connect(self._plotClick)

        # Default to not showing a few subwindows
        self.dataExplorerDock.hide()
        self.kspacePhaseDock.hide()
        self.phaseDock.hide()

        self.phaseImage.maskable = True
        self.phaseImage.toggleMask.connect(self.maskPhase)
        self.magnitudeImage.maskable = True
        self.magnitudeImage.toggleMask.connect(self.maskImage)

    @QtCore.pyqtSlot()
    def _openFID(self):
        """ QT slot that launches the files selector to open a Varian FID file
        
        Selecting the top level \*.fid folder will open it correctly, loading
        both the image data and the procpar file.
        
        """
        # launch the folder selection dialog
        if platform.system() == 'Windows':
            home = os.environ['USERPROFILE']
        elif platform.system() == 'Linux':
            home = os.environ['HOME']

        FID = QtGui.QFileDialog.getExistingDirectory(caption="Open FID",
                                                     directory=home,
                                        options=QtGui.QFileDialog.ShowDirsOnly)
        # Open the FID file
        if FID:
            self.dic, self.data = ng.varian.read(str(FID))
            temp = (float(self.dic['procpar']['lpe']['values'][0]) /
                    float(self.dic['procpar']['lro']['values'][0]))
            self.aspectRatio = temp*(2*float(
                               self.dic['procpar']['nv']['values'][0]) /
                               float(self.dic['procpar']['np']['values'][0]))

            # Add a DC offset corection filter
            self.filterStack.insert(0, filt.makeDCO(Size=10))
            # apply any default filters and recon
            self.updateAll()

    @QtCore.pyqtSlot()
    def _filtConfigure(self):
        """ QT slot that opens the Filter configuration window """
        self.subwindow = FilterConfig(Dim=np.shape(self.data),
                                      FilterStack=self.filterStack)
        if self.subwindow.exec_():
            self.filterStack = self.subwindow.filterStack
            self.updateAll()

    @QtCore.pyqtSlot()
    def _setCMaps(self):
        """ QT slot that opens the Color Map Configuration window"""
        self.subwindow = startCMPUI.startCMPUI(self.CMaps)
        if self.subwindow.exec_():  # on exit, set the new color maps
            self.CMaps = self.subwindow.CMaps
            self.updateAll()

    def updateAll(self):
        """
        Refreshes all of the displays with the current data and color maps
        as well as applying the filter stack.

        """
        if self.data == []:
            return

        # apply all of the filters
        self.datafilt = filt.applyStack(self.data, self.filterStack)

        self.image = np.fft.ifftshift(np.fft.ifft2(
            np.fft.ifftshift(self.datafilt)))
        # Display the kspace data
        self.kspace.imshow(np.abs(self.datafilt), self.CMaps['kspace'],
                           self.aspectRatio)
        # display the phase data
        self.kspacePhase.imshow(np.angle(self.datafilt), self.CMaps['kphase'],
                                self.aspectRatio)
        # display the Image
        self.magnitudeImage.imshow(np.abs(self.image), self.CMaps['mag'],
                                   self.aspectRatio)
        # display the phase map
        self.phaseImage.imshow(np.angle(self.image), self.CMaps['phase'],
                               self.aspectRatio)

    @QtCore.pyqtSlot(int)
    def dataExplorerToggle(self):
        """ QT slot that toggles the data explorer display"""
        if self.dataExplorerDock.isVisible():
            self.dataExplorerDock.hide()
        else:
            self.dataExplorerDock.show()

    @QtCore.pyqtSlot()
    def magnitudeImageToggle(self):
        """ QT slot that toggles the image display"""
        if self.magnitudeDock.isVisible():
            self.magnitudeDock.hide()
        else:
            self.magnitudeDock.show()

    @QtCore.pyqtSlot()
    def phaseImageToggle(self):
        """ QT slot that toggles the phase display"""
        if self.phaseDock.isVisible():
            self.phaseDock.hide()
        else:
            self.phaseDock.show()

    @QtCore.pyqtSlot()
    def kspaceToggle(self):
        """ QT slot that toggles the k-space display"""
        if self.kspaceDock.isVisible():
            self.kspaceDock.hide()
        else:
            self.kspaceDock.show()

    @QtCore.pyqtSlot()
    def kphaseToggle(self):
        """ QT slot that toggles the k-space phase display"""
        if self.kspacePhaseDock.isVisible():
            self.kspacePhaseDock.hide()
        else:
            self.kspacePhaseDock.show()

    @QtCore.pyqtSlot(int)
    def _plotClick(self, Event, DataPoint, PlotPoint):
        """ QT slot that handles clicks to place markers on paired plots"""
        if (Event.canvas == self.magnitudeImage):
            self.iMag.setText(str(np.abs(self.image[DataPoint])))
            self.iPhase.setText(str(np.angle(self.image[DataPoint])))
            self.phaseImage.addMarker(PlotPoint)

        elif (Event.canvas == self.phaseImage):
            self.iMag.setText(str(np.abs(self.image[DataPoint])))
            self.iPhase.setText(str(np.angle(self.image[DataPoint])))
            self.magnitudeImage.addMarker(PlotPoint)

        elif (Event.canvas == self.kspace):
            self.kMag.setText(str(np.abs(self.datafilt[DataPoint])))
            self.kPhase.setText(str(np.angle(self.datafilt[DataPoint])))
            self.kspacePhase.addMarker(PlotPoint)

        elif (Event.canvas == self.kspacePhase):
            self.kMag.setText(str(np.abs(self.datafilt[DataPoint])))
            self.kPhase.setText(str(np.angle(self.datafilt[DataPoint])))
            self.kspace.addMarker(PlotPoint)

    @QtCore.pyqtSlot(int)
    def clearImageMarkers(self):
        """ QT slot that clears all markers from the image space plots """
        self.magnitudeImage.clearMarkers()
        self.phaseImage.clearMarkers()

        self.iMag.setText(' ')
        self.iPhase.setText(' ')

    @QtCore.pyqtSlot(int)
    def clearKspaceMarkers(self):
        """ QT slot that clears all markers from the k-space plots """
        self.kspace.clearMarkers()
        self.kspacePhase.clearMarkers()

        self.kMag.setText(' ')
        self.kPhase.setText(' ')

    @QtCore.pyqtSlot()
    def maskPhase(self):
        """ QT slot that toggles the mask for the phase map """
        if self.phaseImage.mask is None:
            self.phaseImage.setMask(Mask=filt.mask(self.image))
        else:
            self.phaseImage.setMask(None)

    @QtCore.pyqtSlot()
    def maskImage(self):
        """ QT slot that toggles the mask for the image """
        if self.magnitudeImage.mask is None:
            self.magnitudeImage.setMask(Mask=filt.mask(self.image))
        else:
            self.magnitudeImage.removeMask()

    @QtCore.pyqtSlot(int)
    def exitProg(self):
        """ QT slot that exits the program"""
        self.close()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
    