# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:21:00 2023

controllo sulle date che non siano future (e se lo sono che lo siano spesso)
valid_to_dt non entra qui perchè pandas non riconosce 9999 come una data

@author: battilu
"""

import pandas as pd
import numpy as np
from datetime import datetime

def anomalie_date(df, colonne_dat, tolleranza):
    anomalie_dt=pd.DataFrame(columns=('variabile','carattere','occorrenze'))
    today=datetime.now().strftime("%Y-%m-%d")
    for colonna in colonne_dat:
        anomalie=pd.DataFrame(columns=('variabile','carattere','occorrenze'))
        anom = df.loc[pd.to_datetime(df[colonna],format="%Y/%m/%d")>today][colonna]
        if len(anom)>0 & len(anom)<df.shape[0]*tolleranza:
            anom_df = pd.DataFrame(anom.value_counts())
            anomalie['carattere'] = anom_df.index
            anomalie['occorrenze'] = list(anom_df['count'])
            anomalie['variabile'] = colonna
            anomalie_dt = pd.concat([anomalie_dt,anomalie])       
    del anomalie, colonna, anom
    return anomalie_dt