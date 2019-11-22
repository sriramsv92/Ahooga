# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 12:59:01 2019

@author: Sriram Sivaraman
"""
import pandas as pd
ahoo=pd.read_csv('ahooga-cleaned.csv')

ahoo_component=ahoo[ahoo['Product_group']=='Component']
ahoo_bike=ahoo[ahoo['Product_group']=='Bike']
ahooga_product_bike_family=ahoo_bike[['Actual_quantity','Created_date_month','Product_family']]
grouped_ahoo_bike_family = ahooga_product_bike_family.groupby(['Created_date_month','Product_family'],as_index=False).count()
grouped_ahoo_bike_family.to_csv('grouped_ahoo_bike_family.csv',index=False)
ahooga_product_component_family=ahoo_component[['Actual_quantity','Created_date_month','Product_family']]
grouped_ahoo_component_family = ahooga_product_component_family.groupby(['Created_date_month','Product_family'],as_index=False).count()
grouped_ahoo_component_family.to_csv('grouped_ahoo_component_family.csv',index=False)
ahooga_product_bike_SKU=ahoo_bike[['Actual_quantity','Created_date_month','New_SKU_Name']]
grouped_ahoo_bike_SKU = ahooga_product_bike_SKU.groupby(['Created_date_month','New_SKU_Name'],as_index=False).count()
grouped_ahoo_bike_SKU.to_csv('grouped_ahoo_bike_SKU.csv',index=False)

ahooga_product_component_SKU=ahoo_component[['Actual_quantity','Created_date_month','New_SKU_Name']]
grouped_ahoo_component_SKU = ahooga_product_component_SKU.groupby(['Created_date_month','New_SKU_Name'],as_index=False).count()
grouped_ahoo_component_SKU.to_csv('grouped_ahoo_component_SKU.csv',index=False)