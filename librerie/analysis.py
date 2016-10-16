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
import database

class loadStory:
    """
    Class with all the elaboration function for the charge datas
    column begin from 0=A
    spectrum = load sptectum
    extreme = local max and min values of spectrum
    ranges = three dimension array : range, number of cycles, mean values
    """
    def __init__(self, fileName, header, fileType='.xlsx', sheet='Carichi', column=1, limit=None):
        """
        TODO: no limit = ValueError-->make possible to read all value in the column
        """
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
        maybe you can read sa90, don't worry, we pass only choosen phi
        """
        _sRT=int(_sRT)
        _sRC=int(_sRC)
        self.D=0
        Rlist=[]
        p=0
        for j in data:
            Rlist.append(j[0])
        for item in self.block:#every amplitude
            sa=item[0]/2#cycle amplitude from range
            for i in item[1]:#every mean for amplitude
                p=p+1
                sm=i[1]#cycle median
                N=i[0]#number of applied cycle fo that load
                try:
                    R=round((sm-sa)/(sm+sa),1)
                    if R<-99:#-99 is group limit
                        R=-99
                    elif R>99:#99 is group limit
                        R=99
                except ZeroDivisionError:
                    R=-99
                if sm>0:
                    _sR=_sRT#considered as traction
                else:
                    _sR=_sRC#considered as compression
                try:
                    x=Rlist.index(R)#if we have the group with same R
                    sa90=data[x][1]*_sR*(1-R)/2
                    print("ORA")
                except ValueError:#if we don't
                    if Rmethod=="Interpol":
                        RlistOrd=Rlist.sort()
                        x=Rlist.index(database.nextMin(R,RlistOrd))
                        sa90m=data[x][1]*_sR*(1-R)/2
                        sm_m=(1+R)*data[x][1]*_sR/2
                        x=Rlist.index(database.nextMin(R,RlistOrd.reverse()))
                        sa90M=data[x][1]*_sR*(1-R)/2
                        sm_M=(1+R)*data[x][1]*_sR/2
                        sa90=pm.interpolationR([sa90m,sm_m],[sa90M,sm_M],R,sa)
                    else:#Rmethod
                        """
                        TODO: possibility to choose which group
                        """
                        _R=data[0][0]#take the first point
                        _smax90R=float(data[0][1])*_sR
                        sa90=pm.Rmethod(_sR,_R,_smax90R,R,sa)
                minerD=pm.miner(_sR,sa90,sa,N)
                self.D=self.D+minerD
                print(p, sa, sm, sa90, minerD,self.D)
                print()
                
    def plot(self):
        """
        It will plot extreme values of the spectrum
        TODO: create the block cycle array to plot
        """
        pg.plot(self.extreme, symbol='o')

class matList:
    def __init__(self, id_n, name, sigmaT, matrix, fiber,sigmaC):
        self.id=id_n
        self.sigmaT=sigmaT
        self.sigmaC=sigmaC
        self.matrix=matrix
        self.fiber=fiber
        self.name=name
        pass