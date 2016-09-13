# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016

Analysis class library
"""

import file#, database
import countingMethod as cm
import predictionMethod as pm
import pyqtgraph as pg

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
                self.spectrum=file.readXls(fileName, sheet, column, header, limit)
                self.extreme=cm.reverses(self.spectrum)
                self.Error=0 #no error
            except (IndexError):
                self.Error=1 #columns doesn't exist
            except(KeyError):
                self.Error=2 #sheet doesn't exist
            except(TypeError):
                self.Error=3 #wrong column, no numbers
    
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
            
    def errorsCheck(self, dt):
        if self.Error==1:
            string=string=dt+" Error: the column doesn't exist! Story won't be created"
        elif self.Error==2:
            string=dt+" Error: the sheet doesn't exist! Story won't be created"
        elif self.Error==3:
            string=dt+" Error: Content of selected cells is not number"
        else:
            string='Unknown Error'
        return string
    
    
    def packing(self,mR,mM,v):
        """
        check if packing limit are setted and call packing functions
        """
        if mR>0:
            self.block=cm.packRange(self.block,mR,v)
            if mM>0:
                self.block=cm.packMedian(self.block,mM,v)
    
    def save(self, fileName, sheet):
        file.writeXls(fileName, self.block, sheet)
    
    def analize(self, data,_sRT,_sRC,Rmethod):
        """
        it analize the load story for given material
        data = groups selected
        _ = group material limit
        the group give the fatigue parameter to the max value
        """
        _sRT=int(_sRT)
        _sRC=int(_sRC)
        D=0
        Rlist=[]
        for j in data:
            Rlist.append(j[0])
        for item in self.block:#every amplitude
            sa=item[0]#cycle amplitude
            for i in item[1]:#every mean for amplitude
                sm=i[1]#cycle median
                N=i[0]#number of applied cycle fo that load
                R=(sm-sa)/(sm+sa)
                if sm>0:
                    _sR=_sRT
                else:
                    _sR=_sRC
                try:
                    x=Rlist.index(R)#if we have the group with same R
                    sa90=data[x][2]*_sR*(1+R)/2
                except ValueError:#no correspondent group
                    try:
                        x=Rlist.index(-1)#we have group for R=-1
                        _sa=data[x][2]*_sR#R=-1 so (1+R)/2=0
                        sa90=pm.haigh(_sa,R,sm)
                    except ValueError:
                        _R=int(data[0][0])
                        _smax90R=float(data[0][2])*_sR
                        sa90=pm.genHaigh(_sR,_R,_smax90R,R,sa,Rmethod)
                D=D+pm.miner(_sR,sa90,sa,N)
                print(sa90,D)
                
    def plot(self):
        """
        It will plot extreme values of the spectrum
        TODO: create the block cycle array to plot
        """
        pg.plot(self.extreme, symbol='o')

class matList:
    def __init__(self, id_n, name, sigmaT, matrix, fiber,sigmaR):
        self.id=id_n
        self.sigmaT=sigmaT
        self.sigmaR=sigmaR
        self.matrix=matrix
        self.fiber=fiber
        self.name=name
        pass