# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 09:23:26 2023

File per la scrittura del json parametrico. 
È possibile anche modificare il json agendo direttamente sul file.json, ma 
così facendo lo script non sarebbe più allineato

@author: battilu
"""

import os
os.chdir("C:/Users/battilu/OneDrive - Intrum/Analytics/3. Analisi/1. DQ/")

import json

parametri = {
    "tabella": "quality.property",   #quality.cadastral 
    "partizionamento": 'type',   #None
    "null_percent": .95,
    "null_percent_low": 1/10_000,
    "coeff_variabil": 1000,
    "coeff_dispers": .2,
    "freq_lun": .00001,
    "amp_lung": 5,
    "tolleranza_date": .01,
    "verso": "bidirezionale",    #bidirezionale, positivo (solo outlier positivi), negativo (solo negativi)
    "molt_estremo": 7,
    "q": .95,
    "max_perc_threshold_cond": .1, 
    "max_perc_threshold_marg": .5,
    "coeff_dom_rel": 1000
}

# Scrivi i parametri in un file JSON
with open('lib/parametri.json', 'w') as file:
    json.dump(parametri, file)
    

