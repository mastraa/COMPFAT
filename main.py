# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# cd /Users/mastraa/Documents/Andrea/Università/Magistrale/Tesi/fatigue
# cd /Users/gregoriomastrangelo/Desktop/Andrea/Universita/Tesi_Mastrangelo/fatigue/librerie/gui

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


radice=gui.MainWindow("Titolo","900x600")
radice.mainloop()