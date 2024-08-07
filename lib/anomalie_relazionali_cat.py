# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 18:08:04 2023

@author: battilu
"""
import pandas as pd
import numpy as np
import itertools

def anomalie_bivariate_categoriali(df, colonne_string, coeff_dom_rel, max_perc_threshold_cond,max_perc_threshold_marg):
    # Genera tutte le combinazioni di coppie
    anomalies_fin = pd.DataFrame(columns=['categorical_1', 'categorical_2', 'label', 'value1', 'value2', 'conteggio', 'description'])
    combinazioni = list(itertools.permutations(colonne_string, 2))
    for coppia in combinazioni:
        categorical_1 = coppia[0]
        categorical_2 = coppia[1]
#        print(categorical_1 + ' - ' + categorical_2)
        if ((len(df[categorical_1].value_counts())<coeff_dom_rel) & (len(df[categorical_2].value_counts())<coeff_dom_rel)):
            df[categorical_1] = df[categorical_1].astype(str)
            df[categorical_2] = df[categorical_2].astype(str)
            df_freq = pd.pivot_table(df, index=categorical_1, columns=categorical_2, aggfunc='size') # create table of absolute frequencies
            #df_freq2 = df_freq.div(df_freq.sum(axis=1), axis=0) # marginal distribution by column for each row (row sums to 1)
            max_perc_threshold_cond_c = max_perc_threshold_cond / np.sqrt(df_freq.shape[0])
#            print(max_perc_threshold_cond_c)
            max_perc_threshold_marg_c = max_perc_threshold_marg / np.sqrt(df_freq.shape[1])
#            print(max_perc_threshold_marg_c)
            
            
        #    anomalies = pd.DataFrame(columns=['index', 'macrocategory', 'type', 'label', 'value1', 'value2', 'description'])
            anomalies = pd.DataFrame(columns=['categorical_1', 'categorical_2', 'label', 'value1', 'value2', 'conteggio', 'description'])
            for categorical_1_level, row in df_freq.iterrows(): # iterate through all levels of categorical_1
        #        print('********* ' + categorical_1_level + ' - ' + str(row))
                max_value = row.max() # most frequent column
                for categorical_2_level, value in row.items(): # iterate through all levels of categorical_2
        #            print('* ' + categorical_2_level + ' - ' + str(value))
                    if value < max_value * max_perc_threshold_cond_c: #se casistica rara analizzando le righe
        #                print("primo filtro " + categorical_1_level + str(value) + " - " + str(max_value * max_perc_threshold_cond))
                        row_total = df_freq.sum(axis=0) #prendo le marginali di colonna
        #                print("secondo filtro " + categorical_2_level + str(row_total.loc[categorical_2_level] / row_total.sum() > max_perc_threshold_marg) + " - " + str(row_total.loc[categorical_2_level] / row_total.sum()) + " - " + str(max_perc_threshold_marg))
        #                print(str(row_total.loc[categorical_2_level]) + ' - ' + str(row_total.sum()))
                        if row_total.loc[categorical_2_level] / row_total.sum() > max_perc_threshold_marg_c: # if the total by column is not rare overall
                            list_row_pk = df[(df[categorical_1]==categorical_1_level) & (df[categorical_2]==categorical_2_level)].index.to_list()
                            for row_pk in list_row_pk:
                                anomalies.loc[len(anomalies)] = ['relational', 'outlier categoriale relazionale', f'{categorical_1} vs {categorical_2}', categorical_1_level, categorical_2_level, value, f'La coppia {categorical_1_level}-{categorical_2_level} si presenta solo {int(value)} ({(100*value/ row_total.loc[categorical_2_level]):.2e} %) volte nei campi {categorical_1}-{categorical_2}']
        #                    for row_pk in list_row_pk:
        #                        indice_row=list(df.index).index(row_pk)
        #                        anomalies.loc[len(anomalies)] = [row_pk, 'relational', 'outlier categoriale relazionale', f'{categorical_1} vs {categorical_2}', categorical_1_level, categorical_2_level, f'La coppia {categorical_1_level}-{categorical_2_level} si presenta solo {int(value)} ({(100*value/ row_total.loc[categorical_2_level]):.2e} %) volte nei campi {categorical_1}-{categorical_2}']
                                anomalies = anomalies.drop_duplicates()
            anomalies_fin = pd.concat([anomalies_fin , anomalies])
        
    return anomalies_fin 
      
