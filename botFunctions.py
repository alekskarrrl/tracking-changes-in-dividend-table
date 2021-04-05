# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 05:38:13 2021

@author: User
"""
import pandas as pd
pd.set_option('display.max_columns', 150)
pd.set_option('display.max_rows', 300)
from bs4 import BeautifulSoup
import requests as req
#from telegram.ext import Updater
#from telegram.ext import CommandHandler, CallbackContext
import config



# - Parsing table by parse_div_table("https://www.dohod.ru/ik/analytics/dividend") 

# --------------definition parse_div_table -----------------------------
def parse_div_table():  # ready for using
    resp = req.get("https://www.dohod.ru/ik/analytics/dividend")
    soup = BeautifulSoup(resp.text, 'lxml')
    root = soup.tbody
    root_childs = [e for e in root.children if e.name is not None]
    div_table = pd.DataFrame(columns=['Акция', 'Сектор', 'Период', 'Выплата на акцию (прогноз)', 
                                  'Размер дивиденда рекомендован советом директоров', 'Валюта', 
                                  'Доходность выплаты', 'Цена расчета доходности', 'Дата закрытия реестра (оценка)', 
                                  'Дата закрытия реестра рекомендована советом директоров', 'Капитализация, млн.', 'DSI', 
                                  'Прогноз прибыли в след. 12m', 'Доля от прибыли', 'Кол-во акций в обращении, млн. шт.', 
                                  'Стабильность выплат', 'Стабильность роста', 'Комментарий/Див. политика'])
    i = 0
    for tr_child in root_childs:
        tr_child = [r for r in tr_child.find_all('td') if r.name is not None]
        div_table.loc[i] = [tr_child[j].text.strip() for j in range(0, 18)]
        for j in range(0, 18):
            if (j==4) or (j==9):
                if len(tr_child[j].find_all('span')) == 0:
                    div_table.loc[i][j] = 'No'
                else:
                    for n in range(0, len(tr_child[j].find_all('span'))):
                        if tr_child[j].find_all('span')[n]['title'] == 'Размер дивиденда рекомендован советом директоров':
                            div_table.loc[i][4] = 'Yes'
                        elif tr_child[j].find_all('span')[n]['title'] == 'Дата закрытия реестра под выплату дивидендов рекомендована советом директоров':
                            div_table.loc[i][9] = 'Yes'
                        else:
                            div_table.loc[i][j] = 'ERROR'
                #print(tr_child)
        i = i + 1
    div_table.replace({'n/a' : 'Nan'}, inplace=True)
    
    div_table['Выплата на акцию (прогноз)'] = div_table['Выплата на акцию (прогноз)'].astype('float').round(2)
    div_table['Цена расчета доходности'] = div_table['Цена расчета доходности'].astype('float').round(2)
    div_table['Дата закрытия реестра (оценка)'] = div_table['Дата закрытия реестра (оценка)'].astype('datetime64', errors='ignore')
    div_table['Капитализация, млн.'] = div_table['Капитализация, млн.'].astype('float').round(2)
    div_table['DSI'] = div_table['DSI'].astype('float').round(2)
    div_table['Прогноз прибыли в след. 12m'] = div_table['Прогноз прибыли в след. 12m'].astype('float').round(2)
    div_table['Доля от прибыли'] = div_table['Доля от прибыли'].astype('float').round(2)
    div_table['Кол-во акций в обращении, млн. шт.'] = div_table['Кол-во акций в обращении, млн. шт.'].astype('float').round(2)
    
    div_table.sort_values(by=['Акция', 'Сектор', 'Период'], inplace=True)
    div_table.reset_index(drop=True, inplace=True)
    return  div_table
    
# --------------definition parse_div_table END -----------------------------


# --------------definition compare_table -----------------------------

def compare_table(df_curr, df_new):
    if df_curr.compare(df_new, align_axis=0, keep_equal=True).empty:
        #print("No changes in table")
        return pd.DataFrame()
    else:
        df_mask_fill = df_curr.compare(df_new, align_axis=0, keep_shape = True, keep_equal=True)
        df_mask = df_curr.compare(df_new, align_axis=0, keep_shape = True)
        df_diff_short = df_mask[df_mask.notna().sum(axis=1) > 0]
        list_ind = df_diff_short.index.values
        #len(list_ind)
        ind_lvl_1 = []
        for i in range(0, len(list_ind)):
            #print(list_ind[i][0])
            if list_ind[i][0] not in ind_lvl_1:
                ind_lvl_1.append(list_ind[i][0])
                #print(ind_lvl_1)
         
        return df_diff_short.combine_first(df_mask_fill.loc[ind_lvl_1])        
         
    
    


# --------------definition compare_table  END -----------------------------


#-------------------create_text_message--------------------------------

def create_text_message(df):
    text = ''
    list_ind = df.index.values
    ind_lvl_1 = []
    for i in range(0, len(list_ind)):
        if list_ind[i][0] not in ind_lvl_1:
            ind_lvl_1.append(list_ind[i][0])
                
    for ind in ind_lvl_1:
        show_stock_name = True
        for col in df.columns.values:
            if (df.loc[(ind, 'self'), col] != df.loc[(ind, 'other'), col]):
                if show_stock_name:
                    text = text + str(df.loc[(ind, 'self'), 'Акция']) + ': \n'
                text = text + col +': ' + 'before ' + str(df.loc[(ind, 'self'), col]) + ', now ' +  str(df.loc[(ind, 'other'), col]) + '\n'
                show_stock_name = False
        text = text + '\n'
        #print(ind_lvl_1)
    return text






#-------------------create_text_message END------------------------------------