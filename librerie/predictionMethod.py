# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 17/11/2016

"""
from math import log10

def haigh(_sa,_sR, sm):
    """
    Haigh diagram method starting from R=-1
    """
    return _sa*(1-sm/_sR)
    
def Rmethod(_sR, _R, _smax, R, sa):
    """
    From a group with any _R value it creates the _sm,_sa curve
    it search the intersection with the rect with real R value
    from intersection get the smax=_sm+_sa
    from smax it deduce sa_amm knowing real sm: sa_amm=smax-sm
    sm = median value of applicated load
    _*: values are database data
    in case of sm<0 give compressive sR
    """
    if -1<=R<1:
        _sm=_smax*(1+_R)/2 #median value of database data
        _sRx=_sR
    else:#_smax is real _smin!
        _smax=-_smax
        _sm=_smax/2*(1/_R+1)#we want negative _sm in the left side of Haigh diagram
        _sRx=-_sR#left side diagram
    _sa=abs(_smax-_sm)
    m,q=rect2([_sm,_sa],[_sRx,0])#haigh curve, _sRx needed to be in the right side of the diagram
    
    #print(_R, _smax, _sm, _sa, m, q)    
    
    _sa=q*_sR/(_sR+abs(q*(1+R)/(1-R)))#intersection of Haigh and R curve
    #abs are needed in case of sm<0!
    _sm=xRect(_sa,m,q)#sm corrisp to the amplitude of intersection


    result=abs(_sm)+_sa
    return result

def interpolationR(p1,p2,R):
    """
    Interpolation of the rect beetween major and minor nearest values
    """
    m,q=rect2(p1,p2)#haigh curve
    _sm=q/((1-R)/(1+R)-m)#intersection sm, rect intersection formula
    #(we don't use *FORMULA of R_method because it may not pass in (sR,0)).
    _sa=(1-R)/(1+R)*_sm #intersection sa
    #print(p1,p2,m,q)
    result=_sm+_sa#_sm+_sa=_smax2E6
    return result

def miner(_sR, _smax90, smax, N):
    """
    miner damaging method
    _sa = database or haigh output amplitude for incipient collpase
    sa = applied amplitude
    """
    if _smax90<0:#sm is higher than the max value for sigma
        D=1.1
    else:
        m,q=rect2([0,log10(_sR)],[log10(2*10**6),log10(_smax90)])
        Nmax=10**(xRect(log10(smax),m,q))
        D=N/Nmax
        #print(m,q,Nmax)
    return D,m

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
    
def HaighPoints(sm, R, sext):
    """
    automatically detect the side of diagram
    return [sm,sa] of haigh diagram
    sext=s estreme (max or min) calculated as sR*phi 
    """
    if sm>=0:
        _sm=sext/2*(1+R)
        _sa=sext/2*(1-R)
    else:
        """era...secondo me errato...
        _sm=sext/2*(1+1/R)
        _sa=sext/2*(1/R-1)
        """
        _sa=sext/2
        _sm=_sa*((1+R)/(1-R))
        #print((1+R)/(1-R), _sm, _sa)
    return[_sm,_sa]