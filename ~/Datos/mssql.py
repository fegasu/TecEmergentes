# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 13:23:49 2023

@author: Administrador
"""

import sqlalchemy
import pyodbc
import pandas as pd



conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=BOGDFPCGMASP213\SQLEXPRESS;'
                      'Database=covid19;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('SELECT * FROM DM_TIPO')

for i in cursor:
    print(i)

df = pd.read_sql_query('SELECT * FROM DM_TIPO', conn)
    
    
