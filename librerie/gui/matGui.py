# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:58:33 2016

@author: mastraa
"""


import matplotlib.pyplot as plt


def scatter(points,legend=["Groups","sa/sR","sm/sR"]):
    """
    plot a scatter graph with a label per point
    points=[x,y,label]
    legend=[title,ylabel,xlabel]
    """
    fig = plt.figure(legend[0])
    fig.suptitle(legend[0], fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    
    fig.subplots_adjust(top=0.85)
    ax.set_ylabel(legend[1])
    ax.set_xlabel(legend[2])


    ax.plot(points[0],points[1], 'ro')
    for i in range(len(points[0])):
        if points[1][i]>0.8:
            y=-20
        else:
            y=20
        ax.annotate('(%s)' %points[2][i], xy=(points[0][i],points[1][i]), xytext=(0,y), textcoords='offset points')
    ax.axis([-1.05,1.05,-0.05,1.05])
    ax.plot([-1,0,1],[0,1,0])
    fig.show()

