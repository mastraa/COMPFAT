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

def genHaigh(_sR, _R, _sa, sm):
    """
    Haigh diagrama method starting from any R value
    sm = median value of applicated load
    _* values are database data
    in case of sm<0 give compressive sR
    """
    _sm=(1+_R)/2*_sa #median value of database data
    m,q=rect2([0,_sa],[_sm,_sR])
    return q+m*sm

def interpolationR():
    """
    Interpolated curve with 3 or more group values
    TODO: study the method
    """
    pass

def miner(_sR, _sa, sa, Nf):
    """
    miner damaging method
    _sa = database or haigh output amplitude for incipient collpase
    sa = applied amplitude
    """
    m,q=rect2([0,log10(_sR)],[log10(2*10**6),log10(_sa)])
    Nmax=10**(xRect(log10(sa),m,q))
    return Nf/Nmax

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