
import numpy as np
import filters as filt
from filter_display import Ui_Filter
from PyQt4 import QtGui
from mplwidget import mplCanvas


class startFilterUI(QtGui.QDialog, Ui_Filter):
    Filters = {}
    M_N = (0, 0)
    Shape = {}
    Outer = {}
    Contour = {}
    CR = {}

    #popup window for showing the shape of a window function
    def __init__(self, Names, Filters, Shape, Radius, Outer, CR, M_N,
                 parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Filter()
        self.setupUi(self)

        #This makes it easier to use the member functions
        self.Filters = Filters
        self.M_N = M_N
        self.Shape = Shape
        self.Outer = Outer
        self.Radius = Radius
        self.CR = CR
        #holders for the GUI objects
        self.tabWidget.clear()  # overall tab
        self.tab = {}  # individual tabs
        self.filter_display = {}  # the plot of the filter
        self.window = {}  # the filter marticies
        self.constructionBox = {}  # box to group construction radiobuttons
        self.constructionLayout = {}  # layout for that box
        self.contourBox = {}  # box to group contour type radiobuttons
        self.contourLayout = {}  # layout for that box
        self.radioOuter = {}  # outer product radiobutton
        self.radioRotated = {}  # rotated radiobutton
        self.radioConstRadius = {}  # constant radius contour radiobutton
        self.radioConstFreq = {}  # constant frequency contour radiobutton
        self.radiusLabel = {}  # label for the radius spinbox
        self.radiusSB = {}  # spinbox for the filter radius
        self.shapeLabel = {}  # label for the shape spinbox
        self.shapeSB = {}  # spinbox for the shape value
        self.leftLayout = {}  # layout for the left side of the tab
        self.rightLayout = {}  # layout for the right side of the tab
        self.tabLayout = {}  # layout for the whole tab

        #build the GUI for each filter
        for f in Names:
            text = str(f.text())  # get filter name
            #create the needed layouts
            self.tabLayout[text] = QtGui.QHBoxLayout()
            self.leftLayout[text] = QtGui.QVBoxLayout()
            self.rightLayout[text] = QtGui.QVBoxLayout()
            self.tabLayout[text].addLayout(self.leftLayout[text], stretch=1)
            self.tabLayout[text].addLayout(self.rightLayout[text], stretch=2)

            self.constructionLayout[text] = QtGui.QVBoxLayout()
            self.constructionLayout[text].addStretch(1)

            self.contourLayout[text] = QtGui.QVBoxLayout()
            self.contourLayout[text].addStretch(1)

            #configure the tab for that filter
            self.tab[text] = QtGui.QWidget()
            self.tab[text].setLayout(self.tabLayout[text])
            self.tab[text].setObjectName(text)
            self.tabWidget.addTab(self.tab[text], text)

            #add radio buttons to set the construction type
            self.constructionBox[text] = QtGui.QGroupBox(parent=self.tab[text])
            self.constructionBox[text].setTitle("Construction Type")
            self.constructionBox[text].setFixedHeight(75)
            self.leftLayout[text].addWidget(self.constructionBox[text])
            self.constructionBox[text].setLayout(self.constructionLayout[text])

            self.radioOuter[text] = \
                QtGui.QRadioButton(self.constructionBox[text])
            self.radioOuter[text].setText("Outer Product")
            self.radioOuter[text].toggled.connect(self.outerUpdate)
            self.constructionLayout[text].addWidget(self.radioOuter[text])

            self.radioRotated[text] = \
                QtGui.QRadioButton(self.constructionBox[text])
            self.radioRotated[text].setText("Rotational")
            self.constructionLayout[text].addWidget(self.radioRotated[text])

            #add radio buttons to set the contour type
            self.contourBox[text] = QtGui.QGroupBox(parent=self.tab[text])
            self.contourBox[text].setTitle("Contour Type")
            self.contourBox[text].setFixedHeight(75)
            self.leftLayout[text].addWidget(self.contourBox[text])
            self.contourBox[text].setLayout(self.contourLayout[text])

            self.radioConstRadius[text] = \
                QtGui.QRadioButton(self.contourBox[text])
            self.radioConstRadius[text].setText("Constant Radius")
            self.radioConstRadius[text].toggled.connect(self.contourUpdate)
            self.contourLayout[text].addWidget(self.radioConstRadius[text])

            self.radioConstFreq[text] = \
                QtGui.QRadioButton(self.contourBox[text])
            self.radioConstFreq[text].setText("Constant Frequency")
            self.contourLayout[text].addWidget(self.radioConstFreq[text])

            #add a spin box to set the filter radius
            self.radiusLabel[text] = QtGui.QLabel()
            self.radiusLabel[text].setText("Radius")
            self.leftLayout[text].addWidget(self.radiusLabel[text])
            self.radiusSB[text] = QtGui.QSpinBox(self.tab[text])
            self.radiusSB[text].setMaximum(4096)
            self.radiusSB[text].setValue(self.Radius[text])
            self.radiusSB[text].valueChanged.connect(self.radiusUpdate)
            self.radiusSB[text].setSingleStep(2)
            self.leftLayout[text].addWidget(self.radiusSB[text])

            #add a spin box for the shaping value, if it has one
            if (text == 'Dolph-Chebyshev') or (text == 'Gaussian') or \
                    (text == 'Kaiser') or (text == 'Slepian'):
                self.shapeLabel[text] = QtGui.QLabel()
                self.shapeLabel[text].setText("Shape")
                self.leftLayout[text].addWidget(self.shapeLabel[text])
                self.shapeSB[text] = QtGui.QDoubleSpinBox(self.tab[text])
                self.shapeSB[text].setMaximum(4096)
                self.shapeSB[text].setDecimals(2)
                self.shapeSB[text].setSingleStep(0.01)
                self.shapeSB[text].setValue(self.Shape[text])
                self.shapeSB[text].valueChanged.connect(self.shapeUpdate)
                self.leftLayout[text].addWidget(self.shapeSB[text])

            #add in the display for the frequency domain filter
            self.filter_display[text] = mplCanvas(self.tab[text])
            self.rightLayout[text].addWidget(self.filter_display[text])
            if Outer[text]:
                self.radioOuter[text].setChecked(True)
            else:
                self.radioRotated[text].setChecked(True)
            if CR[text]:
                self.radioConstRadius[text].setChecked(True)
            else:
                self.radiConstFreq[text].setChecked(True)
            self.drawFilter(text)
        self.show()

    def outerUpdate(self):
        "Call back for when the construction method is changed"
        self.Outer[str(self.sender().parent().parent().objectName())] = \
            self.sender().isChecked()
        self.drawFilter(str(self.sender().parent().parent().objectName()))

    def contourUpdate(self):
        "Call back for when the contour type is changed"
        self.CR[str(self.sender().parent().parent().objectName())] = \
            self.sender().isChecked()
        self.drawFilter(str(self.sender().parent().parent().objectName()))

    def radiusUpdate(self):
        "Call back for when the radius is changed"
        self.Radius[str(self.sender().parent().objectName())] = \
            self.sender().value()
        self.drawFilter(str(self.sender().parent().objectName()))

    def shapeUpdate(self):
        "Call back for when the shape is changed"
        self.Shape[str(self.sender().parent().objectName())] = \
            self.sender().value()
        self.drawFilter(str(self.sender().parent().objectName()))

    def drawFilter(self, text):
        if (text == 'Dolph-Chebyshev') or (text == 'Gaussian') or \
                (text == 'Kaiser') or (text == 'Slepian'):
            self.window[text] = filt.build2d_lp(Window=(self.Filters[text],
                                                        self.Shape[text]),
                                                Dim=self.M_N,
                                                Radius=self.Radius[text],
                                                Outer=self.Outer[text],
                                                CR=self.CR[text])
        elif text == 'None':
            self.window[text] = np.ones((self.M_N))
        else:
            self.window[text] = filt.build2d_lp(Window=self.Filters[text],
                                                Dim=self.M_N,
                                                Radius=self.Radius[text],
                                                Outer=self.Outer[text],
                                                CR=self.CR[text])
        self.filter_display[text].imshow(self.window[text])
