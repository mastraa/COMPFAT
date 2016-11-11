# -*- coding: utf-8 -*-
"""
Fatigue Test Software: 

BETA version 0.1.2

Andrea Mastrangelo
Ing.Paolo Carraro
Prof.Marino Quaresimin

Last update: 11/11/2016 (general updates)


Previous release: BETA 0.0.1 - first release
"""

# cd /Users/mastraa/Documents/Andrea/Università/Magistrale/Tesi/fatigue
# cd /Users/gregoriomastrangelo/Desktop/Andrea/Universita/Tesi_Mastrangelo/fatigue

import sys
import matplotlib
matplotlib.use("Qt4Agg")
sys.path.append('librerie')
sys.path.append('librerie/gui')

import mainGui as gui
"""
TODO: study how to hide config files in directory and compile it!
"""

#storia = analysis.loadStory('data/Monza.xlsx', 1, fileType='xls', sheet='Carichi', column=1, limit=150)
#storia.counting()#rainflow and histMean by default
#storia.save('data/prova.xlsx', 'result')

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


radice=gui.MainWindow("COMPFAT","1000x700")#title, width_x_height
radice.iconbitmap('icon.ico')
radice.mainloop()