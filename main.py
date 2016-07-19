# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys, os

sys.path.append('librerie')


import countingmethod as cm
import predictionMethod as pm
#import numpy as np
#import pyqtgraph as pg
import pygubu
import database as db

try:
    import tkinter as tk
    from tkinter import messagebox
except:
    import Tkinter as tk
    import tkMessageBox as messagebox

#x = np.linspace(0,4,20)
#y = 0.2 + 0.5*np.sin(x) + 0.2*np.cos(10*x) + 0.2*np.sin(4*x)

#cycles = rainflow_m.extract_cycles(y)

#pv=rainflow.peakvalley(y)
#cicli=rainflow.cycles(pv)


m,q=pm.rect2([0,2],[8,6])
x=pm.xRect(4,m,q)


class lifePredict:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        fpath = os.path.join(os.path.dirname(__file__),"gui.ui")
        builder.add_from_file(fpath)

        mainwindow = builder.get_object('mainWindow', master)

        builder.connect_callbacks(self)
        
"""
if __name__ == '__main__':
    root = tk.Tk()
    app = lifePredict(root)
    root.mainloop()
"""