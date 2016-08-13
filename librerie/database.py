# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016
"""

import sqlite3


name = "fatData.db"
connection = sqlite3.connect(name)
cursor = connection.cursor()

"""
cursor.execute("SELECT * FROM matGroup") 
print("fetchall:")
result = cursor.fetchall() 
for r in result:
    print(r)
cursor.execute("SELECT * FROM matGroup")
print("\nfetch one:")
res = cursor.fetchone() 
print(res)
"""
def searchField(table, field):
    """
    return a list of all item in field column of table selcted
    """
    lista =[]
    table='matLib'
    cursor.execute("SELECT '"+field+"' FROM '"+table+"'")
    result = cursor.fetchone()
    while result:
        lista.append(result[0])
        result = cursor.fetchone()
    return list(set(lista))
    
def searchAll():
    """
    Return a list of item of alla column
    with the request characteristic in table
    """