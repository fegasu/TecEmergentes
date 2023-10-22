# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 08:44:05 2023

@author: Jose Fernando Galindo Suarez
"""
import pandas as pd
data=pd.read_csv("c:/Borrar/COVID19.csv",low_memory=False)
data.columns=data.columns.str.replace('ID de caso','ID')
#CREANDO LA DIMENSION PAIS
def CambioData(col,val1,val2):
    data[col]=data[col].str.replace(val1,val2)
def CambioDataVacios(col,val1):
    data[col].fillna(val1,inplace=True)
def CrearDataFrame(cols):
    aux=pd.DataFrame(data[cols])
    aux.drop_duplicates(inplace=True)
    return aux
def RenombrarColumna(da,cols):
    da.rename(columns=cols, inplace=True)


RenombrarColumna(data,{"ID  de caso":'IDXXXX'})
RenombrarColumna(data,{"Código DIVIPOLA":'IDCIUDAD'})
RenombrarColumna(data,{"Ciudad de ubicación":'CIUDAD'})
RenombrarColumna(data,{"Departamento o Distrito":'DEPARTAMENTO '})
#data.columns=data.columns.str.replace('Departamento o Distrito','DEPARTAMENTO')
RenombrarColumna(data,{"ID  de caso":'IDXXXX'})
RenombrarColumna(data,{"Código DIVIPOLA":'IDCIUDAD'})
RenombrarColumna(data,{"Ciudad de ubicación":'CIUDAD'})
RenombrarColumna(data,{"Departamento o Distrito":'DEPARTAMENTO'})
data.columns=data.columns.str.replace('Departamento o Distrito','DEPARTAMENTO')
RenombrarColumna(data,{"atención":'ATENCION'})
RenombrarColumna(data,{"Tipo":'TIPO'})
RenombrarColumna(data,{"Estado":'ESTADO'})
RenombrarColumna(data,{"País de procedencia":'PAIS'})
RenombrarColumna(data,{"Fecha":'FECHA'})
RenombrarColumna(data,{"Edad":'EDAD'})
RenombrarColumna(data,{"Sexo":'SEXO'})


#Creando la dimension ciudad
DM_CIUDAD=CrearDataFrame(["IDCIUDAD","CIUDAD"])
DM_CIUDAD["IDDPTO"]=DM_CIUDAD["IDCIUDAD"]//1000

#CREANDO LA DIMENSION DEPARTAMENTO
DM_DEPARTAMENTO=pd.DataFrame(data[["IDCIUDAD","DEPARTAMENTO "]])
DM_DEPARTAMENTO["IDCIUDAD"]=DM_DEPARTAMENTO["IDCIUDAD"]//1000
DM_DEPARTAMENTO.drop_duplicates(inplace=True)
DM_DEPARTAMENTO.columns=DM_DEPARTAMENTO.columns.str.replace('IDCIUDAD','IDDPTO')


#CREANDO LA DIMENSION ATENCION
CambioDataVacios("ATENCION","N/A")
DM_ATENCION=CrearDataFrame(["ATENCION"])
DM_ATENCION["IDATENCION"]=range(1,len(DM_ATENCION)+1)

#CREANDO LA DIMENSION TIPO
CambioData("TIPO","relacionado","Relacionado")
CambioData("TIPO","RELACIONADO","Relacionado")
CambioData("TIPO","En Estudio","En estudio")

DM_TIPO=CrearDataFrame(["TIPO"])
DM_TIPO["IDTIPO"]=range(1,len(DM_TIPO)+1)

#CREANDO LA DIMENSION ESTADO
CambioData("ESTADO","leve","Leve")
CambioDataVacios("ESTADO","N/A")

DM_ESTADO=CrearDataFrame(["ESTADO"])
DM_ESTADO["IDESTADO"] = range(1,len(DM_ESTADO)+1)

    
CambioData("PAIS","MÉXICO","MEXICO")
CambioData("PAIS","PERÚ","PERU")
CambioData("PAIS","PANAMÁ","PANAMA")
CambioData("PAIS","CANADÁ","CANADA")
CambioData("PAIS","ARABIA SAUDÍ","ARABIA SAUDITA")
CambioData("PAIS","ESTADOS UNIDOS DE AMÉRICA","ESTADOS UNIDOS")
CambioData("PAIS","ESTADOS UNIDOS DE AMERICA","ESTADOS UNIDOS")

CambioDataVacios("PAIS","COLOMBIA")
DM_PAIS=CrearDataFrame(["PAIS"])
DM_PAIS['IDPAIS']=range(1,len(DM_PAIS)+1)

#Mezclar dimensiones con la tabla de hecho
data = pd.merge(DM_ATENCION,data,left_on="ATENCION",right_on="ATENCION",how="right")
del data['ATENCION']
del data['CIUDAD']
del data['DEPARTAMENTO ']
data = pd.merge(DM_TIPO,data,left_on="TIPO",right_on="TIPO",how="right")
del data['TIPO']
data = pd.merge(DM_ESTADO,data,left_on="ESTADO",right_on="ESTADO",how="right")
del data['ESTADO']
data = pd.merge(DM_PAIS,data,left_on="PAIS",right_on="PAIS",how="right")
del data['PAIS']

#crear el index de las dimensiones y la tabla de hecho
def CrearIndice(da,col):
    da.set_index(col,inplace=True)

CrearIndice(DM_CIUDAD, "IDCIUDAD")
CrearIndice(DM_DEPARTAMENTO, "IDDPTO")
CrearIndice(DM_ATENCION, "IDATENCION")
CrearIndice(DM_TIPO, "IDTIPO")
CrearIndice(DM_ESTADO, "IDESTADO")
CrearIndice(DM_PAIS, "IDPAIS")
CrearIndice(data, "ID")

RenombrarColumna(DM_CIUDAD,{"CIUDAD":'NOMBRE'})
RenombrarColumna(DM_DEPARTAMENTO,{"DEPARTAMENTO ":'NOMBRE'})
RenombrarColumna(DM_ATENCION,{"ATENCION":'NOMBRE'})
RenombrarColumna(DM_TIPO,{"TIPO":'NOMBRE'})
RenombrarColumna(DM_ESTADO,{"ESTADO":'NOMBRE'})
RenombrarColumna(DM_PAIS,{"PAIS":'NOMBRE'})


def CrearCSV(da,nom,ruta):
    da.to_csv(ruta+"/"+nom+".csv")

CrearCSV(DM_CIUDAD,"ZDM_CIUDAD","c:/Borrar")
CrearCSV(DM_DEPARTAMENTO,"ZDM_DEPARTAMENTO","c:/Borrar")
CrearCSV(DM_ATENCION,"ZDM_ATENCION","c:/Borrar")
CrearCSV(DM_TIPO,"ZDM_TIPO","c:/Borrar")
CrearCSV(DM_ESTADO,"ZDM_ESTADO","c:/Borrar")
CrearCSV(DM_PAIS,"ZDM_PAIS","c:/Borrar")

CrearCSV(data,"ZTH_COVID19","c:/Borrar")


'''
CREATE DATABASE COVID19;
USE COVID19
CREATE TABLE COVID19(
ID INTEGER PRIMARY KEY,
IDPAIS INTEGER,
IDESTADO INTEGER,
IDTIPO INTEGER,
IDATENCION INTEGER,
FECHA DATE,
IDCIUDAD INTEGER,
EDAD INTEGER,
SEXO CHAR(1)
);

CREATE TABLE DM_CIUDAD(
    IDCIUDAD INTEGER PRIMARY KEY,
    NOMBRE TEXT,
    IDDPTO INTEGER 
    );

CREATE TABLE DM_DEPARTAMENTO(
    IDDPTO INTEGER PRIMARY KEY,
    NOMBRE TEXT
    );

CREATE TABLE DM_ATENCION(
    IDATENCION INTEGER PRIMARY KEY,
    NOMBRE TEXT
    );

CREATE TABLE DM_TIPO(
    IDTIPO INTEGER PRIMARY KEY,
    NOMBRE TEXT
    );

CREATE TABLE DM_ESTADO(
    IDESTADO INTEGER PRIMARY KEY,
    NOMBRE TEXT
    );

CREATE TABLE DM_PAIS(
    IDPAIS INTEGER PRIMARY KEY,
    NOMBRE TEXT
    );

LOAD DATA INFILE 'c:/Borrar/ZDM_TIPO.csv' INTO TABLE DM_TIPO
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(IDTIPO,NOMBRE);

LOAD DATA INFILE 'c:/Borrar/ZDM_ATENCION.csv' INTO TABLE DM_ATENCION
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(IDATENCION,NOMBRE);

LOAD DATA INFILE 'c:/Borrar/ZDM_ESTADO.csv' INTO TABLE DM_ESTADO
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(IDESTADO,NOMBRE);

LOAD DATA INFILE 'c:/Borrar/ZDM_PAIS.csv' INTO TABLE DM_PAIS
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(IDPAIS,NOMBRE);

LOAD DATA INFILE 'c:/Borrar/ZDM_DEPARTAMENTO.csv' INTO TABLE DM_DEPARTAMENTO
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(IDDPTO,NOMBRE);

LOAD DATA INFILE 'c:/Borrar/ZDM_CIUDAD.csv' INTO TABLE DM_CIUDAD
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(IDCIUDAD,NOMBRE,IDDPTO);

LOAD DATA INFILE 'c:/Borrar/ZTH_COVID19.csv' INTO TABLE COVID19
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(ID,IDPAIS,IDESTADO,IDTIPO,IDATENCION,FECHA,IDCIUDAD,EDAD,SEXO);

ALTER TABLE DM_CIUDAD ADD CONSTRAINT DPTOFK FOREIGN KEY(IDDPTO) 
REFERENCES DM_DEPARTAMENTO(IDDPTO);

ALTER TABLE COVID19 ADD CONSTRAINT CIUDADFK FOREIGN KEY(IDCIUDAD) 
REFERENCES DM_CIUDAD(IDCIUDAD);

ALTER TABLE COVID19 ADD CONSTRAINT ATENCIONFK FOREIGN KEY(IDATENCION) 
REFERENCES DM_ATENCION(IDATENCION);

ALTER TABLE COVID19 ADD CONSTRAINT ESTADOFK FOREIGN KEY(IDESTADO) 
REFERENCES DM_ESTADO(IDESTADO);

ALTER TABLE COVID19 ADD CONSTRAINT PAISFK FOREIGN KEY(IDPAIS) 
REFERENCES DM_PAIS(IDPAIS);

ALTER TABLE COVID19 ADD CONSTRAINT TIPOFK FOREIGN KEY(IDTIPO) 
REFERENCES DM_TIPO(IDTIPO);

CREATE OR REPLACE VIEW VCOVID19 AS
SELECT 'DM_ATENCION',COUNT(*) FILAS FROM DM_ATENCION
UNION
SELECT 'DM_CIUDAD',COUNT(*) FILAS FROM DM_CIUDAD
UNION
SELECT 'DM_DEPARTAMENTO',COUNT(*) FILAS FROM DM_DEPARTAMENTO
UNION
SELECT 'DM_ESTADO',COUNT(*) FILAS FROM DM_ESTADO
UNION
SELECT 'DM_PAIS',COUNT(*) FILAS FROM DM_PAIS
UNION
SELECT 'DM_TIPO',COUNT(*) FILAS FROM DM_TIPO
UNION
SELECT 'TH_COVID19',COUNT(*) FILAS FROM COVID19
;






'''