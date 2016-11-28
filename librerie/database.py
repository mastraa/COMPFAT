# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 28/11/2016
"""

import sqlite3, os

_name = "fatData.db"



def configName(url, file, _name):
    """
    get DB name from config file
    """
    
    try:
        f=open(os.path.join(url, file))
        istr=f.readlines()
        for item in istr:
            if "DB" in item:
                last = item.find(".db")
                name=item[3:last+3]
                if os.path.isfile(os.path.join(url, 'configFile/'+name)):
                    _name=os.path.join(url, 'configFile/'+name)
                else:
                    _name=os.path.join(url, 'configFile/'+_name)
        return _name
    except FileNotFoundError:
        return os.path.join(url, 'configFile/'+_name)

def DBconnect(_name):
    connection = sqlite3.connect(_name)
    cursor = connection.cursor()
    return connection, cursor

def DBdisconnect(connection):
    connection.close()
    

def searchField(name, table, field):
    """
    return a list of all item in field column of table selcted
    """
    connection, cursor = DBconnect(name)
    lista =[]
    cursor.execute('SELECT ({coi}) FROM {tn}'.\
        format(coi=field, tn=table))
    result = cursor.fetchone()
    while result: 
        lista.append(result[0])
        result = cursor.fetchone()
    DBdisconnect(connection)
    return list(set(lista))
    
    
    
def searchAll(name, table, field, goal):
    """
    Return a list of item of all column
    with the request characteristic in table
    """
    connection, cursor = DBconnect(name)
    cursor.execute("SELECT * FROM "+table+" WHERE "+field+"=:Id",{"Id": goal})
    result = cursor.fetchall()
    DBdisconnect(connection)
    return result
    
def searchAllGroups(name, fibre, matrix, beh, arch):
    connection, cursor = DBconnect(name)
    cursor.execute("SELECT * FROM matGroup WHERE fibre=? AND behav=? AND arch=? AND matrix=?",(fibre, beh, arch, matrix))
    result = cursor.fetchall()
    DBdisconnect(connection)
    return result
    
def insertMat(db, name, fiber ,matrix, sRc, sRt):
    connection, cursor = DBconnect(db)
    try:
        cursor.execute("INSERT INTO matLib (name, fiber, matrix, sRt, sRc, note) VALUES ('"+name+"','"+fiber+"','"+matrix+"',"+str(sRt)+","+str(sRc)+",'nota')")
    except sqlite3.Error as e:
        print (e.args[0])
    connection.commit()
    DBdisconnect(connection)
    
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