# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 15:18:42 2016

@author: mastraa

last update: 
"""

Counting Method available:
Rainflow or pagoda roof
Simply Rainflow: the same of Rainflow to use for repetitive load story
Peak Valley: it combines highest peak and lowest valley (remained) to set a cycle range, delete the point at every iteration
Simple Range: calculate as a range every side of the reversed spectrum

More details:
ASTM E1049-85 (2005)
"Appunti di costruzioni di macchine", prof.Bruno Atzori


Database data:
for R value:
if one row is valid for more than one R value you have two row with the first and the last R
for R<-1 you see a row for R=-1 and one for R=-99
infinite it's like 99/-99

R finding:
If wanted R is not available in group there are two case (R_method and interpolation):
there is a group with casual R so we consider that sa-sm curve is rect, we find m and q,
the second point to obtain the rect is (sR,0). We find the intersection (sm,sa)*.
the other method interpolate the nearest group with lower and higher R to obtain (sm,sa)*.
When we know * point we have smax* that is assumed to be egual to smax=sm+sa with sm of our block.

Interpolation method seems to be the best way, but sometimes a group with higher sm has an higher fatigue ratio and the slope of the Haigh modified curve become positive. We suggest to check the groups before deciding.


GUI features

Load Data Page:

File setting area:
Users can set the extension of the file, open a file (at the moment only xlsx are available)
Once file is opened users can choose the page and set the column in which loads are stored and even the presence of header
First column is 1
At the moment users must use header also to avoid the reading of the firsts rows

Counting method area:
Users can choose counting method
You can choose also if pack datas with similar value, input value are the dimension of the interval in which you pack datas.
Radio button let you choose if the value of packed data to use in the analysis will be the median value of the group or the max value. Suggest to to use median if you know that the main groups are numerous.
If you don’t know or you have little group you may use max value in emergency advance. 

View Data area:
Users can create a story giving a name to it
The lower limit is not available (see header instructions)
Max limit is the number of the row that will be considered
Many stories could be created and stored in the program
Below you can also delete stories

Users can also save all stories created to a file
file name and extension could be set, page name will be the story name
At the moment only xlsx file are available

You can plot datas, at the moment it will only show extreme values plot

Material Data Page:

You can choose from all kind of fiber in the top combobox
Search button show in the table below the list of material saved with that kind of fiber

Save Selected Material Button saves the material you selected in the table, now
that item will be available in Analysis page

Adding new materials:???
Name and id must be unique, id is auto assigned, name is not. In case of egual
name the query will be ignored.

Analysis page:
In this page the user will choose material and load story to use.
When you choose material in the box on the top you have to search for groups, groups will be shown on the table below.
If R is different from any group you can approximate it in two ways:
interpolation between the two nearest values
using a sort of Haigh diagram
we suggest to use the second one if you have only one group for that material.
The first one raise an error if you are out of the range of R group.
Below you must choose the load story to analyze and you can start analysis.


Log Monitor:
It shows users actions: saving, creation, deleting, errors