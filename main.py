# -*- coding: utf-8 -*-
"""
Fatigue Test

BETA version 0.0.1

Andrea Mastrangelo
Ing.Paolo Carraro
Prof.Marino Quaresimin
"""

# cd /Users/mastraa/Documents/Andrea/Università/Magistrale/Tesi/fatigue
# cd /Users/gregoriomastrangelo/Desktop/Andrea/Universita/Tesi_Mastrangelo/fatigue

import sys

sys.path.append('librerie')
sys.path.append('librerie/gui')

import mainGui as gui

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


radice=gui.MainWindow("Prova","1000x650")#title, width_x_height
radice.mainloop()