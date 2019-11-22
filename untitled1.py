# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 09:17:17 2019

@author: Sriram Sivaraman
"""

import pandas as pd
ahooga_table=pd.read_csv('ahooga_table_practice.csv',index_col=False)
for i in range(len(ahooga_table)):
    table=ahooga_table.loc[i,'Created_date'].split('/')
    x=int(''.join(table))
    ahooga_table.loc[i,'Created_date']=x
        
ahooga_table.to_csv('ahooga_tablex.csv',index=False)

bikes_frame=ahooga_table[ahooga_table['Product_group']=='Bike']
dict={}
for i in bikes_frame['Product_family'].unique():
    data_frame=bikes_frame[bikes_frame['Product_family']==i]
    dict[i]=list(data_frame['New_SKU_Name'].unique())