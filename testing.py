from datetime import datetime as dt
from datetime import time as t
import pandas as pd
from pandas import DataFrame as df

from openpyxl import Workbook, load_workbook

pd.set_option('display.max_columns', None)  # буде відображати всі колонки
# pd.set_option('display.encoding', 'utf-8')  # буде в кодуванні utf-8

""""
отакий запис буде розкодовувати написане  у тому форматі що буде вказаний
#!/usr/bin/python
# -*- coding: windows-1251
"""
#
# a = {"a": "hello",
#      "b": "word"
#      }
#
# c = {"number": 6
#      }
#
# print("a+c = ", a.update(c))
# print("a+c = ", a | c)
#
# print(t(11,112,20))


df_reader = pd.read_excel('code_erroe_137.xlsx')
# print(reader.columns)
# print(reader['Unnamed: 8'].iloc[6:])


# eror_neznachni = df_reader[df_reader['Unnamed: 8'] == 'X'].iloc[6:40, [1, 3, 4, 8]]

nevidpovidnist_neznachni = df_reader[df_reader['Unnamed: 7'] == 'X']
nevidpovidnist_znachni = df_reader[df_reader['Unnamed: 8'] == 'X']
nevidpovidnist_nebezpechni = df_reader[df_reader['Unnamed: 9'] == 'X']

# збереження до файлу
nevidpovidnist_neznachni.to_excel("nevidpovidnist_neznachni.xlsx" )
nevidpovidnist_znachni.to_excel("nevidpovidnist_znachni.xlsx")
nevidpovidnist_nebezpechni.to_excel("nevidpovidnist_nebezpechni.xlsx")

# nevidpovidnist_neznachni.to_json('nevidpovidnist_neznachni.json',  orient = "records", force_ascii=False ,lines = True)
# nevidpovidnist_neznachni.to_json('nevidpovidnist_neznachni.json',  orient = "split", force_ascii=False )

