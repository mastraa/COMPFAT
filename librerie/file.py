# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016

File manipolation library
"""

from openpyxl import load_workbook, Workbook
from decimal import *
#from openpyxl.worksheet.read_only import ReadOnlyWorksheet



def readXls(nameFile, sheet, column, header):
    """
    Read values from excel 2010 files column
    """
    a=[]
    wb = load_workbook(filename = nameFile, read_only=True)
    sheet_ranges = wb[sheet]
    f=sheet_ranges.columns[column]
    for i in range (len(f)-header):
        a.append(f[i+header].value)
    return a
    
def writeXls(nameFile, h, sheetName="Foglio1"):
    """
    Write h values to excel file
    now it will overwrite an already existing file
    TODO: generalize function
    """
    wb = Workbook()
    ws = wb.create_sheet(title=sheetName)
    ws['A1']="range"
    ws['B1']="cycles"
    ws['C1']="mean"
    i=2
    for item in h:
        ws['A'+str(i)]=item[0]
        for value in item[1]:
            ws['B'+str(i)]=value[0]
            ws['C'+str(i)]=value[1]
            i=i+1
    wb.save(nameFile) 

