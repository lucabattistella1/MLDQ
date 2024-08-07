# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:21:00 2023

eventualmente partizionando per una variabile, identifica tutti gli outlier positivi 
che presentano valori estremi

@author: battilu
"""

import pandas as pd
import numpy as np

# Impostare il formato di visualizzazione dei float in notazione fissa
pd.set_option('display.float_format', lambda x: '%.3f' % x)

def anomalie_numeriche_pos(df, partizionamento, colonne_num, molt_estremo, q):
    if partizionamento != None:
        anomalie_num=pd.DataFrame(columns=['variabile', 'partizionamento','anomalia', 'media'])
        tipologie = pd.DataFrame(df[partizionamento].value_counts()).reset_index() #cambia tanto con value_counts(dropna=False)
        tipologie['type_new'] = np.where(tipologie['count']<500, "Categoria Residuale", tipologie[partizionamento])
        df_t=pd.merge(df,tipologie, on=partizionamento,how='left')
        for colonna in colonne_num:
            df_t[colonna]=pd.to_numeric(df_t[colonna])
            if df_t[colonna].dtype!=bool:
                for tipologia in pd.DataFrame(df_t.type_new.value_counts()).index:
                    anomalie=pd.DataFrame(columns=['variabile', 'partizionamento','anomalia', 'media'])
                    db=df_t.loc[(df_t.type_new == tipologia) & (df_t[colonna] > 0)][colonna].dropna()
                    if len(db)>0:
                        soglia_up=molt_estremo*np.mean(db[db>np.quantile(pd.to_numeric(db),q)]) # prendo la coda estrema e isolo quelli che si distanziano molto dalla media della coda
                        db_anom=db[db>soglia_up]
                        if len(db_anom)>0:
                            media= np.mean(db)
                            anomalie['anomalia'] = db_anom
                            anomalie['variabile'] = colonna
                            anomalie['partizionamento'] = partizionamento + ': ' + tipologia
                            anomalie['media'] = media
                            anomalie_num = pd.concat([anomalie_num, anomalie])
        anomalie_num['delta'] = anomalie_num['anomalia'] - anomalie_num['media']
    else:
        anomalie_num=pd.DataFrame(columns=['variabile', 'partizionamento','anomalia', 'media'])
        for colonna in colonne_num:
            df[colonna]=pd.to_numeric(df[colonna])
            if df[colonna].dtype!=bool:
                anomalie=pd.DataFrame(columns=['variabile', 'partizionamento','anomalia', 'media'])
                db=df.loc[(df[colonna] > 0)][colonna].dropna()
                if len(db)>0:
                    soglia_up=molt_estremo*np.mean(db[db>np.quantile(pd.to_numeric(db),q)]) # prendo la coda estrema e isolo quelli che si distanziano molto dalla media della coda
                    db_anom=db[db>soglia_up]
                    if len(db_anom)>0:
                        media= np.mean(db)
                        anomalie['anomalia'] = db_anom
                        anomalie['variabile'] = colonna
                        anomalie['partizionamento'] = "non prevista"
                        anomalie['media'] = media
                        anomalie_num = pd.concat([anomalie_num, anomalie])
        anomalie_num['delta'] = anomalie_num['anomalia'] - anomalie_num['media']
        
    return anomalie_num





def anomalie_numeriche_neg(df, partizionamento, colonne_num, molt_estremo, q):
    q=1-q
    if partizionamento != None:
        anomalie_num=pd.DataFrame(columns=['variabile', 'partizionamento','anomalia', 'media'])
        tipologie = pd.DataFrame(df[partizionamento].value_counts()).reset_index() #cambia tanto con value_counts(dropna=False)
        tipologie['type_new'] = np.where(tipologie['count']<500, "Categoria Residuale", tipologie[partizionamento])
        df_t=pd.merge(df,tipologie, on=partizionamento,how='left')
        for colonna in colonne_num:
            df_t[colonna]=pd.to_numeric(df_t[colonna])
            if df_t[colonna].dtype!=bool:
                for tipologia in pd.DataFrame(df_t.type_new.value_counts()).index:
                    anomalie=pd.DataFrame(columns=['variabile', 'partizionamento','anomalia', 'media'])
                    db=df_t.loc[(df_t.type_new == tipologia) & (df_t[colonna] != 0)][colonna].dropna()
                    if len(db)>0:
                        soglia_down=-molt_estremo*abs(np.mean(db[db<np.quantile(pd.to_numeric(db),q)])) # prendo la coda estrema e isolo quelli che si distanziano molto dalla media della coda
                        if soglia_down<0:
                            db_anom=db[db<soglia_down]
                            if len(db_anom)>0:
                                media= np.mean(db)
                                anomalie['anomalia'] = db_anom
                                anomalie['variabile'] = colonna
                                anomalie['partizionamento'] = partizionamento + ': ' + tipologia
                                anomalie['media'] = media
                                anomalie_num = pd.concat([anomalie_num, anomalie])
            anomalie_num['delta'] = anomalie_num['anomalia'] - anomalie_num['media']
    else:
        anomalie_num=pd.DataFrame(columns=['variabile', 'partizionamento','anomalia', 'media'])
        for colonna in colonne_num:
            df[colonna]=pd.to_numeric(df[colonna])
            if df[colonna].dtype!=bool:
                anomalie=pd.DataFrame(columns=['variabile', 'partizionamento','anomalia', 'media'])
                db=df.loc[(df[colonna] != 0)][colonna].dropna()
                if len(db)>0:
                    soglia_down=-molt_estremo*abs(np.mean(db[db<np.quantile(pd.to_numeric(db),q)])) # prendo la coda estrema e isolo quelli che si distanziano molto dalla media della coda
                    if soglia_down<0:
                        db_anom=db[db<soglia_down]
                        if len(db_anom)>0:
                            media= np.mean(db)
                            anomalie['anomalia'] = db_anom
                            anomalie['variabile'] = colonna
                            anomalie['partizionamento'] = "non prevista"
                            anomalie['media'] = media
                            anomalie_num = pd.concat([anomalie_num, anomalie])
        anomalie_num['delta'] = anomalie_num['anomalia'] - anomalie_num['media']
        
    return anomalie_num
