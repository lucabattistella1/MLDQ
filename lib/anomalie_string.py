# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:21:00 2023

Analizzando le frequenze delle variabili string identifica quelle che presentano un 
potenziale dominio ed evidenzia le casitiche rare

@author: battilu
"""

import pandas as pd
import numpy as np

def anomalie_str(df,colonne_string, coeff_variabil, coeff_dispers):
    anomalie_ch=pd.DataFrame(columns=('variabile','carattere','occorrenze','freq'))
    for colonna in colonne_string:
        if df[colonna].value_counts().shape[0]>0:
            #print(colonna)
            anomalie=pd.DataFrame(columns=('variabile','carattere','occorrenze','freq'))
            data=df[colonna].value_counts() # absolute frequency calculation
            categ_treshold=df.shape[0] / data.shape[0] / coeff_variabil   #treshold dipende da il numero di modalità e il numero totale di record
            anom_var = data[data<categ_treshold]
            if anom_var.shape[0]<data.shape[0]*coeff_dispers: #se una buona % è anomalo, probabilmente non è anomalia
                anomalie['carattere']=list(data.index[data<categ_treshold])#outliers calculation
                anomalie['variabile']=colonna
                anomalie['occorrenze']=list(data[data<categ_treshold])
                anomalie['freq']=anomalie['occorrenze']/data.max()
                anomalie_ch=pd.concat([anomalie_ch,anomalie])
    anomalie_ch=anomalie_ch.sort_values(by=['variabile','occorrenze'], ascending=False)
    anomalie_ch.variabile.value_counts()
    del anomalie, colonna, anom_var, data, categ_treshold
    return anomalie_ch




def anomalie_str_lun(df,colonne_string, freq_lun, amp_lung):
    anomalie_lun = pd.DataFrame(columns=('variabile','carattere','occorrenze'))
    for colonna in colonne_string:
        db = df.dropna(subset=[colonna])
        db['lunghezza'] = db[colonna].astype(str).apply(len)
        # Calcola la media e la deviazione standard della lunghezza
        media = db['lunghezza'].mean()
        deviazione_standard = db['lunghezza'].std()
        # Filtra i record che soddisfano i criteri
        df_filtrato = db.loc[((db['lunghezza'] > (media + 5 * deviazione_standard)) | 
                              (db['lunghezza'] < (media - 5 * deviazione_standard)))]
        filtrati = pd.DataFrame(df_filtrato[colonna].value_counts()).reset_index()
        #elimina i filtrati che compaiono tante volte, con una soglia che dipende dalla 
        #variabilità delle valorizzazioni
        treshold = (df.shape[0] / len(db[colonna].value_counts())) * freq_lun 
        filtrati['da_tenere'] = np.where(filtrati['count']<treshold, 1, 0)
        
        anomalie = pd.DataFrame(columns=('variabile','carattere','occorrenze'))
        anomalie['carattere'] = filtrati.loc[filtrati['da_tenere']==1][colonna]
        anomalie['occorrenze'] = filtrati.loc[filtrati['da_tenere']==1]['count']
        anomalie['variabile'] = colonna
        anomalie_lun = pd.concat([anomalie_lun, anomalie])
    return anomalie_lun
