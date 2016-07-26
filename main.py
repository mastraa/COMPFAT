# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# cd /Users/mastraa/Documents/Andrea/Università/Magistrale/Tesi/fatigue

import sys, os

sys.path.append('librerie')


import countingMethod as cm
import predictionMethod as pm
#import numpy as np
#import pyqtgraph as pg
import matplotlib.pyplot as plt
#import database as db
import file, analysis


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

storia = analysis.loadStory('data/Monza.xlsx', 1, fileType='xls', sheet='Carichi', column=1, limit=150)
storia.counting()#rainflow and histMean by default
storia.save('data/prova.xlsx', 'result')

#print(storia.ranges)
#print(storia.block)
"""
storia.counting("rainflow_s")
print(storia.ranges)
storia.counting("peakValley")
print(storia.ranges)
storia.counting("simpleRange"
print(storia.ranges)
"""