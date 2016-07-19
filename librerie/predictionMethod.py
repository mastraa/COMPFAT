# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016
"""

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