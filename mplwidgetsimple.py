
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class mplWidget(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_axis_off()

        self.CMap = 'gray'
        self.cbar = None
        

        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)