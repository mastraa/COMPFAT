# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:58:33 2016

@author: Andrea Mastrangelo

python3 version

Last update:   02/11/2016
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fdialog
from tkinter import messagebox as msg
import tkinter.scrolledtext as ScrolledText
import time, subprocess, os, sys
import database, analysis
import matGui


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
        self.newMatWin, self.groupChoose=0,0
        self.readme="ReadMe.pdf"
        
        master = ttk.Frame(self, name='master') # create Frame in self
        master.pack(fill=tk.BOTH) # fill both sides of the parent
          
        noteBook = ttk.Notebook(master)
        p1 = ttk.Frame(noteBook)    #Load data page
        p2 = ttk.Frame(noteBook)    #Material Data Page
        p3 = ttk.Frame(noteBook)    #Analysis Page
        noteBook.add(p1, text='Load Data')
        noteBook.add(p2, text='Material Data')
        noteBook.add(p3, text='Analysis')
        noteBook.grid(column=0, row=1, columnspan=6)
        #noteBook.pack(padx=2, pady=3) # fill "master" but pad sides
        ttk.Label(master, text="Log Monitor").grid(column=0, row=2)
        self.logError=ScrolledText.ScrolledText(master, width=100, height=15, state="normal")
        self.logError.grid(row=3,column=0, columnspan=5, rowspan=5)
        self.quitBtn=ttk.Button(master,text='Quit App', command=self.quitApp)#close application
        self.quitBtn.grid(column=5,row=0)
        self.readBtn=ttk.Button(master,text='ReadMe', command=self.openReadme)
        self.readBtn.grid(column=0,row=0)
          
        
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
        self.maxLim=tk.StringVar()
        #widgets
        self.typeChoosen = ttk.Combobox(sec1, width=12, textvariable=self.fileType, state='readonly')#choose file type
        self.typeChoosen.grid(column=1, row=0)
        self.typeChoosen['values']=('.xlsx')#now only xlsx available
        self.typeChoosen.current(0)
        self.openBtn=ttk.Button(sec1,text='Open File', command=self.openFile)#open file button
        self.openBtn.grid(column=1,row=1)
        self.pageChoosen = ttk.Combobox(sec1, width=12, textvariable=self.pageName, state='readonly')#choose file page to read
        self.pageChoosen.grid(column=1, row=2)
        ttk.Entry(sec1, textvariable=self.column, width=10).grid(column=1, row=3)
        ttk.Entry(sec1, textvariable=self.header, width=10).grid(column=1, row=4)
        ttk.Label(sec1,text="max limit").grid(column=0,row=5)
        ttk.Entry(sec1, textvariable=self.maxLim, width=10).grid(column=1, row=5)
        
        
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
        ttk.Label(plotter,text="File Name").grid(column=0,row=2)
        
        self.storyName=tk.StringVar()
        self.saveFile=tk.StringVar()
        self.saveType=tk.StringVar()
        self.st2Delete=tk.StringVar()
        self.st2Plot=tk.StringVar()
        ttk.Entry(plotter, textvariable=self.storyName).grid(column=1, row=0)
        ttk.Button(plotter, text="Create Story", command=self.createStory).grid(column=1,row=1)
        ttk.Entry(plotter, textvariable=self.saveFile).grid(column=1, row=2)
        self.saveChoosen = ttk.Combobox(plotter, width=6, textvariable=self.saveType, state='readonly')#choose file type
        self.saveChoosen.grid(column=2, row=2)
        self.saveChoosen['values']=('.xlsx')#now only xlsx available
        self.saveChoosen.current(0)
        ttk.Button(plotter, text="Save", command=self.saveStory).grid(column=1,row=4)
        ttk.Label(plotter,text="Delete Story").grid(column=0,row=5)        
        self.deleteStory = ttk.Combobox(plotter, width=15, textvariable=self.st2Delete, state='readonly')#choose file type
        self.deleteStory.grid(column=1,row=5)
        ttk.Button(plotter, text="Delete", command=self.delStory).grid(column=2,row=5)
        ttk.Label(plotter,text="Plot Story").grid(column=0,row=6)
        self.toPlotStory = ttk.Combobox(plotter, width=15, textvariable=self.st2Plot, state='readonly')#choose file type
        self.toPlotStory.grid(column=1,row=6)
        ttk.Button(plotter, text="Plot", command=self.plotStory, state="disabled").grid(column=2,row=6)

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
        self.dataList=[]#list of all groups of selected materials to pass to analize function
        self.st2Anal=tk.StringVar()
        self.percent=tk.IntVar()#50-90%
        self.PromptOut=tk.IntVar()
        self.predMet=tk.StringVar()#predictionMehod (Miner/Broutman)
        
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
        self.perSet['values']=[50,90]
        self.perSet.current(0)
        ttk.Button(beh,text="Estract Groups", command=self.extractGroup).grid(row=0,column=8)
        ttk.Button(beh,text="Choose Groups", command=self.chooseGroup).grid(row=0,column=9)
        
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
        self.groupTree.column("#10",minwidth=0,width=50)
        self.groupTree.grid(column=0, columnspan=6, row=2)
        
        ttk.Label(beh,text="Story").grid(column=0,row=3)
        self.analStory = ttk.Combobox(beh, width=15, textvariable=self.st2Anal, state='readonly')#choose file type
        self.analStory.grid(column=1,row=3)
        printCheck=ttk.Checkbutton(beh,text="Prompt Output", variable=self.PromptOut, onvalue=1, offvalue =0, width=15)
        printCheck.grid(row=3, column=2)
        ttk.Button(beh,text="Analize", command=self.analize).grid(row=3,column=3)
        
    def quitApp(self):
        """
        Quit from application
        """
        self.quit()
        
    def openReadme(self):
        filepath=self.readme
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filepath))
    
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
        try:
            pages = load_workbook(filename = self.fileName, read_only=True).get_sheet_names()
            self.pageChoosen['values']=pages
        except FileNotFoundError:
            string=time.strftime("%H:%M:%S")+": Nessun file caricato"
            self.logError.insert(tk.INSERT,string+"\n")
            self.pageChoosen['values']=[]
            
            
        
    def createStory(self):
        """
        create load story and add it to the list
        now it saves data to default file
        """
        try:
            limit=int(self.maxLim.get())
        except ValueError:#limit not inserted
            limit=0
        try:
            newStory = analysis.loadStory(self.fileName, int(self.header.get()), fileType=str(self.fileType.get()), sheet=self.pageName.get(), column=int(self.column.get()), limit=limit)  
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
    
    def delStory(self):
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
            
    def extractGroup(self):
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
            self.dataList.append([item[2],item[7],item[8]])#R,phi50,phi90
            
    def analize(self):
        """
        TODO: disconnect damage value from the load story class!
        """
        try:
            key = self.st2Anal.get()#get the name of the story selected
            self.loadStored[key].analize(self.dataList,self.matStored[self.matAnal.get()].sigmaT,self.matStored[self.matAnal.get()].sigmaC,\
            self.percent.get(), self.PromptOut.get())
            danno=self.loadStored[key].D
            string=key+"  analized with Miner and total damage is: "+str(danno)+"\n"
            string_2="You can repeat this block "+str(round(danno**-1,2))+" times."
            string=string+string_2
        except IndexError:
            string="ERROR: select press on Show Group! \n Otherwise no group suites your request!"
        self.logError.insert(tk.INSERT,time.strftime("%H:%M:%S")+" "+string+"\n")
        
    def plotStory(self):
        """
        TODO: improve graphical plotting
        """
        print(self.window_2)
        #key=self.st2Plot.get()
        #self.loadStored[key].plot()
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
    
    def chooseGroup(self):
        """
        Tools to modify group list
        """
        if self.groupChoose==1:
            pass
        else:
            groupChoosen(self, "Group Data Tools","400x250")
            self.groupChoose = 1

class matWind(tk.Toplevel):
    """
    """
    def __init__(self, parent, title, size):
        tk.Toplevel.__init__(self, parent)
        self.title(title)
        self.geometry(size)#x,y
        self.resizable(0,0)
        self.parent=parent
        self.iconbitmap='icon_2.ico'
        self.configure(background="gray89")
        
        self.name=tk.StringVar()
        self.sRt=tk.StringVar()
        self.sRc=tk.StringVar()
        self.fiber=tk.StringVar()
        self.matrix=tk.StringVar()
        
        ttk.Label(self,text="Name").grid(column=0,row=0)
        ttk.Entry(self, textvariable=self.name, width=20).grid(column=1, row=0)
        ttk.Label(self,text="fiber").grid(column=0,row=1)
        self.fibreChoosen = ttk.Combobox(self, width=12, textvariable=self.fiber)#choose file page to read
        self.fibreChoosen.grid(column=1, row=1)
        self.fibreChoosen['values']=('carbon','glass')
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
        """
        From Material data tools get properties and insert them to
        main gui materials page tree 
        """
        name=self.name.get()
        fiber=self.fiber.get().lower()
        matrix=self.matrix.get()
        sRt=int(self.sRt.get())
        sRc=abs(int(self.sRc.get() ))
        self.parent.tree.insert('','end',values=('no ID',name,fiber,matrix,sRt,sRc,' '))#id, name, fiber, matrix, Rt, Rc, note
    
    def DBsave(self):
        database.insertMat()
        msg.showwarning("Disabled", "This functionality hasn't been implemented yet")
        
class groupChoosen(tk.Toplevel):
    """
    """
     
    def __init__(self, parent, title, size):
        tk.Toplevel.__init__(self, parent)
        self.title(title)
        self.geometry(size)#x,y
        self.resizable(0,0)
        self.parent=parent
        self.groups=[]
        self.dataList=self.parent.dataList
        self.iconbitmap='icon_2.ico'
        self.configure(background="gray89")
        for child in self.parent.groupTree.get_children():
            self.groups.append(self.parent.groupTree.item(child)['values'])
        
        self.groupTree=ttk.Treeview(self,selectmode="extended",columns=('1','2','3'))
        self.groupTree.heading("#0", text=" ")
        self.groupTree.column("#0",minwidth=0,width=1)
        self.groupTree.heading("#1", text="R")
        self.groupTree.column("#1",minwidth=0,width=50)
        self.groupTree.heading("#2", text="50%")
        self.groupTree.column("#2",minwidth=0,width=50)
        self.groupTree.heading("#3", text="90%")
        self.groupTree.column("#3",minwidth=0,width=50)        
        self.groupTree.grid(column=0, columnspan=4, rowspan=6)
        ttk.Button(self, text="Plot", command=self.plotting).grid(column=4,row=0)
        ttk.Button(self, text="Delete", command=self.deleting).grid(column=4,row=1)
        ttk.Button(self, text="Quit", command=self.quitting).grid(column=4,row=2)
        ttk.Button(self, text="Save & Quit", command=self.saving).grid(column=4,row=3)
        
        self.inserting()
        
        
    def plotting(self):
        """
        plots remaining groups
        """
        self.plotter=[[],[],[],[],[]]#sm50,sa50,sm90,sa90
        for item in self.dataList:
            R=float(item[0])
            smax2E650=float(item[1])
            smax2E690=float(item[2])
            self.plotter[4].append(R)
            if R==-99 or R==99:
                self.plotter[0].append(-smax2E650/2)#sm50
                self.plotter[1].append(smax2E650/2)#sa50
                self.plotter[2].append(-smax2E690/2)#sm90
                self.plotter[3].append(smax2E690/2)#sa90
            else:
                self.plotter[0].append(smax2E650/2*(1+R))#sm50
                self.plotter[1].append(smax2E650/2*(1-R))#sa50
                self.plotter[2].append(smax2E690/2*(1+R))#sm90
                self.plotter[3].append(smax2E690/2*(1-R))#sa90
        if self.parent.percent.get()==50:
            x=self.plotter[0]
            y=self.plotter[1]
        else:
            x=self.plotter[2]
            y=self.plotter[3]
        matGui.scatter([x,y,self.plotter[4]])
            
    def inserting(self):
        """
        insert groups in local table
        """
        for item in self.groups:
            self.groupTree.insert('','end',values=(item[9],item[5],item[6])) 
    
    def deleting(self):
        for item in self.groupTree.selection():
            i=self.groupTree.index(item)
            self.groupTree.delete(item)           
            del(self.groups[i])
            del(self.dataList[i])
    
    def saving(self):
        """
        save remaining group to parent table
        call quit function
        """
        self.parent.dataList=self.dataList
        for i in self.parent.groupTree.get_children():
            self.parent.groupTree.delete(i)
        for item in self.groups:
            self.parent.groupTree.insert('','end',values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9]))
        self.quitting()
            
    def quitting(self):
        self.parent.groupChoose=0
        self.destroy()
        