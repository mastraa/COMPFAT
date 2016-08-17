# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016

Analysis class library
"""

import file#, database
import countingMethod as cm
import predictionMethod as pm

class loadStory:
    """
    Class with all the elaboration function for the charge datas
    column begin from 0=A
    """
    def __init__(self, fileName, header, fileType='.xlsx', sheet='Carichi', column=1, limit=None):
        if fileType=='.xlsx':        
            self.spectrum=file.readXls(fileName, sheet, column, header)
        if limit:
            self.extreme = cm.reverses(self.spectrum[:limit])
        else:
            self.extreme = cm.reverses(self.spectrum)
    
    def counting(self, cMethod="Rainflow", hMethod="mean"):
        """
        choose counting method and calculate
        default CM: rainflow
        default HM: mean separation
        """ 
        if cMethod=="Rainflow":
            self.ranges=cm.rainflow(self.extreme)
        elif cMethod=="Simply Rainflow":
            self.ranges=cm.siplyRainflow(self.extreme)
        elif cMethod=="Peak Valley":
            self.ranges=cm.peakValley(self.extreme)
        elif cMethod=="Simple Range":
            self.ranges=cm.simpleRange(self.extreme)
        else:
            print ("unknown method")
        if hMethod=="mean":
            self.block=cm.histoMean(self.ranges)
        else:
            self.block=cm.histo(self.ranges)
    
    def save(self, fileName, sheet):
        file.writeXls(fileName, self.block, sheet)

class matList:
    def __init__(self, id_n, name, sigma, matrix, fiber):
        pass