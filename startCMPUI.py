"""
Starts the main colormap configuration UI
"""
import numpy as np
import matplotlib.pyplot as plt
from PyQt4 import QtGui

from color_maps import Ui_ColorMapsDialog


class startCMPUI(QtGui.QDialog, Ui_ColorMapsDialog):
    """
    popup window for defining the color maps
    """

    def __init__(self, cmaps, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        self.CMaps = cmaps
        self.maps = [m for m in plt.cm.datad if not m.endswith("_r")]
        self.maps.sort()  # organize them in alphabetical order
        #populate the combo boxes
        self.PComboBox.addItems(self.maps)
        self.PComboBox.setCurrentIndex(self.PComboBox.findText(cmaps['phase']))
        self.MComboBox.addItems(self.maps)
        self.MComboBox.setCurrentIndex(self.MComboBox.findText(cmaps['mag']))
        self.KComboBox.addItems(self.maps)
        self.KComboBox.setCurrentIndex(
            self.KComboBox.findText(cmaps['kspace']))
        self.KPComboBox.addItems(self.maps)
        self.KPComboBox.setCurrentIndex(
            self.KPComboBox.findText(cmaps['kphase']))

        #initial draw of the color bars
        self.drawBarM()
        self.drawBarP()
        self.drawBarK()
        self.drawBarKP()
        #connect connect changes in the comboboxes to their function
        self.MComboBox.activated.connect(self.drawBarM)
        self.PComboBox.activated.connect(self.drawBarP)
        self.KComboBox.activated.connect(self.drawBarK)
        self.KPComboBox.activated.connect(self.drawBarKP)

    #these functions regenerate the color bars with the current map
    def drawBarM(self):
        """ Draws the color bar for the magnitude image colormap"""
        a = np.outer(np.arange(0, 1, 0.01), np.ones(20)).T
        index = self.MComboBox.currentIndex()
        self.CMaps['mag'] = self.maps[index]
        self.Mcolorbar.ax.imshow(a, cmap=self.maps[index], aspect='auto')
        self.Mcolorbar.ax.set_position([0, 0, 1, 1])
        self.Mcolorbar.draw()

    def drawBarP(self):
        """ Draws the color bar for the phase image colormap"""
        a = np.outer(np.arange(0, 1, 0.01), np.ones(20)).T
        index = self.PComboBox.currentIndex()
        self.CMaps['phase'] = self.maps[index]
        self.Pcolorbar.ax.imshow(a, cmap=self.maps[index], aspect='auto')
        self.Pcolorbar.ax.set_position([0, 0, 1, 1])
        self.Pcolorbar.draw()

    def drawBarK(self):
        """ Draws the color bar for the kspace image colormap"""
        a = np.outer(np.arange(0, 1, 0.01), np.ones(20)).T
        index = self.KComboBox.currentIndex()
        self.CMaps['kspace'] = self.maps[index]
        self.Kcolorbar.ax.imshow(a, cmap=self.maps[index], aspect='auto')
        self.Kcolorbar.ax.set_position([0, 0, 1, 1])
        self.Kcolorbar.draw()

    def drawBarKP(self):
        """ Draws the color bar for the kspace phase image colormap"""
        a = np.outer(np.arange(0, 1, 0.01), np.ones(20)).T
        index = self.KPComboBox.currentIndex()
        self.CMaps['kphase'] = self.maps[index]
        self.KPcolorbar.ax.imshow(a, cmap=self.maps[index], aspect='auto')
        self.KPcolorbar.ax.set_position([0, 0, 1, 1])
        self.KPcolorbar.draw()
