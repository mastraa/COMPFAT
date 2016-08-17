# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:58:33 2016

@author: mastraa
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fdialog
import tkinter.scrolledtext as ScrolledText
import pyqtgraph as pg
import time
import matGui, database, analysis

from openpyxl import load_workbook

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
        self.loadStored={}
        self.matStored={}
        
        master = ttk.Frame(self, name='master') # create Frame in self
        master.pack(fill=tk.BOTH) # fill both sides of the parent
          
        noteBook = ttk.Notebook(master)
        p1 = ttk.Frame(noteBook)    #Load data page
        p2 = ttk.Frame(noteBook)    #Material Data Page
        p3 = ttk.Frame(noteBook)    #Analysis Page
        noteBook.add(p1, text='Load Data')
        noteBook.add(p2, text='Material Data')
        noteBook.add(p3, text='Analysis')
        noteBook.grid(column=0, row=0)
        #noteBook.pack(padx=2, pady=3) # fill "master" but pad sides
        ttk.Label(master, text="Log Monitor").grid(column=0, row=1)
        self.logError=ScrolledText.ScrolledText(master, width=100, height=15)
        self.logError.grid(row=2,column=0)
          
        
        """ Load Setting Page """
        #create and locate the frame
        sec1=ttk.LabelFrame(p1,text="File setting")
        sec1.grid(column=0,row=0,sticky='W', padx=10, pady=10)
        #create all labels
        ttk.Label(sec1,text="type").grid(column=0,row=0)
        ttk.Label(sec1,text="url").grid(column=0,row=1)
        ttk.Label(sec1,text="page name").grid(column=0,row=2)
        ttk.Label(sec1,text="column number").grid(column=0,row=3)
        ttk.Label(sec1,text="header").grid(column=0,row=4)
        #initialize all tkvariables
        self.fileType = tk.StringVar()
        self.pageName = tk.StringVar()
        self.column=tk.StringVar()
        self.header=tk.StringVar()
        #widgets
        self.typeChoosen = ttk.Combobox(sec1, width=12, textvariable=self.fileType, state='readonly')#choose file type
        self.typeChoosen.grid(column=1, row=0)
        self.typeChoosen['values']=('.xlsx')#now only xlsx available
        self.typeChoosen.current(0)
        self.openBtn=ttk.Button(sec1,text='Open File', command=self.openFile)#open file button
        self.openBtn.grid(column=1,row=1)
        self.pageChoosen = ttk.Combobox(sec1, width=12, textvariable=self.pageName, state='readonly')#choose file page to read
        self.pageChoosen.grid(column=1, row=2)
        ttk.Entry(sec1, textvariable=self.column, width=5).grid(column=1, row=3)
        ttk.Entry(sec1, textvariable=self.header, width=5).grid(column=1, row=4)
        
        
        sec2=ttk.LabelFrame(p1,text="Counting Method")
        sec2.grid(column=0,row=1,sticky='W', padx=10, pady=10)
        ttk.Label(sec2,text="method").grid(column=0,row=0)
        ttk.Label(sec2,text="delta").grid(column=0,row=1)
        self.method = tk.StringVar()
        self.methodChoosen = ttk.Combobox(sec2, width=20, textvariable=self.method, state='readonly')
        self.methodChoosen.grid(column=1, row=0)
        self.methodChoosen['values']=('Rainflow','Simply Rainflow','Peak Valley','Simple Range')
        self.methodChoosen.current(0)
        
          
        plotter=ttk.LabelFrame(p1,text="View data")
        plotter.grid(column=1,row=0,rowspan=2, sticky='NW', padx=10, pady=10)
        ttk.Label(plotter,text="story name").grid(column=0,row=0)
        ttk.Label(plotter,text="lower limit").grid(column=0,row=1)
        ttk.Label(plotter,text="max limit").grid(column=2,row=1)
        ttk.Label(plotter,text="File Name").grid(column=0,row=3)
        ttk.Label(plotter,text="Delete Story").grid(column=0,row=6)
        self.storyName=tk.StringVar()
        self.lowLim=tk.StringVar()#disabled, to use set header
        self.maxLim=tk.StringVar()
        self.saveFile=tk.StringVar()
        self.saveType=tk.StringVar()
        self.st2Delete=tk.StringVar()
        ttk.Entry(plotter, textvariable=self.storyName).grid(column=1, row=0)
        ttk.Entry(plotter, textvariable=self.lowLim, state='disabled').grid(column=1, row=1)
        ttk.Entry(plotter, textvariable=self.maxLim).grid(column=3, row=1)
        ttk.Button(plotter, text="Create Story", command=self.createStory).grid(column=1,row=2)
        ttk.Entry(plotter, textvariable=self.saveFile).grid(column=1, row=3)
        self.saveChoosen = ttk.Combobox(plotter, width=6, textvariable=self.saveType, state='readonly')#choose file type
        self.saveChoosen.grid(column=2, row=3)
        self.saveChoosen['values']=('.xlsx')#now only xlsx available
        self.saveChoosen.current(0)
        ttk.Button(plotter, text="Save", command=self.saveStory).grid(column=1,row=4)
        self.deleteStory = ttk.Combobox(plotter, width=15, textvariable=self.st2Delete, state='readonly')#choose file type
        self.deleteStory.grid(column=1,row=6)
        ttk.Button(plotter, text="Delete", command=self.deleteStory).grid(column=2,row=6)

        """Material data page"""
        self.material=tk.StringVar()    #type of fiber
        
        mat=ttk.LabelFrame(p2,text="Material")
        mat.grid(column=0,row=0,sticky='W', padx=10, pady=10)
        
        lista=database.searchField('matLib','fiber')
        self.matChoosen = ttk.Combobox(mat, width=12, textvariable=self.material, state='readonly')
        self.matChoosen.grid(column=0, row=0)
        self.matChoosen['values']=lista
        ttk.Button(mat,text="Search", command=self.searchMat).grid(row=0,column=1)
        
        self.tree=ttk.Treeview(mat,selectmode="extended",columns=('1','2','3','4','5'))
        self.tree.heading("#0", text=" ")
        self.tree.column("#0",minwidth=0,width=1)        
        self.tree.heading("#1", text="Id")
        self.tree.column("#1",minwidth=0,width=30)
        self.tree.heading("#2", text="Name")
        self.tree.column("#2",minwidth=0,width=200)
        self.tree.heading("#3", text="Fibre")
        self.tree.column("#3",minwidth=0,width=80)
        self.tree.heading("#4", text="Matrix")
        self.tree.column("#4",minwidth=0,width=50)
        self.tree.heading("#5", text="R [MPa]")
        self.tree.column("#5",minwidth=0,width=100)
        self.tree.grid(column=0, columnspan=4, row=2)
        
        
        ttk.Button(mat,text="Save Selected Material", command=self.saveMat).grid(row=3,column=2)        
        
        
        
        """Analysis page"""
        self.matAnal=tk.StringVar()#material selected for analysis
        self.behaviour=tk.StringVar()
        self.architecture=tk.StringVar()
        self.Rmethod=tk.StringVar()
        
        beh=ttk.LabelFrame(p3,text="Analysis Setting")
        beh.grid(column=0,row=1,sticky='W', padx=10, pady=10)
        ttk.Label(beh,text="Material").grid(column=0,row=0)
        self.matSet = ttk.Combobox(beh, width=20, textvariable=self.matAnal, state='readonly')#choose file type
        self.matSet.grid(column=1, row=0)
        ttk.Label(beh,text="Behaviour").grid(column=3,row=0)
        self.behSet = ttk.Combobox(beh, width=5, textvariable=self.behaviour, state='readonly')#choose file type
        self.behSet.grid(column=4, row=0)
        self.behSet['values']=['FD','MD']
        self.archSet = ttk.Combobox(beh, width=5, textvariable=self.architecture, state='readonly')#choose file type
        self.archSet.grid(column=5, row=0)
        self.archSet['values']=['UD','W']
        ttk.Button(beh,text="Show Group", command=self.showGroup).grid(row=0,column=6)
        ttk.Label(beh,text="R method").grid(column=7,row=0)
        self.archSet = ttk.Combobox(beh, width=5, textvariable=self.architecture, state='readonly')#choose file type
        self.archSet.grid(column=8, row=0)
        self.archSet['values']=['Haigh','Interpolate']
                
        
        self.groupTree=ttk.Treeview(beh,selectmode="extended",columns=('1','2','3','4','5','6','7','8','9','10'))
        self.groupTree.heading("#0", text=" ")
        self.groupTree.column("#0",minwidth=0,width=1)
        self.groupTree.heading("#1", text="Group N")
        self.groupTree.column("#1",minwidth=0,width=50)
        self.groupTree.heading("#2", text="Fibre")
        self.groupTree.column("#2",minwidth=0,width=75)
        self.groupTree.heading("#3", text="Matrix")
        self.groupTree.column("#3",minwidth=0,width=50)
        self.groupTree.heading("#4", text="Behav.")
        self.groupTree.column("#4",minwidth=0,width=50)
        self.groupTree.heading("#5", text="Arch")
        self.groupTree.column("#5",minwidth=0,width=50)
        self.groupTree.heading("#6", text="50%")
        self.groupTree.column("#6",minwidth=0,width=50)
        self.groupTree.heading("#7", text="90%")
        self.groupTree.column("#7",minwidth=0,width=50)
        self.groupTree.heading("#8", text="T_s")
        self.groupTree.column("#8",minwidth=0,width=50)
        self.groupTree.heading("#9", text="Quality")
        self.groupTree.column("#9",minwidth=0,width=100)
        self.groupTree.heading("#10", text="R")
        self.groupTree.column("#10",minwidth=0,width=20)
        self.groupTree.grid(column=0, columnspan=6, row=2)
        
        
    def openFile(self):
        """
        Open file with given extension and save the file name
        TODO: generalized to open also dat files
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
        """
        newStory = analysis.loadStory(self.fileName, int(self.header.get()), fileType=str(self.fileType.get()), sheet=self.pageName.get(), column=int(self.column.get()), limit=int(self.maxLim.get()))  
        nSname =str(self.storyName.get())       
        self.loadStored[nSname] = newStory   
        self.loadStored[nSname].counting(cMethod=str(self.method.get())) #range counting
        string=time.strftime("%H:%M:%S")+" "+nSname+" strory created"
        self.logError.insert(tk.INSERT,string+"\n")
        self.deleteStory['values']=list(self.loadStored.keys()) #update deleteStory Combobox
        
        
    def saveStory(self):
        """
        Save all story to file
        the page name will be the story name
        """
        for key in self.loadStored:
            self.loadStored[key].save('data/'+str(self.saveFile.get())+str(self.saveType.get()), key)
            string=time.strftime("%H:%M:%S")+" "+key+" strory saved to "+"data/"+str(self.saveFile.get())+str(self.saveType.get())
            self.logError.insert(tk.INSERT,string+"\n")
        
    def deleteStory(self):
        """
        delete story stored in loadStored
        """
        key = self.st2Delete.get()
        del self.loadStored[key]
        self.deleteStory['values']=list(self.loadStored.keys()) #update deleteStory Combobox
        string=time.strftime("%H:%M:%S")+" "+key+" strory deleted"
        self.logError.insert(tk.INSERT,string+"\n")
        
    def saveMat(self):
        """
        get material from list and create a material class saved in a dict
        """
        for item in self.tree.selection():
            values = self.tree.item(item, 'values')
            self.matStored[values[1]]=analysis.matList(values[0], values[1], values[4], values[3], values[2])
            self.matSet['values']=list(self.matStored.keys())
            string=time.strftime("%H:%M:%S")+" "+values[1]+" material saved"
            self.logError.insert(tk.INSERT,string+"\n")
    
    def searchMat(self):
        """
        clear table and
        search materials from database using fibre as field
        """
        for i in self.tree.get_children():
            self.tree.delete(i)
        materiale=str(self.material.get())
        for item in database.searchAll('matLib','fiber',materiale):
            self.tree.insert('','end',values=(item[0],item[4],item[1],item[2], item[3]))
            
    def showGroup(self):
        """
        search the groups with the given characteristics
        and show it in the table
        """
        arch=str(self.architecture.get())
        beh=str(self.behaviour.get())
        name=str(self.matAnal.get())
        fiber=str(self.matStored[name].fiber)
        matrix=str(self.matStored[name].matrix)
        groups=database.searchAllGroups(fiber, matrix, beh, arch)
        for item in groups:
            self.groupTree.insert('','end',values=(item[1],item[3],item[4],item[5],item[6],item[7],item[8],item[9],'qualità',item[2]))
        
        
          
