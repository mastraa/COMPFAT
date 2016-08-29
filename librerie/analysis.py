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
    spectrum = load sptectum
    extreme = local max and min values of spectrum
    ranges = three dimension array : range, number of cycles, mean values
    """
    def __init__(self, fileName, header, fileType='.xlsx', sheet='Carichi', column=1, limit=None):
        if fileType=='.xlsx':   
            try: 
                self.spectrum=file.readXls(fileName, sheet, column, header)
                if limit:
                    self.extreme = cm.reverses(self.spectrum[:limit])
                else:
                    self.extreme = cm.reverses(self.spectrum)
                self.Error='00' #no error
            except (IndexError):
                self.Error='01' #columns doesn't exist
            except(KeyError):
                self.error='02' #sheet doesn't exist
    
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
    
    
    def packing(self,mR,mM):
        """
        check if packing limit are setted and call packing functions
        """
        if mR>0:
            self.block=cm.packRange(self.block,mR)
            if mM>0:
                self.block=cm.packMedian(self.block,mM)
    
    def save(self, fileName, sheet):
        file.writeXls(fileName, self.block, sheet)

class matList:
    def __init__(self, id_n, name, sigma, matrix, fiber):
        self.id=id_n
        self.sigma=sigma
        self.matrix=matrix
        self.fiber=fiber
        self.name=name
        pass