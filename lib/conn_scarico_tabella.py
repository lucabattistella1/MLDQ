# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 11:34:41 2023

Connessione a postgresql e scarico della tabella di analisi

@author: battilu
"""

#import librerie
import psycopg2
from configparser import ConfigParser
import pandas as pd

def esegui_connessione(tabella):
    config_postgreSQL = ConfigParser()
    config_postgreSQL.read('lib/uat_sandbox.ini')
    try:
        conn_postgreSQL = psycopg2.connect(
        database=config_postgreSQL.get('postgresql','database'),
        host=config_postgreSQL.get('postgresql', 'host'),
        port=config_postgreSQL.get('postgresql', 'port'),
        user=config_postgreSQL.get('postgresql', 'user'),
        password=config_postgreSQL.get('postgresql', 'password')
        )
    except psycopg2.Error as error:
        print("Unable to connect to postgreSQL database: ", error)
    finally:
        if conn_postgreSQL:
            print("Estabilished Connection to postgreSQL")
    
    #recupero la tabella
    if tabella == 'quality.property':
        print('****************************************************************************************')
        print('construction_year trasformata in char perchè presenta un valore 0001-01-01 che genera errore')
        print('****************************************************************************************')
        query = """SELECT property_pk, system_fk, lot_fk, original_property_id, source_property_id, 
                group_property_id, source_lot_id, property_description, macro_type, type, sub_type, 
                solvency_status, status, acquisition_amount,  address, street_no, city, province, 
                region, country, zip_code, commercial_sqm, sqm, occupancy_status,  selling_amount, 
                antieconomic_legal_procedure_flag, longitude, latitude, area_type, 
                construction_completion_flag, construction_completion,  current_record_flag, 
                main_family_flag,insert_flow, correlation_id, reference_period, portfolio_family, 
                valid_from_dt, valid_to_dt,acquisition_date,  insert_ts, update_ts, selling_date ,
                to_char(construction_year, 'YYYY-MM-DD') as construction_year_ch
                FROM """ + tabella + " WHERE current_record_flag is true;"
        df = pd.read_sql_query(query, conn_postgreSQL, coerce_float=False, parse_dates={"construction_year":str})
    else:
        query = "SELECT * FROM " + tabella + " WHERE current_record_flag is true;"
        df = pd.read_sql_query(query, conn_postgreSQL, coerce_float=False)

    conn_postgreSQL.close()
    return df


