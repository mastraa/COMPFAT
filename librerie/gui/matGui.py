# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:58:33 2016

@author: mastraa
"""

import tkinter as tk
from tkinter import ttk
import database, analysis

class MatWindow(tk.Toplevel):
    """
    Material options
    Load, save material
    """
    def __init__(self, title, size, matStore):
        tk.Toplevel.__init__(self)
        self.title(title)
        self.width=1000
        self.height=size[1]
        self.configure(background="gray50")
        
        lista=database.searchField('matLib','fiber')
        self.material=tk.StringVar()
        self.matChoosen = ttk.Combobox(self, width=12, textvariable=self.material, state='readonly')
        self.matChoosen.grid(column=0, row=0)
        self.matChoosen['values']=lista
        ttk.Button(self,text="Search", command=self.searchMat).grid(row=0,column=1)
        
        self.tree=ttk.Treeview(self,selectmode="extended",columns=('1','2','3','4'))
        self.tree.heading("#0", text="Id")
        self.tree.column("#0",minwidth=0,width=30)
        self.tree.heading("#1", text="Name")
        self.tree.column("#1",minwidth=0,width=200)
        self.tree.heading("#2", text="Fiber")
        self.tree.column("#2",minwidth=0,width=80)
        self.tree.heading("#3", text="Matrix")
        self.tree.column("#3",minwidth=0,width=50)
        self.tree.heading("#4", text="R [MPa]")
        self.tree.column("#4",minwidth=0,width=100)
        self.tree.grid(column=0, columnspan=5, row=2)
        
        
        self.idMat=tk.StringVar()
        ttk.Label(self,text="Mat ID").grid(column=0,row=3)
        ttk.Entry(self, textvariable=self.idMat).grid(column=1, row=3)
        ttk.Button(self,text="OK", command=lambda:self.close(matStore)).grid(row=3,column=2)
        
    def close(self,matStore):
        """TODO: find the way to give back the material data"""
        matStore['prova']=analysis.matList(int(self.idMat.get()), 'prova')
        self.destroy()
    
    def searchMat(self):
        materiale=str(self.material.get())
        for item in database.searchAll('matLib','fiber',materiale):
            self.addToTable(item)
        
    def addToTable(self, item):
        self.tree.insert('','end',text=item[0],values=(item[4],item[1],item[2],item[3]))
        

          
        
          
