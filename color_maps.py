# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'color_maps.ui'
#
# Created: Mon Dec 03 21:56:20 2012
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ColorMapsDialog(object):
    def setupUi(self, ColorMapsDialog):
        ColorMapsDialog.setObjectName(_fromUtf8("ColorMapsDialog"))
        ColorMapsDialog.resize(400, 443)
        self.verticalLayoutWidget = QtGui.QWidget(ColorMapsDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 421))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.KLabel = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.KLabel.setFont(font)
        self.KLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.KLabel.setIndent(0)
        self.KLabel.setObjectName(_fromUtf8("KLabel"))
        self.verticalLayout.addWidget(self.KLabel)
        self.KComboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.KComboBox.setObjectName(_fromUtf8("KComboBox"))
        self.verticalLayout.addWidget(self.KComboBox)
        self.Kcolorbar = mplCanvas(self.verticalLayoutWidget)
        self.Kcolorbar.setObjectName(_fromUtf8("Kcolorbar"))
        self.verticalLayout.addWidget(self.Kcolorbar)
        self.KPLabel = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.KPLabel.setFont(font)
        self.KPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.KPLabel.setObjectName(_fromUtf8("KPLabel"))
        self.verticalLayout.addWidget(self.KPLabel)
        self.KPComboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.KPComboBox.setObjectName(_fromUtf8("KPComboBox"))
        self.verticalLayout.addWidget(self.KPComboBox)
        self.KPcolorbar = mplCanvas(self.verticalLayoutWidget)
        self.KPcolorbar.setObjectName(_fromUtf8("KPcolorbar"))
        self.verticalLayout.addWidget(self.KPcolorbar)
        self.MLabel = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.MLabel.setFont(font)
        self.MLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MLabel.setIndent(0)
        self.MLabel.setObjectName(_fromUtf8("MLabel"))
        self.verticalLayout.addWidget(self.MLabel)
        self.MComboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.MComboBox.setObjectName(_fromUtf8("MComboBox"))
        self.verticalLayout.addWidget(self.MComboBox)
        self.Mcolorbar = mplCanvas(self.verticalLayoutWidget)
        self.Mcolorbar.setObjectName(_fromUtf8("Mcolorbar"))
        self.verticalLayout.addWidget(self.Mcolorbar)
        self.PLabel = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.PLabel.setFont(font)
        self.PLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PLabel.setIndent(0)
        self.PLabel.setObjectName(_fromUtf8("PLabel"))
        self.verticalLayout.addWidget(self.PLabel)
        self.PComboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.PComboBox.setObjectName(_fromUtf8("PComboBox"))
        self.verticalLayout.addWidget(self.PComboBox)
        self.Pcolorbar = mplCanvas(self.verticalLayoutWidget)
        self.Pcolorbar.setObjectName(_fromUtf8("Pcolorbar"))
        self.verticalLayout.addWidget(self.Pcolorbar)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ColorMapsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ColorMapsDialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ColorMapsDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(ColorMapsDialog)

    def retranslateUi(self, ColorMapsDialog):
        ColorMapsDialog.setWindowTitle(QtGui.QApplication.translate("ColorMapsDialog", "Color Maps", None, QtGui.QApplication.UnicodeUTF8))
        self.KLabel.setText(QtGui.QApplication.translate("ColorMapsDialog", "K-Space Color Map", None, QtGui.QApplication.UnicodeUTF8))
        self.KPLabel.setText(QtGui.QApplication.translate("ColorMapsDialog", "K-Space Phase Color Map", None, QtGui.QApplication.UnicodeUTF8))
        self.MLabel.setText(QtGui.QApplication.translate("ColorMapsDialog", "Magnitude Image Color Map", None, QtGui.QApplication.UnicodeUTF8))
        self.PLabel.setText(QtGui.QApplication.translate("ColorMapsDialog", "Phase Image Color Map", None, QtGui.QApplication.UnicodeUTF8))

from mplwidget import mplCanvas
