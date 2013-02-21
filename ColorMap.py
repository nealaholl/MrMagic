# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ColorMap.ui'
#
# Created: Sat Feb  9 19:48:24 2013
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

class Ui_CMapDialog(object):
    def setupUi(self, CMapDialog):
        CMapDialog.setObjectName(_fromUtf8("CMapDialog"))
        CMapDialog.resize(402, 172)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CMapDialog.sizePolicy().hasHeightForWidth())
        CMapDialog.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QtGui.QWidget(CMapDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 151))
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
        self.ComboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.ComboBox.setObjectName(_fromUtf8("ComboBox"))
        self.verticalLayout.addWidget(self.ComboBox)
        self.colorbar = mplWidget(self.verticalLayoutWidget)
        self.colorbar.setObjectName(_fromUtf8("colorbar"))
        self.verticalLayout.addWidget(self.colorbar)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CMapDialog)
        QtCore.QMetaObject.connectSlotsByName(CMapDialog)

    def retranslateUi(self, CMapDialog):
        CMapDialog.setWindowTitle(_translate("CMapDialog", "Color Maps", None))
        self.KLabel.setText(_translate("CMapDialog", "Color Map", None))

from mplwidgetsimple import mplWidget
