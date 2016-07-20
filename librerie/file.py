# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016

File manipolation library
"""

from openpyxl import load_workbook, Workbook
import matplotlib.pyplot as plt
from decimal import *
#from openpyxl.worksheet.read_only import ReadOnlyWorksheet



def readF(nameFile):
    """
    Read values from excel 2010 files
    """
    wb = load_workbook(filename = nameFile, read_only=True)
    sheet_ranges = wb['Carichi']
    rows=sheet_ranges.rows
    time=[]
    f=[]
    for item in rows:
        time.append(item[0].value)
        f.append(item[1].value)
    return f[1:]
    
def writeFile(nameFile, h, sheetName="Foglio1"):
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

