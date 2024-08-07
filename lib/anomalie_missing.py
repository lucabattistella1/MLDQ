# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 12:43:36 2023

verifica la presenza di variabili con tantissimi valori mancanti o di variabili 
sempre valorizzate ad occasione di casi sporadici che possono rappresentare un'anomalia

@author: battilu
"""

import pandas as pd

def anomalie_miss(df,null_percent,null_percent_low):
    variable_list_null = df.columns
    anomalie_miss = pd.DataFrame(columns=['variabile','anomalia', 'perc_missing'])
    for col in variable_list_null:
        sum_of_missing = (sum(df[col] == '')  +    # Check for values = ''
                        sum(df[col] == ' ') +      # Check for values = ' ' 
                        sum(df[col].isnull()))     # Check for Null values 
        threshold = len(df[col])*(null_percent)
        if ((sum_of_missing >= threshold) & (sum_of_missing<df.shape[0])):
            anomalie_miss.loc[len(anomalie_miss)]=[col , f'colonna con più del {null_percent*100}% di valori nulli', round((sum_of_missing/len(df[col]))*100,2)]
        
        if ((sum_of_missing<(len(df[col])*null_percent_low)) & (sum_of_missing!=0)):
            anomalie_miss.loc[len(anomalie_miss)]=[col, f'colonna con {sum_of_missing} valori nulli', round((sum_of_missing/len(df[col]))*100,2)]
    del sum_of_missing, col, threshold  
    return(anomalie_miss)