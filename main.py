# -*- coding: utf-8 -*-
"""
Fatigue Test Software: 

BETA version 0.1.2

Andrea Mastrangelo
Ing.Paolo Carraro
Prof.Marino Quaresimin

Last update: 28/11/2016 (general updates)


Previous release: BETA 0.0.1 - first release
"""

# cd /Users/mastraa/Documents/Andrea/Università/Magistrale/Tesi/fatigue
# cd /Users/gregoriomastrangelo/Desktop/Andrea/Universita/Tesi_Mastrangelo/fatigue

import sys,os
import matplotlib
matplotlib.use("Qt4Agg")

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

sys.path.append(os.path.join(application_path, 'librerie'))
sys.path.append(os.path.join(application_path, 'librerie/gui'))


#sys.path.append('librerie')
#sys.path.append('librerie/gui')

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


radice=gui.MainWindow("COMPFAT","1000x700", application_path)#title, width_x_height
radice.iconbitmap(os.path.join(application_path,'configFile/icon.ico'))
radice.mainloop()