# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:58:33 2016

@author: mastraa
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fdialog
import pyqtgraph as pg
import analysis

from openpyxl import load_workbook, Workbook

def prova(x,y, btn):
    pg.plot(x, y, pen='r')
    print(btn)

class MainWindow(tk.Tk):
    """
    """
    def __init__(self, title, size):
        tk.Tk.__init__(self)
        self.title(title)
        self.geometry(size)#x,y
        self.resizable(0,0)
        self.configure(background="gray89")
        
        master = ttk.Frame(self, name='master') # create Frame in self
        master.pack(fill=tk.BOTH) # fill both sides of the parent
          
        noteBook = ttk.Notebook(master)
        p1 = ttk.Frame(noteBook)    #Load data page
        p2 = ttk.Frame(noteBook)    #Material Data Page
        p3 = ttk.Frame(noteBook)    #Analysis Page
        noteBook.add(p1, text='Load Data')
        noteBook.add(p2, text='Material Data')
        noteBook.add(p3, text='Analysis')
        noteBook.pack(fill=tk.BOTH, padx=2, pady=3) # fill "master" but pad sides
          
        
        """ Load Setting Page """
        
        sec1=ttk.LabelFrame(p1,text="File setting")
        sec1.grid(column=0,row=0,sticky='W', padx=10, pady=10)
        ttk.Label(sec1,text="type").grid(column=0,row=0)
        ttk.Label(sec1,text="url").grid(column=0,row=1)
        ttk.Label(sec1,text="page name").grid(column=0,row=2)
        ttk.Label(sec1,text="column number").grid(column=0,row=3)
        ttk.Label(sec1,text="header").grid(column=0,row=4)
        self.fileType = tk.StringVar()
        self.pageName = tk.StringVar()
        self.column=tk.StringVar()
        self.header=tk.StringVar()
        self.typeChoosen = ttk.Combobox(sec1, width=12, textvariable=self.fileType, state='readonly')
        self.typeChoosen.grid(column=1, row=0)
        self.typeChoosen['values']=('.xlsx','.dat')
        self.typeChoosen.current(1)
        self.openBtn=ttk.Button(sec1,text='Open File', command=self.openFile)
        self.openBtn.grid(column=1,row=1)
        self.pageChoosen = ttk.Combobox(sec1, width=12, textvariable=self.pageName, state='readonly')
        self.pageChoosen.grid(column=1, row=2)
        ttk.Entry(sec1, textvariable=self.column).grid(column=1, row=3)
        ttk.Entry(sec1, textvariable=self.header).grid(column=1, row=4)
        
        
        sec2=ttk.LabelFrame(p1,text="Counting Method")
        sec2.grid(column=0,row=1,sticky='W', padx=10, pady=10)
        ttk.Label(sec2,text="method").grid(column=0,row=0)
        ttk.Label(sec2,text="delta").grid(column=0,row=1)
        self.method = tk.StringVar()
        self.methodChoosen = ttk.Combobox(sec2, width=12, textvariable=self.method, state='readonly')
        self.methodChoosen.grid(column=1, row=0)
        self.methodChoosen['values']=('Rainflow','Simply Rainflow','Peak Valley','Simple Range')
        self.methodChoosen.current(1)
        
          
        plotter=ttk.LabelFrame(p1,text="View data")
        plotter.grid(column=1,row=0,rowspan=2, sticky='NW', padx=10, pady=10)
        ttk.Label(plotter,text="story name").grid(column=0,row=0)
        self.storyName=tk.StringVar()
        ttk.Entry(plotter, textvariable=self.storyName).grid(column=1, row=0)
        ttk.Button(plotter, text="Create Story", command=self.createStory).grid(column=1,row=1)
        
        
    def openFile(self):
        """
        Open file with given extension and save the file name
        """
        fileOpt={}
        fileOpt['initialdir']='data'
        fileOpt['filetypes']=[('all files',self.fileType.get())]
        fileOpt['parent']=self
        fileOpt['title']='Load spectrum file'
        self.fileName=fdialog.askopenfilename(**fileOpt)
        pages = load_workbook(filename = self.fileName, read_only=True).get_sheet_names()
        self.pageChoosen['values']=pages
            
        
    def createStory(self):
        """
        add load story to the list
        at the momento it will count with rainflow and save data to default file
        
        TODO: choose file and sheet name 
        """
        self.loads.append(analysis.loadStory(self.fileName, int(self.header.get()), fileType=str(self.fileType.get()), sheet=self.pageName.get(), column=int(self.column.get())))  
        analysis.loadStory.counting()
        analysis.loadStory.save('data/prova.xlsx', 'result_1')
        
        """Material data page"""
          
          
        """Analysis page"""
          
