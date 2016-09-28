# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016

"""
from math import log10

def haigh(_sa,_sR, sm):
    """
    Haigh diagram method starting from R=-1
    """
    return _sa*(1-sm/_sR)

def Rmethod(_sR, _R, _smax, R, sa):
    """
    Haigh diagrama method starting from any R value
    sm = median value of applicated load
    _* values are database data
    in case of sm<0 give compressive sR
    """
    _sm=_smax*(1+_R)/2 #median value of database data
    _sa=_smax-_sm
    m,q=rect2([_sm,_sa],[_sR,0])
    
    sm=(1+R)/(1-R)*sa    
    _sa=q*_sR/(_sR+q*(1+R)/(1-R))#intersection of Haigh and R curve
    _sm=xRect(_sa,m,q)
    result=_sm+_sa-sm
    return result

def interpolationR(p1,p2,R,_sR,sa):
    """
    Interpolation of the rect beetween major and minor nearest values
    """
    m,sa90=rect2(p1,p2)
    sm=(1+R)/(1-R)*sa 
    _sa=sa90*_sR/(_sR+sa90*(1+R)/(1-R))#intersection of Haigh and R curve
    _sm=xRect(_sa,m,sa90)
    result=_sm+_sa-sm
    return result

def miner(_sR, _sa, sa, N):
    """
    miner damaging method
    _sa = database or haigh output amplitude for incipient collpase
    sa = applied amplitude
    """
    if _sa<0:#sm is higher than the max value for sigma
        D=1.1
    else:
        m,q=rect2([0,log10(_sR)],[log10(2*10**6),log10(_sa)])
        Nmax=10**(xRect(log10(sa),m,q))
        D=N/Nmax
    return D

def rect2(p1,p2):
    """
    Rect from two point
    """
    m=(p2[1]-p1[1])/(p2[0]-p1[0])
    q=p1[1]-m*p1[0]
    return m,q

def xRect(y,m,q):
    """
    x value from rect constant and y
    """
    return (y-q)/m