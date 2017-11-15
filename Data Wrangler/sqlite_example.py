# -*- coding: utf-8 -*-
"""
Created on Sat May 27 09:26:15 2017

@author: aruna
"""

import pandas as pd
import sqlite3

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("../data/hatecrimes.db")
df = pd.read_sql_query("SELECT state as State, agtype as Agency_type, agName as Agency_name,vRace,vRel,vSexOr from crimes", con)

# verify that result of SQL query is stored in the dataframe
print(df.head())

con.close()