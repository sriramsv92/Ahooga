# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 20:30:35 2019

@author: Sriram Sivaraman
"""
import os

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



ahooga_tablexxx=pd.read_csv('ahooga_df.csv',index_col=False)
ahoo = pd.read_csv('ahooga_table_practice.csv')
for i in range(len(ahoo)):
    ahoo.loc[i,'Actual_quantity']=abs(int(ahoo.loc[i,'Actual_quantity']))
    
def date_month_split(dataframe2,column_to_split):
    #dataframe2 = dataframe[dataframe[column_to_split].notnull()]
    #dataframe2=dataframe2.reset_index(drop=True)
    table_name_month=column_to_split + '_' + 'month'
    table_name_year=column_to_split + '_' + 'year'
    
    
    
    for i in range(len(dataframe2)):
        split=dataframe2.loc[i,column_to_split].split('/')
       
        dataframe2.loc[i,table_name_month]=int(split[1])
        dataframe2.loc[i,table_name_year]=int(split[2])
       
        
        
        
    dataframe2=dataframe2.drop([column_to_split],axis=1)
    return dataframe2
    
ahoo=date_month_split(ahoo,'Created_date')
ahoo.to_csv('ahooga-cleaned.csv')
ahoo_product_bike=ahoo[ahoo['Product_group']=='Bike']

ahoo_product_component=ahoo[ahoo['Product_group']=='Component']

lms=list(ahoo_product_bike['Product_family'].unique())
df2 = pd.DataFrame()
for i in lms:
    ahoo2=ahoo_product_bike[ahoo_product_bike['Product_family']==i]
    df2=pd.concat([df2,ahoo2])
ahooga_product_bike_family=ahoo_product_bike[['Actual_quantity','Created_date_month','Product_family']]
grouped_ahoo_bike_family = ahooga_product_bike_family.groupby(['Created_date_month','Product_family'],as_index=False).count()
grouped_ahoo_bike_family.to_csv('grouped_ahoo_bike_family.csv',index=False)
app = dash.Dash(__name__)

server = app.server










app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ahoo_product_bike['Product_family'].unique()],
        value=(ahoo_product_bike['Product_family'].unique()),multi=True
    ),
    html.Div([dcc.Graph(id='feature-graphic', figure=go.Figure()),html.Div(id='output')])
    
])

@app.callback(Output('output', 'children'),
              [Input('dropdown', 'value')])

def update_output(value):

    for i in value:
        print(i)
    return value

if __name__ == '__main__':
    app.run_server(debug=True)