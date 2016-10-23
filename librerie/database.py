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
    cursor.execute('SELECT ({coi}) FROM {tn}'.\
        format(coi=field, tn=table))
    result = cursor.fetchone()
    while result: 
        lista.append(result[0])
        result = cursor.fetchone()
    return list(set(lista))
    
    
def searchAll(table, field, goal):
    """
    Return a list of item of all column
    with the request characteristic in table
    """
    cursor.execute("SELECT * FROM "+table+" WHERE "+field+"=:Id",{"Id": goal})
    result = cursor.fetchall()
    return result
    
def searchAllGroups(fibre, matrix, beh, arch):
    cursor.execute("SELECT * FROM matGroup WHERE fibre=? AND behav=? AND arch=? AND matrix=?",(fibre, beh, arch, matrix))
    result = cursor.fetchall()
    return result
    
def nextMax(value,lista):
    """
    value is the aim
    lista: list ordered from min to max
    return the minimum value higher than aim_value
    return R value or NameError
    """
    for i in lista:
        if i>value:
            return i
    raise NameError('No value')

def nextMin(value,lista):
    """
    value is the aim
    lista: list ordered from max to min
    return the maximum value lower than aim_value
    return R value or NameError
    """
    for i in lista:
        if i<value:
            return i
    raise NameError('No value')