# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 12:20:58 2023

Controlli descrittivi su:
    - colonne missing
    - colonne monovalorizzate

@author: battilu
"""

import pandas as pd
import numpy as np

def colonne_null_mono(df):
    variable_list_null = df.columns
    anomalie_null_mono=pd.DataFrame()
    for col in variable_list_null:
        anomalie_null = pd.DataFrame(  columns=['variabile','anomalia'])
        anomalie_mono = pd.DataFrame(  columns=['variabile','anomalia'])
        if df[col].notnull().sum() == 0: # checks if the column has only null values
            nuova_riga = {'variabile': col, 'anomalia': 'colonna con soli nulli'}
            anomalie_null.loc[0] = nuova_riga
            anomalie_null_mono = pd.concat([anomalie_null_mono,anomalie_null])
        elif len(df[col].astype(str).str.strip().unique()) == 1: # checks if the column has only constants values (including '' and ' ')
            nuova_riga = {'variabile': col, 'anomalia': f"colonna con un unico valore '{str(df[col].values[0])}'"}
            anomalie_mono.loc[0] = nuova_riga
            anomalie_null_mono = pd.concat([anomalie_null_mono,anomalie_mono])
    del anomalie_null, anomalie_mono, nuova_riga, col
    return anomalie_null_mono