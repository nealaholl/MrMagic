"""
Configuration window for the various filters.
"""

import numpy as np
from PyQt4 import QtGui

import filters as filt

from filter_config import Ui_filterConfig


class FilterConfig(QtGui.QDialog, Ui_filterConfig):
    """
    Starts a sub-window used to configure the filter stack.

    """
    diameter = 32
    width = 5
    shape = 3
    flistitems = []
    FILTER_NAMES = {'Barthann': 'barthann',
                    'Bartlett': 'bartlett',
                    'Blackman': 'blackman',
                    'Blackman-Harris': 'blackmanharris',
                    'Bohman': 'bohman',
                    'Boxcar': 'boxcar',
                    'Dolph-Chebyshev': 'chebwin',
                    'DC Offset': 'DC Offset',
                    'Flat Top': 'flattop',
                    'Gaussian': 'gaussian',
                    'Hamming': 'hamming',
                    'Hanning': 'hanning',
                    'Kaiser': 'kaiser',
                    'Nuttall': 'nuttall',
                    'Parzen': 'parzen',
                    'Slepian': 'slepian',
                    'Triangle': 'triang'}

    def __init__(self, Dim=(128, 128), FilterStack=[], Parent=None):
        QtGui.QDialog.__init__(self, Parent)
        self.setupUi(self)

        #Build reverse filter dictionary
        self.REV_FILTER_NAMES = {v: k for k, v in self.FILTER_NAMES.items()}
        self.dim = Dim
        self.filterStack = FilterStack
        #Add filters to the combobox
        self.windowCB.addItems(sorted(self.FILTER_NAMES.keys()))
        self.diameterSB.setValue(np.max(Dim))

        #Connect widgets to their callbacks functions
        self.windowCB.currentIndexChanged.connect(self._updateWindow)
        self.newButton.clicked.connect(self._newFilter)
        self.removeButton.clicked.connect(self._removeFilter)

        self.lowpassRB.toggled.connect(self._enableSP)
        self.highpassRB.toggled.connect(self._enableSP)
        self.cbandstopRB.toggled.connect(self._enableBS)
        self.vbandstopRB.toggled.connect(self._enableVBS)
        self.hbandstopRB.toggled.connect(self._enableHBS)
        self.notchRB.toggled.connect(self._enableNotch)

        self.outerRB.toggled.connect(self._rbToggle)
        self.rotationalRB.toggled.connect(self._rbToggle)
        self.pixelRB.toggled.connect(self._rbToggle)
        self.percentRB.toggled.connect(self._rbToggle)

        self.diameterSB.valueChanged.connect(self._updateFilter)
        self.widthSB.valueChanged.connect(self._updateFilter)
        self.shapeSB.valueChanged.connect(self._updateFilter)
        self.hcenterSB.valueChanged.connect(self._updateFilter)
        self.vcenterSB.valueChanged.connect(self._updateFilter)

        self.filterList.itemClicked.connect(self._changeFilter)
        self._updateList()
        if self.filterList.count() > 0:
            self.filterList.setCurrentRow(self.filterList.count()-1)
        self._changeFilter()

    def _updateFilter(self):
        """Update the filter in the stack and redisplay"""
        if self.filterStack == []:
            return
        window = self.FILTER_NAMES[str(self.windowCB.currentText())]
        if (window == 'chebwin') or (window == 'gaussian') or \
                (window == 'kaiser') or (window == 'slepian'):
            window = (window, self.shapeSB.value())

        if window == 'DC Offset':
            workingFilter = filt.makeDCO()

        elif self.lowpassRB.isChecked():
            workingFilter = \
                filt.makeLPF(Window=window,
                             Dim=self.dim,
                             Diameter=self.diameterSB.value(),
                             Outer=self.outerRB.isChecked(),
                             Cont=self.percentRB.isChecked())
        elif self.highpassRB.isChecked():
            workingFilter = \
                filt.makeHPF(Window=window,
                             Dim=self.dim,
                             Diameter=self.diameterSB.value(),
                             Outer=self.outerRB.isChecked(),
                             Cont=self.percentRB.isChecked())

        elif self.cbandstopRB.isChecked():
            workingFilter = \
                filt.makeBSF(Window=window,
                             Dim=self.dim,
                             Radius=self.diameterSB.value(),
                             Diameter=self.widthSB.value(),
                             Cont=self.percentRB.isChecked())

        elif self.vbandstopRB.isChecked():
            workingFilter = \
                filt.makeVBSF(Window=window,
                              Dim=self.dim,
                              Center=self.hcenterSB.value(),
                              Width=self.widthSB.value())

        elif self.hbandstopRB.isChecked():
            workingFilter = \
                filt.makeHBSF(Window=window,
                              Dim=self.dim,
                              Center=self.vcenterSB.value(),
                              Width=self.widthSB.value())

        elif self.notchRB.isChecked():
            center = (self.vcenterSB.value(), self.hcenterSB.value())
            workingFilter = filt.makeNF(Window=window,
                                        Dim=self.dim,
                                        Center=center,
                                        Width=self.widthSB.value())

        self.filterDisplay.imshow(workingFilter.function(np.ones(self.dim)))
        index = self.filterList.currentRow()
        self.filterStack[index] = workingFilter
        self._updateList()
        self.filterList.setCurrentRow(index)

    def _newFilter(self):
        '''Add a new filter to the stack'''
        self.filterStack.append(filt.makeLPF(Window='hanning',
                                             Dim=self.dim,
                                             Radius=max(self.dim),
                                             Outer=False,
                                             Cont=False))
        self._enableSP(True)
        self.filterList.setCurrentRow(self.filterList.count()-1)
        self._updateList()

    def _removeFilter(self):
        """Remove filter from the stack"""
        if self.filterList.currentRow() is not True:
            return
        self.filterStack.pop(self.filterList.currentRow())
        self._updateList()

    def _updateList(self):
        """Update the diplay list with filters in the stack"""
        if self.filterStack == []:
            return
        self.filterList.clear()
        for tempFilt in self.filterStack:
            self.filterList.addItem(tempFilt.params['Type'])

    def _rbToggle(self, Active):
        """Callback for toggle even for the radio buttons"""
        if Active:
            self._updateFilter()

    def _enableSP(self, Active):
        """
        Sets the widgets active needed to configure low and high pass filters.

        """
        if Active:
            self.windowCB.setEnabled(True)

            self.lowpassRB.setEnabled(True)
            self.highpassRB.setEnabled(True)
            self.cbandstopRB.setEnabled(True)
            self.vbandstopRB.setEnabled(True)
            self.hbandstopRB.setEnabled(True)
            self.notchRB.setEnabled(True)

            self.diameterSB.setEnabled(True)
            self.widthSB.setEnabled(False)
            self.hcenterSB.setEnabled(False)
            self.vcenterSB.setEnabled(False)

            self.outerRB.setEnabled(True)
            self.rotationalRB.setEnabled(True)

            self.pixelRB.setEnabled(True)
            self.percentRB.setEnabled(True)
            self._updateFilter()

    def _enableBS(self, Active):
        """
        Activates the widgets needed to configure circular band stop filters.

        """
        if Active:
            self.windowCB.setEnabled(True)

            self.lowpassRB.setEnabled(True)
            self.highpassRB.setEnabled(True)
            self.cbandstopRB.setEnabled(True)
            self.vbandstopRB.setEnabled(True)
            self.hbandstopRB.setEnabled(True)
            self.notchRB.setEnabled(True)

            self.diameterSB.setEnabled(True)
            self.widthSB.setEnabled(True)
            self.hcenterSB.setEnabled(False)
            self.vcenterSB.setEnabled(False)

            self.outerRB.setEnabled(False)
            self.rotationalRB.setEnabled(False)

            self.pixelRB.setEnabled(True)
            self.percentRB.setEnabled(True)
            self._updateFilter()

    def _enableVBS(self, Active):
        """
        Activates the widgets needed to configure vertical band stop filters.

        """
        if Active:
            self.windowCB.setEnabled(True)

            self.lowpassRB.setEnabled(True)
            self.highpassRB.setEnabled(True)
            self.cbandstopRB.setEnabled(True)
            self.vbandstopRB.setEnabled(True)
            self.hbandstopRB.setEnabled(True)
            self.notchRB.setEnabled(True)

            self.diameterSB.setEnabled(False)
            self.widthSB.setEnabled(True)
            self.hcenterSB.setEnabled(True)
            self.vcenterSB.setEnabled(False)

            self.outerRB.setEnabled(False)
            self.rotationalRB.setEnabled(False)

            self.pixelRB.setEnabled(False)
            self.percentRB.setEnabled(False)
            self._updateFilter()

    def _enableHBS(self, Active):
        """
        Activates the widgets needed to configure horizontal band stop filters.

        """
        if Active:
            self.windowCB.setEnabled(True)

            self.lowpassRB.setEnabled(True)
            self.highpassRB.setEnabled(True)
            self.cbandstopRB.setEnabled(True)
            self.vbandstopRB.setEnabled(True)
            self.hbandstopRB.setEnabled(True)
            self.notchRB.setEnabled(True)

            self.diameterSB.setEnabled(False)
            self.widthSB.setEnabled(True)
            self.hcenterSB.setEnabled(False)
            self.vcenterSB.setEnabled(True)

            self.outerRB.setEnabled(False)
            self.rotationalRB.setEnabled(False)

            self.pixelRB.setEnabled(False)
            self.percentRB.setEnabled(False)
            self._updateFilter()

    def _enableNotch(self, Active):
        """ Activates the widgets needed to notch filters """
        if Active:
            self.windowCB.setEnabled(True)

            self.lowpassRB.setEnabled(True)
            self.highpassRB.setEnabled(True)
            self.cbandstopRB.setEnabled(True)
            self.vbandstopRB.setEnabled(True)
            self.hbandstopRB.setEnabled(True)
            self.notchRB.setEnabled(True)

            self.diameterSB.setEnabled(False)
            self.widthSB.setEnabled(True)
            self.hcenterSB.setEnabled(True)
            self.vcenterSB.setEnabled(True)

            self.outerRB.setEnabled(False)
            self.rotationalRB.setEnabled(False)

            self.pixelRB.setEnabled(False)
            self.percentRB.setEnabled(False)
            self._updateFilter()

    def _disableAll(self):
        """ Turn off all filter config widgets """
        self.windowCB.setEnabled(True)

        self.lowpassRB.setEnabled(False)
        self.highpassRB.setEnabled(False)
        self.cbandstopRB.setEnabled(False)
        self.vbandstopRB.setEnabled(False)
        self.hbandstopRB.setEnabled(False)
        self.notchRB.setEnabled(False)

        self.diameterSB.setEnabled(False)
        self.widthSB.setEnabled(False)
        self.shapeSB.setEnabled(False)
        self.hcenterSB.setEnabled(False)
        self.vcenterSB.setEnabled(False)

        self.outerRB.setEnabled(False)
        self.rotationalRB.setEnabled(False)

        self.pixelRB.setEnabled(False)
        self.percentRB.setEnabled(False)

    def _updateWindow(self):
        """ Updates widgets when the filter window is changed """
        window = str(self.sender().currentText())
        if (window == 'Dolph-Chebyshev') or (window == 'Gaussian') or\
                (window == 'Kaiser') or (window == 'Slepian'):
            self.shapeSB.setEnabled(True)
        elif window == 'DC Offset':
            self._disableAll()
            self.filterDisplay.imshow(np.zeros(self.dim))
        else:
            self.shapeSB.setEnabled(False)

        self._updateFilter()

    def _changeFilter(self):
        """ Callback to handle a change in the selected filter"""
        if self.filterStack == []:
            return
        index = self.filterList.currentRow()
        self._loadFilter(self.filterStack[index])

    def _setOuter(self, Filt):
        """ Convenience function to check/set the filter construction method"""
        if Filt.params['Outer']:
            self.outerRB.setChecked(True)
        else:
            self.rotationalRB.setChecked(True)

    def _setContour(self, Filt):
        """ Convenience function to check/set the filter contour type"""
        if Filt.params['Contour']:
            self.percentRB.setChecked(True)
        else:
            self.pixelRB.setChecked(True)

    def _loadFilter(self, Filt):
        """ Update the display with and existing filter's settings """
        window = self.REV_FILTER_NAMES[Filt.params['Name']]
        self.windowCB.setCurrentIndex(self.windowCB.findText(window))
        if (window == 'Dolph-Chebyshev') or (window == 'Gaussian') or \
                (window == 'Kaiser') or (window == 'Slepian'):
            self.shapeSB.setValue(Filt.params['Shape'])

        if Filt.params['Type'] == 'Low Pass':
            self._enableSP(True)
            self.lowpassRB.setChecked(True)
            self.diameterSB.setValue(Filt.params['Radius'])
            self._setOuter(Filt)
            self._setContour(Filt)

        elif Filt.params['Type'] == 'High Pass':
            self._enableSP(True)
            self.highpassRB.setChecked(True)
            self.diameterSB.setValue(Filt.params['Radius'])
            self._setOuter(Filt)
            self._setContour(Filt)

        elif Filt.params['Type'] == 'Band Stop':
            self._enableBS(True)
            self.cbandstopRB.setChecked(True)
            self.diameterSB.setValue(Filt.params['Radius'])
            self.widthSB.setValue(Filt.params['Width'])
            self._setContour(Filt)

        elif Filt.params['Type'] == 'Vertical Band Stop':
            self._enableVBS(True)
            self.vbandstopRB.setChecked(True)
            self.diameterSB.setValue(Filt.params['Width'])
            self.hcenterSB.setValue(Filt.params['Center'])

        elif Filt.params['Type'] == 'Horizontal Band Stop':
            self._enableHBS(True)
            self.hbandstopRB.setChecked(True)
            self.widthSB.setValue(Filt.params['Width'])
            self.vcenterSB.setValue(Filt.params['Center'])

        elif Filt.params['Type'] == 'Notch':
            self._enableNotch(True)
            self.notchRB.setChecked(True)
            self.widthSB.setValue(Filt.params['Width'])
            self.hcenterSB.setValue(Filt.params['Center'][0])
            self.vcenterSB.setValue(Filt.params['Center'][1])

        else:
            self._disableAll()
            self.filterDisplay.imshow(np.zeros(self.dim))

        self._updateFilter()
