# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 15:01:46 2023

@author: Administrador

"""
import sqlalchemy
import pyodbc
import pandas as pd
ruta="E:/Datos"
data=pd.read_csv(ruta+"/TH_COVID19.csv",low_memory=False)


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=BOGDFPCGMASP213\SQLEXPRESS;'
                      'Database=covid19;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

for row in data.itertuples():
    cursor.execute('''
                INSERT INTO COVID19 (ID,IDFECHA,IDPAIS,IDESTADO,IDTIPO,IDATENCION,IDCIUDAD,EDAD,SEXO)
                VALUES (?,?,?,?,?,?,?,?,?)
                ''',
                row.ID,
                row.IDFECHA,
                row.IDPAIS,
                row.IDESTADO,
                row.IDTIPO,
                row.IDATENCION,
                row.IDCIUDAD,
                row.EDAD,
                row.SEXO
                )
conn.commit()


