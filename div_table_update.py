# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 03:59:45 2021

@author: User
"""

import pandas as pd
pd.set_option('display.max_columns', 150)
pd.set_option('display.max_rows', 300)
import requests as req
import time
from botFunctions import parse_div_table, compare_table, create_text_message
import streamlit as st
import os
import config



# ---------------Telegram API------------------

def telegram_bot_sendtext(bot_message):
    
    send_text = 'http://api.telegram.org/bot' + os.getenv('bot_token') + '/sendMessage?chat_id=' + os.getenv('bot_chatID') + '&parse_mode=Markdown&text=' + bot_message
    #send_text = 'https://api.telegram.org/bot' + config.bot_token + '/sendMessage?chat_id=' + config.bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    
    response = req.get(send_text)

    return response.json()
    

#st.header("Last saved version of the table: ")
#df_curr = pd.DataFrame()


#df_curr = pd.read_csv("Div_table_dohod_ru.csv", index_col=0)
#df_curr.sort_index(inplace=True)

#st.dataframe(df_curr)

#st.header("Updated table (from web page): ")
#st.write(df_new)

# ##########################################
# df_origin = pd.read_csv("Div_table_dohod_ru.csv", index_col=0)
# df_origin['concat_column'] = df_origin['Акция'] + " " + df_origin['Период']
# st.dataframe(df_origin)
# df_origin.to_csv("Div_table_dohod_ru.csv")
# ##########################################



while True:
    df_new = pd.DataFrame()
    df_curr = pd.DataFrame()

    df_new = parse_div_table()
    df_curr = pd.read_csv("Div_table_dohod_ru.csv", index_col=0)

    df_curr.set_index('concat_column', inplace=True)
    df_curr.sort_index(inplace=True, na_position='last')


    # -----------------------------------
    #df_new.to_csv("Div_table_dohod_ru.csv")
    #df_new.to_csv("Test.csv")


    new_index = df_curr.index.append(df_new.index).drop_duplicates()
    df_curr_reind = df_curr.reindex(new_index, fill_value='nan')
    df_new_reind = df_new.reindex(new_index, fill_value='nan')

    #df_curr.set_index('concat_column', inplace=True)
    #df_curr.drop(df_curr.columns[0], inplace=True)
    #df_curr.sort_index(inplace=True, na_position='last')

    placeholder_1 = st.empty()
    placeholder_2 = st.empty()
    placeholder_3 = st.empty()
    placeholder_4 = st.empty()
    placeholder_5 = st.empty()
    placeholder_6 = st.empty()



    placeholder_1.header("Last saved version of the table: ")


    placeholder_2.dataframe(df_curr_reind)
    #st.write(df_curr_reind.shape)

    placeholder_3.header("Updated table (from web page): ")

    placeholder_4.dataframe(df_new_reind)
    #st.write(df_new_reind.shape)

    placeholder_5.header("Difference before and after: ")

    df_diff = compare_table(df_curr_reind.iloc[:, :-1], df_new_reind.iloc[:, :-1])


    placeholder_6.dataframe(df_diff)

    if df_diff.empty:
        text_message = "No changes in table"
    else:
        text_message = create_text_message(df_diff)
        df_new.reset_index(inplace=True)
        df_new.to_csv("Div_table_dohod_ru.csv")   # Update table in csv


    telegram_bot_sendtext(text_message)
    #print(test)

    time.sleep(60*60)
    placeholder_1.empty()
    placeholder_2.empty()
    placeholder_3.empty()
    placeholder_4.empty()
    placeholder_5.empty()
    placeholder_6.empty()



