# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:58:33 2016

@author: mastraa

Last update 13/09/2016
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fdialog
from tkinter import messagebox as msg
import tkinter.scrolledtext as ScrolledText
#import pyqtgraph as pg
import time
import database, analysis
import countingMethod as cm

from openpyxl import load_workbook


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
        self.newMatWin=0
        
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
        self.deltaR=tk.DoubleVar()#range interval for packing, null=no packing
        self.deltaM=tk.DoubleVar()#median interval for packing, null=no packing
        self.blockLevel=tk.IntVar()
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
        ttk.Label(sec2,text="delta Range").grid(column=0,row=1)
        ttk.Label(sec2,text="delta Medium").grid(column=0,row=2)
        self.method = tk.StringVar()
        self.methodChoosen = ttk.Combobox(sec2, width=20, textvariable=self.method, state='readonly')
        self.methodChoosen.grid(column=1, row=0)
        self.methodChoosen['values']=('Rainflow','Simply Rainflow','Peak Valley','Simple Range')
        self.methodChoosen.current(0)
        ttk.Entry(sec2, textvariable=self.deltaR, width=5).grid(column=1, row=1)
        ttk.Entry(sec2, textvariable=self.deltaM, width=5).grid(column=1, row=2)
        ttk.Radiobutton(sec2, text="Median Value", variable=self.blockLevel, value=1).grid(column=0, row=3)
        ttk.Radiobutton(sec2, text="Max Value", variable=self.blockLevel, value=2).grid(column=1, row=3)
        self.blockLevel.set(1)#set default radio
        
          
        plotter=ttk.LabelFrame(p1,text="View data")
        plotter.grid(column=1,row=0,rowspan=2, sticky='NW', padx=10, pady=10)
        ttk.Label(plotter,text="story name").grid(column=0,row=0)
        ttk.Label(plotter,text="max limit").grid(column=0,row=1)
        ttk.Label(plotter,text="File Name").grid(column=0,row=3)
        
        self.storyName=tk.StringVar()
        self.maxLim=tk.StringVar()
        self.saveFile=tk.StringVar()
        self.saveType=tk.StringVar()
        self.st2Delete=tk.StringVar()
        self.st2Plot=tk.StringVar()
        ttk.Entry(plotter, textvariable=self.storyName).grid(column=1, row=0)
        ttk.Entry(plotter, textvariable=self.maxLim).grid(column=1, row=1)
        ttk.Button(plotter, text="Create Story", command=self.createStory).grid(column=1,row=2)
        ttk.Entry(plotter, textvariable=self.saveFile).grid(column=1, row=3)
        self.saveChoosen = ttk.Combobox(plotter, width=6, textvariable=self.saveType, state='readonly')#choose file type
        self.saveChoosen.grid(column=2, row=3)
        self.saveChoosen['values']=('.xlsx')#now only xlsx available
        self.saveChoosen.current(0)
        ttk.Button(plotter, text="Save", command=self.saveStory).grid(column=1,row=4)
        ttk.Label(plotter,text="Delete Story").grid(column=0,row=6)        
        self.deleteStory = ttk.Combobox(plotter, width=15, textvariable=self.st2Delete, state='readonly')#choose file type
        self.deleteStory.grid(column=1,row=6)
        ttk.Button(plotter, text="Delete", command=self.deleteStory).grid(column=2,row=6)
        ttk.Label(plotter,text="Plot Story").grid(column=0,row=7)
        self.toPlotStory = ttk.Combobox(plotter, width=15, textvariable=self.st2Plot, state='readonly')#choose file type
        self.toPlotStory.grid(column=1,row=7)
        ttk.Button(plotter, text="Plot", command=self.plotStory).grid(column=2,row=7)

        """Material data page"""
        self.material=tk.StringVar()    #type of fiber
        
        mat=ttk.LabelFrame(p2,text="Material")
        mat.grid(column=0,row=0,sticky='W', padx=10, pady=10)
        
        lista=database.searchField('matLib','fiber')
        self.matChoosen = ttk.Combobox(mat, width=12, textvariable=self.material, state='readonly')
        self.matChoosen.grid(column=0, row=0)
        self.matChoosen['values']=lista
        ttk.Button(mat,text="Search", command=self.searchMat).grid(row=0,column=1)
        ttk.Button(mat,text="New Matetial", command=self.newMat).grid(row=0,column=2)
        
        self.tree=ttk.Treeview(mat,selectmode="extended",columns=('1','2','3','4','5','6','7'))
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
        self.tree.heading("#5", text="Rt [MPa]")
        self.tree.column("#5",minwidth=0,width=75)
        self.tree.heading("#6", text="Rc [MPa]")
        self.tree.column("#6",minwidth=0,width=75)
        self.tree.heading("#7", text="Note")
        self.tree.column("#7",minwidth=0,width=200)
        self.tree.grid(column=0, columnspan=4, row=2)
        
        
        ttk.Button(mat,text="Save Selected Material", command=self.saveMat).grid(row=3,column=2)        
        
        
        
        """Analysis page"""
        self.matAnal=tk.StringVar()#material selected for analysis
        self.behaviour=tk.StringVar()
        self.architecture=tk.StringVar()
        self.Rmethod=tk.StringVar()
        self.dataList=[]#list of all groups of selected materials to pass to analize function
        self.st2Anal=tk.StringVar()
        self.percent=tk.StringVar()#50-90%
        
        beh=ttk.LabelFrame(p3,text="Analysis Setting")
        beh.grid(column=0,row=1,sticky='W', padx=10, pady=10)
        ttk.Label(beh,text="Mat.").grid(column=0,row=0)
        self.matSet = ttk.Combobox(beh, width=20, textvariable=self.matAnal, state='readonly')
        self.matSet.grid(column=1, row=0)
        ttk.Label(beh,text="Beh.").grid(column=2,row=0)
        self.behSet = ttk.Combobox(beh, width=5, textvariable=self.behaviour, state='readonly')
        self.behSet.grid(column=3, row=0)
        self.behSet['values']=['FD','MD']
        ttk.Label(beh,text="Arch.").grid(column=4,row=0)
        self.archSet = ttk.Combobox(beh, width=5, textvariable=self.architecture, state='readonly')
        self.archSet.grid(column=5, row=0)
        self.archSet['values']=['UD','W']
        ttk.Label(beh,text="%").grid(column=6,row=0)
        self.perSet = ttk.Combobox(beh, width=5, textvariable=self.percent, state='readonly')
        self.perSet.grid(column=7, row=0)
        self.perSet['values']=['50','90']
        ttk.Button(beh,text="Show Group", command=self.showGroup).grid(row=0,column=8)
        ttk.Label(beh,text="Amp. stimation").grid(column=9,row=0)
        self.RmethodSet = ttk.Combobox(beh, width=8, textvariable=self.Rmethod, state='readonly')
        self.RmethodSet.grid(column=10, row=0)
        self.RmethodSet['values']=['Interpol','R_method'] #interpolation method will be available soon
        
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
        self.groupTree.column("#10",minwidth=0,width=30)
        self.groupTree.grid(column=0, columnspan=6, row=2)
        
        ttk.Label(beh,text="Story").grid(column=0,row=3)
        self.analStory = ttk.Combobox(beh, width=15, textvariable=self.st2Anal, state='readonly')#choose file type
        self.analStory.grid(column=1,row=3)
        ttk.Button(beh,text="Analize", command=self.analize).grid(row=3,column=2)
        
        
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
        create load story and add it to the list
        now it saves data to default file
        """       
        try:
            newStory = analysis.loadStory(self.fileName, int(self.header.get()), fileType=str(self.fileType.get()), sheet=self.pageName.get(), column=int(self.column.get()), limit=int(self.maxLim.get()))  
            if newStory.Error:
                string=newStory.errorsCheck(time.strftime("%H:%M:%S"))
            else:
                nSname =str(self.storyName.get())       
                self.loadStored[nSname] = newStory   
                self.loadStored[nSname].counting(cMethod=str(self.method.get())) #range counting
                self.loadStored[nSname].packing(self.deltaR.get(), self.deltaM.get(),self.blockLevel.get())
                string=time.strftime("%H:%M:%S")+" "+nSname+" strory created"
                self.deleteStory['values']=list(self.loadStored.keys()) #update deleteStory Combobox
                self.analStory['values']=list(self.loadStored.keys()) #update analStory Combobox
                self.toPlotStory['values']=list(self.loadStored.keys()) #update toPlotStory Combobox
        except ValueError:
            string=time.strftime("%H:%M:%S")+" Error: fill all fields requested"
        self.logError.insert(tk.INSERT,string+"\n")
             
        
    def saveStory(self):
        """
        Save all story to file
        the page name will be the story name
        TODO: insert also parameters!
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
        self.analStory['values']=list(self.loadStored.keys()) #update analStory Combobox
        self.toPlotStory['values']=list(self.loadStored.keys()) #update toPlotStory Combobox
        string=time.strftime("%H:%M:%S")+" "+key+" strory deleted"
        self.logError.insert(tk.INSERT,string+"\n")
        
    def saveMat(self):
        """
        get material from list and create a material class saved in a dict
        """
        for item in self.tree.selection():
            values = self.tree.item(item, 'values')
            self.matStored[values[1]]=analysis.matList(values[0], values[1], values[4], values[3], values[2],values[5])#id,name,sT,matrix type,fiber name,sC
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
            self.tree.insert('','end',values=(item[0],item[1],item[2],item[3], item[4],item[5],item[6]))#id, name, fiber, matrix, Rt, Rc, note
            
    def showGroup(self):
        """
        search the groups with the given characteristics
        and show it in the table
        TODO: in the future possibility to add only some groups in the dataList
        """
        arch=str(self.architecture.get())
        beh=str(self.behaviour.get())
        name=str(self.matAnal.get())
        fiber=str(self.matStored[name].fiber)
        matrix=str(self.matStored[name].matrix)
        groups=database.searchAllGroups(fiber, matrix, beh, arch)
        self.dataList=[]
        for i in self.groupTree.get_children():
            self.groupTree.delete(i)
        for item in groups:
            self.groupTree.insert('','end',values=(item[1],item[3],item[4],item[5],item[6],item[7],item[8],item[9],'qualità',item[2]))
            if self.percent.get()=="50":
                phi=item[7]#50%
            else:
                phi=item[8]#90%
            self.dataList.append([item[2],phi])#R,phi
            
    def analize(self):
        """
        TODO: disconnect damage value from the load story class!
        """
        key = self.st2Anal.get()#get the name of the story selected
        try:
            self.loadStored[key].analize(self.dataList,self.matStored[self.matAnal.get()].sigmaT,self.matStored[self.matAnal.get()].sigmaC, self.Rmethod.get())
            danno=self.loadStored[key].D
            string=time.strftime("%H:%M:%S")+" "+key+"  analized with Miner and "+self.Rmethod.get()+" total damage is: "+str(danno)+"\n"
            string_2="You can repeat this block "+str(danno**-1)+" times."
            string=string+string_2
        
        except (NameError, TypeError):
            string=time.strftime("%H:%M:%S")+"You don't have the necessary groups to use interpolation method"#you have only one group or only group only in one side
        self.logError.insert(tk.INSERT,string+"\n")
        
    def plotStory(self):
        """
        TODO: improve graphical plotting
        """
        key=self.st2Plot.get()
        self.loadStored[key].plot()
          
    def newMat(self):
        """
        Possibility to insert a temporary material
        or add material into database
        """
        if self.newMatWin==1:
            pass
        else:
            self.newMatWin = 1
            matWind(self, "Material data tools","400x200")
            

class matWind(tk.Toplevel):
    """
    """
    def __init__(self, parent, title, size):
        tk.Toplevel.__init__(self, parent)
        self.title(title)
        self.geometry(size)#x,y
        self.resizable(0,0)
        self.parent=parent
        
        self.name=tk.StringVar()
        self.sRt=tk.StringVar()
        self.sRc=tk.StringVar()
        self.fiber=tk.StringVar()
        self.matrix=tk.StringVar()
        
        ttk.Label(self,text="Name").grid(column=0,row=0)
        ttk.Entry(self, textvariable=self.name, width=20).grid(column=1, row=0)
        ttk.Label(self,text="fiber").grid(column=0,row=1)
        ttk.Entry(self, textvariable=self.fiber, width=10).grid(column=1, row=1)
        ttk.Label(self,text="matrix").grid(column=2,row=1)
        self.matrixChoosen = ttk.Combobox(self, width=5, textvariable=self.matrix, state='readonly')
        self.matrixChoosen.grid(column=3, row=1)
        self.matrixChoosen['values']=('TS','TP')
        ttk.Label(self,text="sRt").grid(column=0,row=2)
        ttk.Entry(self, textvariable=self.sRt, width=5).grid(column=1, row=2)
        ttk.Label(self,text="sRc").grid(column=2,row=2)
        ttk.Entry(self, textvariable=self.sRc, width=5).grid(column=3, row=2)
        ttk.Button(self, text="Insert", command=self.insert).grid(column=0,row=3)
        ttk.Button(self, text="Save in DB", command=self.DBsave).grid(column=1,row=3)
        ttk.Button(self, text="Quit", command=self.quitting).grid(column=2,row=3)
        
    def quitting(self):
        """
        Quit from material tools
        """
        self.parent.newMatWin=0
        self.destroy()
        
    def insert(self):
        name=self.name.get()
        fiber=self.fiber.get().lower()
        matrix=self.matrix.get()
        sRt=int(self.sRt.get())
        sRc=int(self.sRc.get())
        self.parent.tree.insert('','end',values=('no ID',name,fiber,matrix,sRt,sRc,' '))#id, name, fiber, matrix, Rt, Rc, note
    
    def DBsave(self):
        msg.showwarning("Disabled", "This functionality hasn't been implemented yet")
        