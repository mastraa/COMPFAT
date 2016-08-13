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


GUI features

File setting area:
Users can set the extension of the file, open a file (at the moment only xlsx are available)
Once file is opened users can choose the page and set the column in which loads are stored and
even the presence of header
Remember column A is number 0, B-1...
At the moment users must use header also to avoid the reading of the firsts rows

Counting method area:
Users can choose counting method

View Data area:
Users can create a story giving a name to it
The lower limit is not available (see header istructions)
Max limit is the number of the row that will be considered
Many stories could be created and stored in the program
(at the moment you can't delete them)

Users can also save all stories created to a file
file name and extension could be setted, page name will be the story name
At the moment only xlsx file are available

Below the widget to delete a story, select the story name set before and click DELETE


Log Monitor:
It shows users actions