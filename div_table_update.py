# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 03:59:45 2021

@author: User
"""

import pandas as pd
pd.set_option('display.max_columns', 150)
pd.set_option('display.max_rows', 300)
from bs4 import BeautifulSoup
import requests as req
import time
#from telegram.ext import Updater
#from telegram.ext import CommandHandler, CallbackContext
import config
from botFunctions import parse_div_table, compare_table, create_text_message


# ---------------Telegram API------------------

def telegram_bot_sendtext(bot_message):
    
    send_text = 'https://api.telegram.org/bot' + config.bot_token + '/sendMessage?chat_id=' + config.bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = req.get(send_text)

    return response.json()
    


while True:
    time.sleep(30)
    
    
    df_new = parse_div_table()
    #df_new.to_csv("Div_table_dohod_ru.csv")
    #df_new.to_csv("Test.csv")
    df_curr = pd.read_csv("Div_table_dohod_ru.csv", index_col=0)
    df_diff = compare_table(df_curr, df_new)
    
    if df_diff.empty:
        text_message = "No changes in table"
    else:
        text_message = create_text_message(df_diff)
    
        
    
    
    #text_message = create_text_message(df_diff)
    
    test = telegram_bot_sendtext(text_message)
    print(test)
    
    
# df_new = parse_div_table()
# df_new.to_csv("Div_table_dohod_ru.csv")
# df_curr = pd.read_csv("Div_table_dohod_ru.csv", index_col=0)
# df_new.to_csv("Test.csv")
# compare_table(df_curr, df_new)  # - Compare with previous table  
    # Send message to Telegram bot -------------
    
    
    # Send message to Telegram bot END----------
    
    #df_new.to_csv("Div_table_dohod_ru.csv")
    
    
    
    




#print(df_curr.compare(df_new, align_axis=0))



# - Generate an informational message about differences
# - Send message  
# - Rewrite table  