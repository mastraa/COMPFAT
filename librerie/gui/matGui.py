# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:58:33 2016

@author: mastraa
"""

import tkinter as tk
from tkinter import ttk
import database

class MatWindow(tk.Toplevel):
    """
    Material options
    Load, save material
    """
    def __init__(self, title, size, matStore):
        tk.Toplevel.__init__(self)
        self.title(title)
        self.width=size[0]
        self.height=size[1]
        self.configure(background="gray50")
        
        lista=database.searchField('matLib','fiber')
        self.material=tk.StringVar()
        self.matChoosen = ttk.Combobox(self, width=12, textvariable=self.material, state='readonly')
        self.matChoosen.grid(column=0, row=0)
        self.matChoosen['values']=lista
        
        self.tree=ttk.Treeview(self,selectmode="extended",columns=('1','2','3'))
        self.tree.heading("#0", text="Name")
        self.tree.column("#0",minwidth=0,width=100)
        self.tree.heading("#1", text="Fiber")
        self.tree.column("#1",minwidth=0,width=100)
        self.tree.heading("#2", text="Matrix")
        self.tree.column("#2",minwidth=0,width=100)
        self.tree.heading("#3", text="R [MPa]")
        self.tree.column("#3",minwidth=0,width=100)
        self.tree.grid(column=0, columnspan=3, row=4)
        
        self.tree.insert('','end',text='uno',values=('due','tre','quattro'))
        
        ttk.Button(self,text="OK", command=lambda:self.close(matStore)).grid(row=5,column=0)
        
    def close(self,matStore):
        """TODO: find the way to give back the material data"""
        matStore['prova']=['uno',1]
        self.destroy()

          
        
          
