# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016

File manipolation library
"""

import os
from openpyxl import load_workbook, Workbook
from decimal import *
#from openpyxl.worksheet.read_only import ReadOnlyWorksheet



def readXls(nameFile, sheet, column, header, limit=None):
    """
    Read values from excel 2010 files column
    """
    a=[]
    wb = load_workbook(filename = nameFile, read_only=True, data_only=True)
    #data_only to read current values of cells and not formulas
    sheet_ranges = wb[sheet]
    
    if limit and limit <=1000:#more than 1000 too slow!!!
        for i in range(header+1,header+limit):
            a.append(float(sheet_ranges.cell(row = i, column = column).value))
            #the first cell with cell is 1-1
    else:
        f=sheet_ranges.columns[column-1]#the first cell with columns is 0-0
        for i in range (len(f)-header):
            a.append(f[i+header].value)
        if limit:
            a=a[:limit]
    return a
    
def writeXls(nameFile, h, sheetName="Foglio1"):
    """
    Write h values to excel file
    now it will overwrite an already existing file
    TODO: generalize function
    """
    if fileExist(nameFile):
        wb=load_workbook(filename=nameFile)#load file
    else:
        wb=Workbook()#create new workbook
    ws = wb.create_sheet(title=sheetName)#create new sheet
    ws['A1']="range"
    ws['B1']="cycles"
    ws['C1']="mean"
    ws['D1']="sigma_max"
    ws['E1']="sigma_min"
    ws['F1']="R"
    i=2
    for item in h:
        for value in item[1]:
            ws['A'+str(i)]=item[0]#range
            ws['B'+str(i)]=value[0]#cycles
            ws['C'+str(i)]=value[1]#mean
            s_max=value[1]+item[0]/2
            s_min=value[1]-item[0]/2
            ws['D'+str(i)]=s_max#s_max
            ws['E'+str(i)]=s_min#s_min
            ws['F'+str(i)]=value[2]#R
            i=i+1
    wb.save(nameFile)#save file
    
    
def fileExist(file):
    """
    check if file already exists
    INPUT: file path+name
    OUTPUT: true if exists or false if not
    """
    return os.path.isfile(file)

