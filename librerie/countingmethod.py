# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016
"""
import numpy as np
from copy import deepcopy

__version__="0.0.1"

def reverses(history):
    """
    The function converts the spectrum in an array with only maximum and
    minimum values
    INPUT array of charge
    OUTPUT array with maximum and minimum values
    """
    serie=[]
    serie.append(history[0])
    i=1
    while i<len(history):
        if history[i]>=history[i-1]:
            while( i<len(history) and history[i]>=history[i-1]):
                i=i+1
            serie.append(history[i-1])
        if i>=len(history):#otherwise it will raise an index exception
            break
        if history[i]<history[i-1]:
            while ( i<len(history) and history[i]<history[i-1]):
                i=i+1
            serie.append(history[i-1])
    return serie  
    
def histo(s):
    """
    Calculation of cumulative histograms of ranges divided by range
    INPUT: ranges array
    OUTPUT: array made by two array with ranges and relative frequency
            first higher range value
    """
    temp_v=[] #values
    temp_f=[] #frequency
    for i in range (0,len(s)):
        temp_v.append(round(s[i][0],4))
    temp_v=list(set(temp_v))
    temp_v.sort()
    temp_v.reverse()
    for item in temp_v:
        n=0
        for value in s:
            if round(value[0],4)==item:
                n=n+value[1]
        temp_f.append(n)
    return [temp_v,temp_f]
    
def histoMean(s):
    """
    Calculation of cumulative histograms of ranges divided by range and mean value
    INPUT: ranges array
    OUTPUT: array made by two array with ranges and relative frequency
            first higher range value
    """
    temp=[]
    temp_v=[]
    for i in range (0,len(s)):
        temp.append(round(s[i][0],4))
    temp=list(set(temp))
    temp.sort()
    temp.reverse()
    for item in temp:
        temp_v.append([item,[]])
    flag=1
    for value in s:
        for item in temp_v:
            flag=1
            if round(value[0],4)==item[0]:#if range value are egual
                for char in item[1]:
                    if round(value[2],4)==char[1]:#if mean values are egual
                        char[0]=char[0]+value[1]#increment cycles value
                        flag=0#get down flag
                if flag:#if mean values yet to be add
                    item[1].append([value[1],round(value[2],4)])
    """for item in temp_v:
        print (temp_v)"""#debug
    return temp_v
    
def rearrangeMax(serie):
    """
    Return the serie rearranged starting with max value
    """
    maxPos=serie.index(max(serie))
    return serie[maxPos:]+serie[:maxPos]+serie[maxPos:maxPos+1]

def rainflow(serie):#s = serie of peak and valley
    """
    Rainflowcycle counting algorithm according to ASTM E1049-85 (2005)
    INPUT the serie of peak and valley as a vector
    OUTPUT three dimension array with range, cycles number and mean value
    mean value from "nonmandatory infornation" of E1049-85
    
    [value, cicles, mean]    
    """
    s=deepcopy(serie)#prevent modification of original array!
    i=0
    ranges=[]
    if isinstance(s,np.ndarray):
        s=s.tolist()
    while i<len(s)-1:#-1 because index increment is later
        i=i+1
        if i>1:
            #create ranges
            X=round(abs(s[i]-s[i-1]),4)
            Y=round(abs(s[i-1]-s[i-2]),4)
            #print (i,X,Y)
            #print(s)
            if X>=Y:
                if i == 2: #range Y contains the starting point
                    ranges.append([Y,0.5,round((s[i-1]+s[i-2])/2,4)])
                    del(s[0]) #deleting starting point
                    i=i-1 #cause to reducing s lenght
                else:
                    ranges.append([Y,1.0,round((s[i-1]+s[i-2])/2,4)])
                    del(s[i-2:i]) #discarding Y peak and valley
                    i=i-3 #case to reducing s lenght of 2, but not reread (see position of i increment)
    for i in range (1,len(s)):
        ranges.append([abs(s[i]-s[i-1]),0.5,round((s[i]+s[i-1])/2,4)])
    return ranges 

def simplyRainflow(serie):
    """
    Simplifued Rainflowcycle counting algorithm according to ASTM E1049-85 (2005)
    Use for repetitive history
    Before use that rearrange the history: it must stat with maximum
    """
    s=rearrangeMax(serie)#always rearrange!!! not sure to check only some values
    if isinstance(s,np.ndarray):
        s=s.tolist()
    i=0
    ranges=[]
    while i<len(s)-1:#-1 because index increment is later
        i=i+1
        if i>1:
            #create ranges
            X=round(abs(s[i]-s[i-1]),4)
            Y=round(abs(s[i-1]-s[i-2]),4)
            #print (i,X,Y)
            #print(s)
            if X>=Y:
                ranges.append([Y,1.0,round((s[i-1]+s[i-2])/2,4)])
                del(s[i-2:i]) #discarding Y peak and valley
                i=i-3 #case to reducing s lenght of 2, but not reread (see position of i increment)
    for i in range (1,len(s)):
        ranges.append([abs(s[i]-s[i-1]),0.5,round((s[i]+s[i-1])/2,4)])
    return ranges
    
def peakValley(s):
    """
    PeakValley counting method
    According to the algorithm described in 'Appunti di costruzione di macchine'
    prof. B.Atzori
    """
    Mean=np.mean(s)
    pv=[]
    pv.append([])
    pv.append([])
    b=0
    if s[0]<s[1]:
        b=1
    for item in s:
        pv[b].append(item)
        b=not b
    pv[0].sort()
    pv[0].reverse()
    pv[1].sort()
    i=0
    for item in pv[0]:
        if item > Mean:
            i=i+1
        else:
            break
    pv[0]=pv[0][:i]
    i=0
    for item in pv[1]:
        if item < Mean:
            i=i+1
        else:
            break
    pv[1]=pv[1][:i]
    ranges=[]
    for i in range(0,len(pv[0])):
        try:
            ranges.append([abs(pv[0][i]-pv[1][i]),1,Mean])
        except IndexError:
            ranges.append([abs(pv[0][i]),0.5,Mean])
    if i < (len(pv[1])-1):
        for a in range(i,len(pv[1])):
            ranges.append([abs(pv[1][a]),0.5,Mean])
    return ranges

def simpleRange(s):
    """
    Simple range counting method
    INPUT: serie made of peak and valley as a vector
    OUTPUT: range and medium value
    """
    ranges=[]
    for i in range (1,len(s)):
        ranges.append([abs(s[i]-s[i-1]),0.5,(s[i]+s[i-1])/2])
    return ranges

def packRange(ranges, dim, v):
    """
    it will pack ranges and means in interval of dim dimension
    new range value would be the medim value of interval
    
    it returns new histo range list
    
    it will work only with histoRange output
    """
    x=ranges[0][0]-dim#max range value-dimension of interval
    #x is the lower value of everty interval
    block=[]
    i=0#counter for new variable
    j=0#counter of ranges items inserted
    while x>0:
        if v == 1:
            block.append([x+dim/2,[]])#block value is the median value
        else:
            block.append([x+dim,[]])#block values is the max extreme of interval
        #it will create a pack for every interval
        #someone will be empty and deleted
        for item in ranges[j:]:
            if x<item[0]:
                for value in item[1]:
                    block[i][1].append(value)
                j=j+1#it will exclude used ranges
        x=x-dim
        i=i+1
    """    
    previous loop will lose last ranges if their value is near to zero
    because the lower limit of next interval would be negative
    so they will be added assuming as range value the higher value of remaining
    ranges
    """
    try:
        block.append([ranges[j][0],[]])
        for item in ranges[j:]:
            for value in item[1]:
                block[i][1].append(value)
    except IndexError:#alla ranges inserted yet
        pass
    #deleting empty cycles
    t=0
    while t <len(block):
        if block[t][1]==[]:
            del(block[t])
        else:
            t=t+1
    for item in block:
        print(item)#debug"""
    return block
    
def packMedian(ranges, dim, v):
    """
    Pack cycles with similan median
    Call only after a packRange
    """
    print(v)
    block=[]
    for item in ranges:#for every range value
        z=[]
        block.append([item[0],[]])#insert amplitude value
        for i in item[1]:
            z.append(round(i[1]))
        lim=min(z)
        max_m=max(z)
        if len(z)>1:#there are more than one block
            while lim<=max_m:
                c=0
                for i in item[1]:
                    if i[1]>=lim and i[1]<lim+dim:
                        c=c+i[0]
                lim=lim+dim
                if v == 1:#median value
                    block[-1][1].append([c,lim+dim/2])
                else:#max value
                    block[-1][1].append([c,lim+dim])
        else:
            block[-1][1]=item[1]
    for item in block:
        t=0
        while t<len(item[1]):
            if item[1][t][0]==0:
                del item[1][t]
            else:
                t=t+1
    for item in block:
        print(item)#debug"""
    return block
            
        
        
        
            
    