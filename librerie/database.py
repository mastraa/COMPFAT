# -*- coding: utf-8 -*-
"""
Author: Andrea Mastrangelo

Last release 14/07/2016
"""

import sqlite3

name = "fatData.db"
connection = sqlite3.connect(name)
cursor = connection.cursor()

cursor.execute("SELECT * FROM matGroup") 
print("fetchall:")
result = cursor.fetchall() 
for r in result:
    print(r)
cursor.execute("SELECT * FROM matGroup")
print("\nfetch one:")
res = cursor.fetchone() 
print(res)