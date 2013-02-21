# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contrast.ui'
#
# Created: Thu Feb 21 08:43:56 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ContrastSettings(object):
    def setupUi(self, ContrastSettings):
        ContrastSettings.setObjectName(_fromUtf8("ContrastSettings"))
        ContrastSettings.resize(340, 300)
        self.buttonBox = QtGui.QDialogButtonBox(ContrastSettings)
        self.buttonBox.setGeometry(QtCore.QRect(10, 250, 321, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayoutWidget = QtGui.QWidget(ContrastSettings)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 321, 221))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.radioGamma = QtGui.QRadioButton(self.horizontalLayoutWidget)
        self.radioGamma.setObjectName(_fromUtf8("radioGamma"))
        self.verticalLayout_3.addWidget(self.radioGamma)
        self.radioLog = QtGui.QRadioButton(self.horizontalLayoutWidget)
        self.radioLog.setObjectName(_fromUtf8("radioLog"))
        self.verticalLayout_3.addWidget(self.radioLog)
        self.radioConstant = QtGui.QRadioButton(self.horizontalLayoutWidget)
        self.radioConstant.setChecked(True)
        self.radioConstant.setObjectName(_fromUtf8("radioConstant"))
        self.verticalLayout_3.addWidget(self.radioConstant)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gammaSldr = QtGui.QSlider(self.horizontalLayoutWidget)
        self.gammaSldr.setMaximum(100)
        self.gammaSldr.setSingleStep(0)
        self.gammaSldr.setProperty("value", 0)
        self.gammaSldr.setOrientation(QtCore.Qt.Vertical)
        self.gammaSldr.setTickPosition(QtGui.QSlider.TicksBelow)
        self.gammaSldr.setTickInterval(10)
        self.gammaSldr.setObjectName(_fromUtf8("gammaSldr"))
        self.verticalLayout_2.addWidget(self.gammaSldr)
        self.Gamma = QtGui.QLabel(self.horizontalLayoutWidget)
        self.Gamma.setObjectName(_fromUtf8("Gamma"))
        self.verticalLayout_2.addWidget(self.Gamma)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.autoRange = QtGui.QCheckBox(self.horizontalLayoutWidget)
        self.autoRange.setChecked(True)
        self.autoRange.setObjectName(_fromUtf8("autoRange"))
        self.verticalLayout.addWidget(self.autoRange)
        self.labeMinimuml = QtGui.QLabel(self.horizontalLayoutWidget)
        self.labeMinimuml.setObjectName(_fromUtf8("labeMinimuml"))
        self.verticalLayout.addWidget(self.labeMinimuml)
        self.minSB = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.minSB.setEnabled(False)
        self.minSB.setDecimals(1)
        self.minSB.setMaximum(999999.0)
        self.minSB.setSingleStep(0.1)
        self.minSB.setObjectName(_fromUtf8("minSB"))
        self.verticalLayout.addWidget(self.minSB)
        self.labelMaximum = QtGui.QLabel(self.horizontalLayoutWidget)
        self.labelMaximum.setObjectName(_fromUtf8("labelMaximum"))
        self.verticalLayout.addWidget(self.labelMaximum)
        self.maxSB = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.maxSB.setEnabled(False)
        self.maxSB.setDecimals(1)
        self.maxSB.setMaximum(999999.0)
        self.maxSB.setSingleStep(0.1)
        self.maxSB.setObjectName(_fromUtf8("maxSB"))
        self.verticalLayout.addWidget(self.maxSB)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(ContrastSettings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ContrastSettings.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ContrastSettings.accept)
        QtCore.QMetaObject.connectSlotsByName(ContrastSettings)

    def retranslateUi(self, ContrastSettings):
        ContrastSettings.setWindowTitle(_translate("ContrastSettings", "Contrast Settings", None))
        self.radioGamma.setText(_translate("ContrastSettings", "Gamma", None))
        self.radioLog.setText(_translate("ContrastSettings", "Log", None))
        self.radioConstant.setText(_translate("ContrastSettings", "Constant", None))
        self.Gamma.setText(_translate("ContrastSettings", "Gamma", None))
        self.autoRange.setText(_translate("ContrastSettings", "AutoRange", None))
        self.labeMinimuml.setText(_translate("ContrastSettings", "Minimum", None))
        self.labelMaximum.setText(_translate("ContrastSettings", "Maximum", None))

