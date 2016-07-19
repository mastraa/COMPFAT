# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016
"""
#import numpy as np

__version__="0.0.1"
__s__=[-2,1,-3,5,-1,3,-4,4,-2]
#__x__ = np.linspace(0,4,20)
#__spectrum__= 0.2 + 0.5*np.sin(__x__) + 0.2*np.cos(10*__x__) + 0.2*np.sin(4*__x__)


def rainflow(s):#s = serie of peak and valley
    """
    Rainflowcycle counting algorithm according to ASTM E1049-85 (2005)
    INPUT the serie of peak and valley as a vector
    OUTPUT three dimension array with range, cycles number and mean value
    mean value from "nonmandatory infornation" of E1049-85
    """
    i=0
    cycles=[]
    #if isinstance(s,np.ndarray):
    #    s=s.tolist()
    while i<len(s)-1:#-1 because index increment is later
        i=i+1
        if i>1:
            #create ranges
            X=abs(s[i]-s[i-1])
            Y=abs(s[i-1]-s[i-2])
            #print (i,X,Y)
            #print(s)
            if X>=Y:
                if i == 2: #range Y contains the starting point
                    cycles.append([Y,0.5,(s[i-1]+s[i-2])/2])
                    del(s[0]) #deleting starting point
                    i=i-1 #cause to reducing s lenght
                else:
                    cycles.append([Y,1.0,(s[i-1]+s[i-2])/2])
                    del(s[i-2:i]) #discarding Y peak and valley
                    i=i-3 #case to reducing s lenght of 2, but not reread (see position of i increment)
    for i in range (1,len(s)):
        cycles.append([abs(s[i]-s[i-1]),0.5,(s[i]+s[i-1])/2])
    return cycles
    
    
    
def reverses(history):
    """
    The function converts the spectrum in an array with only peaks and valleys
    INPUT array of charge
    OUTPUT array with peaks and valleys
    """
    serie=[]
    serie.append(history[0])
    i=1
    while i<len(history):
        if history[i]>=history[i-1]:
            while( i<len(history) and history[i]>=history[i-1]):
                i=i+1
            serie.append(history[i-1])
        if history[i]<history[i-1]:
            while ( i<len(history) and history[i]<history[i-1]):
                i=i+1
            serie.append(history[i-1])
    return serie
    
    
    
def histo(s):
    """
    Calculation of cumulative histograms of ranges
    INPUT: ranges array
    OUTPUT: array made by two array with ranges and relative frequency
            first higher range value
    """
    temp_v=[] #values
    temp_f=[] #frequency
    for i in range (0,len(s)):
        temp_v.append(s[i][0])
    temp_v=list(set(temp_v))
    temp_v.sort()
    temp_v.reverse()
    for item in temp_v:
        n=0
        for value in s:
            if value[0]==item:
                n=n+value[1]
        temp_f.append(n)
    return [temp_v,temp_f]
    
    
def rearrangeMax(serie):
    """
    Return the serie rearranged starting with max value
    """
    maxPos=serie.index(max(serie))
    return serie[maxPos:]+serie[:maxPos]+serie[maxPos:maxPos+1]
    
    
    
def simplyRainflow(serie):
    """
    Simplifued Rainflowcycle counting algorithm according to ASTM E1049-85 (2005)
    Use for repetitive history
    Before use that rearrange the history: it must stat with maximum
    """
    if serie.index(max(serie)) > 0:#check if history is rearranged
        s=rearrangeMax(serie)
    else:
        s=serie
    #if isinstance(s,np.ndarray):
    #    s=s.tolist()
    i=0
    cycles=[]
    while i<len(s)-1:#-1 because index increment is later
        i=i+1
        if i>1:
            #create ranges
            X=abs(s[i]-s[i-1])
            Y=abs(s[i-1]-s[i-2])
            #print (i,X,Y)
            #print(s)
            if X>=Y:
                cycles.append([Y,1.0,(s[i-1]+s[i-2])/2])
                del(s[i-2:i]) #discarding Y peak and valley
                i=i-3 #case to reducing s lenght of 2, but not reread (see position of i increment)
    for i in range (1,len(s)):
        cycles.append([abs(s[i]-s[i-1]),0.5,(s[i]+s[i-1])/2])
    return cycles
    
    
def peakValley(s):
    """
    PeakValley counting method
    According to the algorithm described in appunti di costruzione di macchine
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
    print (pv)
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