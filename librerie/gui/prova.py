# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 18:59:32 2016

@author: mastraa
"""

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

def play():
    #QtGui.QApplication.setGraphicsSystem('raster')
    app = QtGui.QApplication([])
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('pyqtgraph example: PlotWidget')
    mw.resize(800,800)
    cw = QtGui.QWidget()
    mw.setCentralWidget(cw)
    l = QtGui.QVBoxLayout()
    cw.setLayout(l)
    
    pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
    l.addWidget(pw)
    pw2 = pg.PlotWidget(name='Plot2')
    l.addWidget(pw2)
    pw3 = pg.PlotWidget()
    l.addWidget(pw3)

    mw.show()

    ## Start Qt event loop unless running in interactive mode or using pyside.
    if __name__ == '__main__':
        import sys
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()