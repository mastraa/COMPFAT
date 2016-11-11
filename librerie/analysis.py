# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 11/11/2016

Analysis class library
"""

import file#, database
import countingMethod as cm
import predictionMethod as pm
import database
from math import log10

class loadStory:
    """
    Class with all the elaboration function for the charge datas
    column begin from 0=A
    spectrum = load sptectum
    extreme = local max and min values of spectrum
    ranges = three dimension array : range, number of cycles, mean values
    """
    def __init__(self, fileName, header, fileType='.xlsx', sheet='Carichi', column=1, limit=0):
        """
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
    
    def analize(self, data,_sRT,_sRC, per, show, pred="miner"):
        """
        it analize the load story for given material
        data = groups selected
        per=statiscal percent 50/90%
        _ = group material limit
        the group give the fatigue parameter to the max value
        maybe you can read sa90, don't worry, we pass only choosen phi
        
        NB: Rlist will take all groups, RlistTemp only usable group,
        we will search in the RlistTemp for available group and then
        we search the respective index in Rlist. Rlist has all groups
        data, RlistTemp only R!!!
        
        """
        _sRT=int(_sRT)
        _sRC=int(_sRC)
        self.R=_sRT
        self.D=0
        Rlist=[]
        p=0
        for i in range(len(data)):
            if data[i][0]==99 or data[i][0]==-99:
                data[i][0]=data[i][0]*10**10
            Rlist.append(data[i][0])
        for item in self.block:#every amplitude
            sa=item[0]/2#cycle amplitude from range
            for i in item[1]:#every mean for amplitude
                RRight,RLeft=[],[]#divide R values for Haigh Curve
                for r in Rlist:
                    if -1<r<1:
                        RRight.append(r)
                    elif r==-1:
                        RRight.append(r)
                        RLeft.append(r)
                    else:
                        RLeft.append(r)
                p=p+1
                N=i[0]#number of applied cycle fo that load
                sm=i[1]#cycle median                
                R=i[2]#cycle ratio
                if -1<=R<1:#takes only one side of Haigh Curve
                    RlistTemp=RRight
                else:
                    RlistTemp=RLeft
                if sm>=0:
                    _sR=_sRT#considered as traction
                    sApp=sm+sa#s_max, then i will compare abs value
                else:
                    _sR=_sRC#considered as compression
                    sApp=sm-sa#s_min
                try:
                    x=Rlist.index(R)#if we have the group with same R
                    smax2E6=data[x][1]*_sR
                    if per==90:
                        smax2E650=smax2E6#50%
                        smax2E6=data[x][2]*_sR#90%
                        _sR90=10**(log10(_sR)-(log10(smax2E650)-log10(smax2E6)))
                    method="group"
                except ValueError:#if we don't
                    try:#Interpol
                        RlistOrd=RlistTemp[:]
                        RlistOrd.sort()
                        
                        x=Rlist.index(database.nextMax(R,RlistOrd))#first higher value
                        smax2E6M50=data[x][1]*_sR
                        sm_M50=smax2E6M50*(1+Rlist[x])/2
                        sa_M50=smax2E6M50*(1-Rlist[x])/2                       
                        RlistOrd.reverse()
                        x=Rlist.index(database.nextMin(R,RlistOrd))
                        smax2E6m50=data[x][1]*_sR
                        sm_m50=smax2E6m50*(1+Rlist[x])/2
                        sa_m50=smax2E6m50*(1-Rlist[x])/2 
                        smax2E650=pm.interpolationR([sm_m50,sa_m50],[sm_M50,sa_M50],R,sa)
                        if per == 50:
                            smax2E6=smax2E650
                        else:#repeat for 90! I need both to calculate delta 50-90 to get _sR90
                            RlistOrd=RlistTemp[:]
                            RlistOrd.sort()
                        
                            x=Rlist.index(database.nextMax(R,RlistOrd))#first higher value
                            smax2E6M90=data[x][1]*_sR
                            sm_M90=smax2E6M90*(1+Rlist[x])/2
                            sa_M90=smax2E6M90*(1-Rlist[x])/2                       
                        
                            RlistOrd.reverse()
                            x=Rlist.index(database.nextMin(R,RlistOrd))
                            smax2E6m90=data[x][1]*_sR
                            sm_m90=smax2E6m90*(1+Rlist[x])/2
                            sa_m90=smax2E6m90*(1-Rlist[x])/2 
                        
                            smax2E6=pm.interpolationR([sm_m90,sa_m90],[sm_M90,sa_M90],R,sa)
                            _sR90=10**(log10(_sR)-(log10(smax2E650)-log10(smax2E6)))
                        method="interpol"
                        if R>1 and Rlist(x)<=1:
                            raise NameError('No value')
                    except(NameError, TypeError):#Rmethod 
                        x=Rlist.index(RlistTemp[0])
                        _R=data[x][0]
                        _smax2E6R50=float(data[x][1])*_sR
                        smax2E6=pm.Rmethod(_sR,_R,_smax2E6R50,R,sa)
                        if per==90:
                            _smax2E6R90=float(data[x][2])*_sR
                            _sR90=10**(log10(_sR)-(log10(_smax2E6R50)-log10(_smax2E6R90)))
                            smax2E6=pm.Rmethod(_sR90,_R,_smax2E6R90,R,sa)
                        method="other"
                if per == 90:
                    _sR=_sR90
                if pred=="miner":
                    minerD,m=pm.miner(_sR,smax2E6,abs(sApp),N)
                    self.D=self.D+minerD
                    if show==1:
                        print('{0:5d}: {1:2d}% {2:10} {3:7f} {4:7f} {5:7f} {6:10e} {7:10e}'.format(p,per,method,round(sApp,2),round(smax2E6,2),round(m,5),minerD,self.D))
                else: #Broutman-Sahu
                    minerD,m=pm.miner(_sR,smax2E6,abs(sApp),N)
                    damn=(self.R-abs(sApp))*minerD
                    self.R==self.R-damn
                    if show==1:
                        print('{0:5d}: {1:2d}% {2:10} {3:7f} {4:7f} {5:7f} {6:10e} {7:10e}'.format(p,per,method,round(sApp,2),round(smax2E6,2),round(m,5),damn,self.R))
                print()                    

class matList:
    def __init__(self, id_n, name, sigmaT, matrix, fiber,sigmaC):
        self.id=id_n
        self.sigmaT=sigmaT
        self.sigmaC=sigmaC
        self.matrix=matrix
        self.fiber=fiber
        self.name=name
        pass