# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# cd /Users/mastraa/Documents/Andrea/Università/Magistrale/Tesi/fatigue

import sys, os

sys.path.append('librerie')


import countingmethod as cm
import predictionMethod as pm
#import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt
import pygubu
#import database as db
import file


try:
    import tkinter as tk
    from tkinter import messagebox
except:
    import Tkinter as tk
    import tkMessageBox as messagebox

"""
m,q=pm.rect2([0,2],[8,6])
x=pm.xRect(4,m,q)
"""





"""
class lifePredict:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        fpath = os.path.join(os.path.dirname(__file__),"gui.ui")
        builder.add_from_file(fpath)

        mainwindow = builder.get_object('mainWindow', master)

        builder.connect_callbacks(self)
        

if __name__ == '__main__':
    root = tk.Tk()
    app = lifePredict(root)
    root.mainloop()
"""

F=file.readF('prova')#list of forces
for i in range(0,len(F)):
    F[i]=round(F[i],4)
Fs=cm.reverses(F[:10])#list of maximums and minimums
plt.plot(Fs)
plt.show()
Fc=cm.rainflow(Fs)#rainflow method: range, cycles, mean
Fc.append([11.1685,1.0,1148.8189])#prova per l'accumulo dei range con le medie
Fc.append([11.1685,3.0,1148.8189])#prova per l'accumulo dei range con le medie
Fc.append([11.1685,1.0,1149.8189])#prova per l'accumulo dei range con le medie
h=cm.histoMean(Fc)
h_1=cm.histo(Fc)
