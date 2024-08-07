# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 11:37:12 2023

1. Scarica il df da utilizzare
2.

@author: battilu
"""
### imposta cartella di lavoro ###
#import getpass
#import sys
'''
sys.path.insert(1, 'C:/Users/' +getpass.getuser()+ '/OneDrive - Intrum/GitHub/DataQuality/')
import os
os.chdir("C:/Users/" +getpass.getuser()+ "/OneDrive - Intrum/GitHub/DataQuality/")
'''

### import librerie ###
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.3f' % x)
import json
from datetime import datetime


### import funzioni ###
from lib.conn_scarico_tabella import esegui_connessione
from lib.anomalie_null_mono import colonne_null_mono
from lib.anomalie_missing import anomalie_miss
from lib.anomalie_string import anomalie_str
from lib.anomalie_string import anomalie_str_lun
from lib.anomalie_date import anomalie_date
from lib.anomalie_num import anomalie_numeriche_pos
from lib.anomalie_num import anomalie_numeriche_neg
from lib.anomalie_relazionali_cat import anomalie_bivariate_categoriali

### Setting parametri ###
#legge i parametri dal file JSON
print('***** Lettura parametri *****')
with open('lib/parametri.json', 'r') as file:
    parametri = json.load(file)
tabella = parametri['tabella'] 
partizionamento = parametri['partizionamento']
null_percent = parametri['null_percent']
null_percent_low = parametri['null_percent_low']
coeff_variabil = parametri['coeff_variabil']
coeff_dispers = parametri['coeff_dispers']
freq_lun = parametri['freq_lun']
amp_lung = parametri['amp_lung']
tolleranza_date = parametri['tolleranza_date']
verso = parametri['verso']
molt_estremo = parametri['molt_estremo']
q = parametri['q']
max_perc_threshold_cond = parametri['max_perc_threshold_cond']
max_perc_threshold_marg = parametri['max_perc_threshold_marg']
coeff_dom_rel = parametri['coeff_dom_rel']


### Scarico del dataframe da utilizzare ###
print('***** Caricamento tabella dati *****')
df = esegui_connessione(tabella)


### Controllo variabili null o mono distribuite ###
print('***** Controllo variabili null o mono distribuite *****')
anomalie_null_mono_df = colonne_null_mono(df)
anomalie_null_mono_df.to_csv('result/anomalie_null_mono - ' + tabella + " - " 
                             + str(datetime.now().strftime("%Y-%m-%d")) 
                             + '.csv',sep=';',index=False)

### Controllo variabili con pochi o tanti missing ###
print('***** Controllo variabili con pochi o tanti missing *****')
anomalie_miss_df = anomalie_miss(df, null_percent,null_percent_low)
anomalie_miss_df.to_csv('result/anomalie_miss - ' + tabella + " - "  + str(
    datetime.now().strftime("%Y-%m-%d")) + '.csv',sep=';',index=False)


### Definizione dei type delle colonne ###
colonne_string = []
colonne_non_num = []
# Prova a convertire ciascuna colonna in numerico
for colonna in df.columns:
    try:
        pd.to_numeric(df[colonna])
    except (ValueError, TypeError):
        colonne_non_num.append(colonna)
# Prova a convertire ciascuna colonna in data
for colonna in colonne_non_num:#
    try:
        pd.to_datetime(df[colonna]) #,format="%Y/%m/%d"
    except (ValueError, TypeError):
        colonne_string.append(colonna)
colonne_dat = list(set(colonne_non_num) - set(colonne_string))
colonne_num = list(set(df.columns) - set(colonne_non_num))

### Controllo variabili stringa ###
print('***** Controllo variabili stringa *****')
anomalie_ch = anomalie_str(df, colonne_string, coeff_variabil, coeff_dispers)
anomalie_ch.to_csv('result/anomalie_stringa - ' + tabella + " - "  + str(
    datetime.now().strftime("%Y-%m-%d")) + '.csv',sep=';',index=False)
anomalie_ch_lun = anomalie_str_lun(df, colonne_string, freq_lun, amp_lung)
anomalie_ch_lun.to_csv('result/anomalie_stringa_lunghezza - ' + tabella + " - "  + str(
    datetime.now().strftime("%Y-%m-%d")) + '.csv',sep=';',index=False)



### Controllo variabili date ###
print('***** Controllo variabili date *****')
anomalie_dt = anomalie_date(df, colonne_dat, tolleranza_date)
anomalie_dt.to_csv('result/anomalie_date - ' + tabella + " - "  + str(
    datetime.now().strftime("%Y-%m-%d")) + '.csv',sep=';',index=False)


### controllo variabili numeriche non boleane ###
print('***** Controllo variabili numeriche *****')
# il secondo parametro è l'eventuale variabile di partizionamento, se non prevista indicare "None"
if verso =='bidirezionale':
    anomalie_num_pos = anomalie_numeriche_pos(df, partizionamento, colonne_num, molt_estremo, q)
    anomalie_num_pos['tipo']  = 'positivo'
    anomalie_num_neg= anomalie_numeriche_neg(df, partizionamento, colonne_num, molt_estremo, q)
    anomalie_num_neg['tipo']  = 'negativo'
    anomalie_num = pd.concat([anomalie_num_pos, anomalie_num_neg])
if verso =='positivo':
    anomalie_num_pos = anomalie_numeriche_pos(df, partizionamento, colonne_num, molt_estremo, q)
    anomalie_num_pos['tipo']  = 'positivo'
    anomalie_num = anomalie_num_pos
if verso =='negativo':
    anomalie_num_neg = anomalie_numeriche_neg(df, partizionamento, colonne_num, molt_estremo, q)
    anomalie_num_neg['tipo']  = 'negativo'
    anomalie_num = anomalie_num_neg
anomalie_num.to_csv('result/anomalie_numeriche - ' + tabella + " - "  + str(
    datetime.now().strftime("%Y-%m-%d")) + '.csv',sep=';',index=False)


### Controllo relazionali ###
print('***** Controllo relazionale variabili categoriche *****')
anomalie_relaz_cat = anomalie_bivariate_categoriali(df, colonne_string, coeff_dom_rel, max_perc_threshold_cond,max_perc_threshold_marg)
anomalie_relaz_cat.to_csv('result/anomalie_relaz_cat - ' + tabella + " - "  + str(
    datetime.now().strftime("%Y-%m-%d")) + '.csv',sep=';',index=False)
