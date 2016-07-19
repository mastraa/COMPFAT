# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016

File manipolation library
"""

from openpyxl import load_workbook
import matplotlib.pyplot as plt
#from openpyxl.worksheet.read_only import ReadOnlyWorksheet



def readF(nameFile):
    wb = load_workbook(filename = 'data/spettro.xlsx', read_only=True)
    sheet_ranges = wb['Carichi']
    rows=sheet_ranges.rows
    time=[]
    f=[]
    for item in rows:
        time.append(item[0].value)
        f.append(item[1].value)
    return f[1:]



