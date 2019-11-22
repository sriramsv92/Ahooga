# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:57:55 2019

@author: Sriram Sivaraman
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 00:34:52 2019

@author: Sriram Sivaraman
"""

import os
import base64
import dash_table
import dash_daq as daq
from six.moves.urllib.parse import quote
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import plotly.graph_objs as go
import plotly.express as px
from plotly.offline import plot
ahooga_bike_family=pd.read_csv('grouped_ahoo_bike_family.csv',index_col=False)
ahooga_component_family=pd.read_csv('grouped_ahoo_component_family.csv',index_col=False)
ahooga_bike_SKU=pd.read_csv('grouped_ahoo_bike_SKU.csv',index_col=False)
ahooga_component_SKU=pd.read_csv('grouped_ahoo_component_SKU.csv',index_col=False)
ahooga_tablex=pd.read_csv('ahooga-cleaned.csv',index_col=False)
from dash.exceptions import PreventUpdate
bikes_frame=ahooga_tablex[ahooga_tablex['Product_group']=='Bike']
bikes_frame = bikes_frame.reset_index(drop=True)
bikes_frame=bikes_frame[['Actual_quantity','Created_date_month','New_SKU_Name','Product_family']]
"""
href = "http://127.0.0.1:8050/page-2?a=test#quiz"
pathname = "/page-2"
search = "?a=test"
hash = "#quiz"
location = dcc.Location(id='url', refresh=False)
"""





#for i in range(len(bikes_frame)):
 #   v=str(bikes_frame.loc[i,'Created_date'])[2:4]
  #  bikes_frame.loc[i,'Created_date_month']=int(v)
dict={}
for i in bikes_frame['Product_family'].unique():
    data_frame=bikes_frame[bikes_frame['Product_family']==i]
    dict[i]=list(data_frame['New_SKU_Name'].unique())

names = list(dict.keys())
for i in dict.keys():
    dict[i].append('<All>')

image_filename = 'Ahooga.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

unique_bike_family=list(ahooga_bike_family['Product_family'].unique())
unique_bike_family.append('<All>')
unique_component_family=list(ahooga_component_family['Product_family'].unique())
unique_component_family.append('<All>')
unique_component_SKU=list(ahooga_component_SKU['New_SKU_Name'].unique())
unique_component_SKU.append('<All>')
#fig=px.bar(ahooga_tablexxx, x="Created_date_month", y="Actual_quantity", color='Product_family')

#plot(fig)

app = dash.Dash(__name__)

server = app.server
ahooga_bikes=ahooga_tablex[ahooga_tablex['Product_group']=='Bike']
ahooga_table=ahooga_bikes[['Actual_quantity','Product_family','New_SKU_Name','Created_date_month','Created_date_year']]
ahooga_table_group=ahooga_table[['Actual_quantity','New_SKU_Name']].groupby(['New_SKU_Name'],as_index=False).count()
ahooga_table_group_test=ahooga_table[['Actual_quantity','New_SKU_Name','Product_family']].groupby(['New_SKU_Name','Product_family'],as_index=False).count()
table_sum=ahooga_table_group['Actual_quantity'].sum()
for i in range(len(ahooga_table_group)):
    ahooga_table_group.loc[i,'SKU_Calculated_percent']=round((ahooga_table_group.loc[i,'Actual_quantity']/table_sum)*100,2)
ahooga_table_group['forecast']=ahooga_table_group['SKU_Calculated_percent']
    #ahooga_table_group.loc[i,'SKU_Calculated_percent']=ahooga_table_group.loc[i,'SKU_Calculated_percent']*100
unique_bike_sku=list(ahooga_table['New_SKU_Name'].unique())
unique_bike_sku.append('<All>')

"""
for i in ahooga_table_group['Product_family'].unique():
    temp_table=ahooga_table_group[ahooga_table_group['Product_family']==i]
    if len(temp_table)<8:
        ahooga_table_group=ahooga_table_group[ahooga_table_group['Product_family']!=i]
        nam=i
        temp_table2=temp_table
        lis=list(temp_table2['Created_date_month'].unique())
        lis2=[1,2,3,4,5,6,7,8]
        for j in lis2:
            if j not in lis:
                vkt=0
                
                temp_table2.loc[len(temp_table2)+0]=[i,j,2019,0,0]
                vkt+=1
"""                


dicts=ahooga_table_group.to_dict('records')
dicts2=pd.DataFrame.from_dict(dicts)             
x=[{'name':i,'value':i,'editable':False}for i in ahooga_table.columns]       
    
            

app.layout = html.Div(children=[html.H1('A dashboard for Ahooga'),html.Img(src='data:image/png;base64,{}'.format(encoded_image)),dcc.Tabs(id="tabs",
                             children=[dcc.Tab(label='Sales comparison',children=[
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in unique_bike_family],
        value='',multi=True
    ),
    dcc.Graph(id='graphic2',figure=go.Figure()),dcc.Dropdown(id='dropy',options=[{'label':name, 'value':name} for name in names],
            value = list(dict.keys())[0],clearable=False),dcc.Dropdown(id='dropy2',value='<All>',multi=True),
        dcc.Graph(id='test_graph',figure=go.Figure()),
    dcc.Dropdown(
        id='dropdown1',
        options=[{'label': i, 'value': i} for i in unique_component_family],
        value=ahooga_component_family['Product_family'].unique(),multi=True),
    dcc.Graph(id='graphic3',figure=go.Figure()),
     
             dcc.Dropdown(
        id='dropdown4',
        options=[{'label': i, 'value': i} for i in unique_component_SKU],
        value=ahooga_component_SKU['New_SKU_Name'].unique(),multi=True),
             dcc.Graph(id='graphic5',figure=go.Figure())
    
]),dcc.Tab(label='Forecasting Sales',children=[html.H4('An example table', style={'color': 'blue', 'fontSize': 14}),daq.BooleanSwitch(
  id='my-switch',
  on=False,label='turn on for including forecast manual percentage calculation',color='#9B51E0'
) , 
html.Div(id='filter_container'),html.Div(id='boolean-switch-output',style={'color': 'blue', 'fontSize': 24}),dash_table.DataTable(id='table',data=[],
        fixed_rows={ 'headers': True, 'data': 0 },style_table={'overflowX': 'scroll'},
         style_cell={'textAlign': 'right','minWidth': '30px', 'maxWidth': '300px','font_size': '20px'},
         style_cell_conditional=[{'if':{'column_id':'New_SKU_Name'},'textAlign':'left'},
                                 {'if':{'column_id':'Product_family'},'textAlign':'left'}],filter_action="native",),daq.BooleanSwitch(id='switch-2',on=False,
                                label='turn on for using SKU instead of bikes',color='blue'),daq.BooleanSwitch(id='switch-3',on=False,
                                label='turn on for adding an extra column for editing forecast',color='blue'),
 dash_table.DataTable(id='table2',data=[],
        fixed_rows={ 'headers': True, 'data': 0 },style_table={'overflowX': 'scroll'},
         style_cell={'textAlign': 'right','minWidth': '50px', 'maxWidth': '250px','font_size': '20px'},
         style_cell_conditional=[{'if':{'column_id':'New_SKU_Name'},'textAlign':'left'},
                                 {'if':{'column_id':'Product_family'},'textAlign':'left'}],filter_action="native",),html.H4('Select the bike family'),dcc.Dropdown(
        id='dropdown_family',
        options=[{'label': i, 'value': i} for i in unique_bike_family],
        value='<All>',multi=True
    ),html.H4('Select the SKU'),dcc.Dropdown(
        id='dropdown_family_sku',
        options=[{'label': i, 'value': i} for i in unique_bike_sku],
        value='<All>',multi=True
    ),html.A(
        'Download Data',
        id='download-link',
        download="rawdata.csv",
        href="",
        target="_blank"),dcc.Graph(id='graphic_actual',figure=go.Figure()),
        dcc.Graph(id='graphic_manual',figure=go.Figure()),])
            
])
             ])
ahooga_table_group=ahooga_table_group[['New_SKU_Name','SKU_Calculated_percent','forecast']]      
data2=ahooga_table_group[['New_SKU_Name','SKU_Calculated_percent']]

@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('table2', 'data')])
def data_download(data):
    df=pd.DataFrame(data)
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    return csv_string
    
        
    
@app.callback([
        Output('table2','data'),
        Output('table2','columns'),
],     [Input('switch-2','on'),
        Input('switch-3','on')])
    
def toggle_bikes_SKU(switch,switch2):
    if switch == True and switch2==False:
        data=ahooga_table[['Actual_quantity','New_SKU_Name','Created_date_month','Created_date_year']].groupby(['Created_date_year','Created_date_month','New_SKU_Name'],as_index=False).count()
        
        col = [{'name':i,'id':i,'editable':False}for i in data.columns]
        dat=data.to_dict('records')
        return dat,col
    elif switch == False and switch2 == False:
        data=ahooga_table[['Actual_quantity','Product_family','Created_date_month','Created_date_year']].groupby(['Created_date_year','Created_date_month','Product_family'],as_index=False).count()
        
        col = [{'name':i,'id':i,'editable':False}for i in data.columns]
        dat=data.to_dict('records')
        return dat,col
        
    elif switch == True and switch2== True:
        data=ahooga_table[['Actual_quantity','New_SKU_Name','Created_date_month','Created_date_year']].groupby(['Created_date_year','Created_date_month','New_SKU_Name'],as_index=False).count()
        data['manual_forecast']=data['Actual_quantity']
        col = [{'name':i,'id':i,'editable':False}for i in data.columns if i != 'manual_forecast']
        col.append({'name':'manual_forecast','id':'manual_forecast','editable':True})
        dat=data.to_dict('records')
        return dat,col
    else:
        data=ahooga_table[['Actual_quantity','Product_family','Created_date_month','Created_date_year']].groupby(['Created_date_year','Created_date_month','Product_family'],as_index=False).count()
        data['manual_forecast']=data['Actual_quantity']
        col = [{'name':i,'id':i,'editable':False}for i in data.columns if i != 'manual_forecast']
        col.append({'name':'manual_forecast','id':'manual_forecast','editable':True})
        dat=data.to_dict('records')
        return dat,col
        
        
        




@app.callback([
    Output('table', 'data'),
    Output('table', 'columns'),
], [Input('my-switch', 'on')])
def create_table(on):
    
    if on == True:
        columns=[
{'name':'New_SKU_Name' , 'id': 'New_SKU_Name', 'editable': False},
{'name':'SKU_Calculated_percent' , 'id': 'SKU_Calculated_percent', 'editable': False},
{'name':'forecast' , 'id': 'forecast', 'editable':True }
]
        data=ahooga_table_group.to_dict('records')
        
        return data, columns
            
        
    else:
        
        columns=[
{'name':'New_SKU_Name' , 'id': 'New_SKU_Name', 'editable': False},
{'name':'SKU_Calculated_percent' , 'id': 'SKU_Calculated_percent', 'editable': False},
]
        data=data2.to_dict('records')
        
        return data, columns
  


@app.callback(
        Output('boolean-switch-output','children'),
        [Input('table','data')],
        [State('my-switch','on')])
def calculation(date,on):
   
    if on == True:
        sumx=0
    
        for dat in range(len(date)):
            i=str((date[dat]['forecast']))
            for j in i:
                
                if j not in ['1','2','3','4','5','6','7','8','9','0','.']:
                    sums=0
                    return 'Wrong type %.5f'%(sums)
            sumx2 = float(date[dat]['forecast'])
            sumx+=sumx2
            sumx=round(sumx)
                
            
            
         
                
                
                
        if sumx>100:
            return 'The calculated sum is %.5f, please select a new value'%(sumx)
        else:
            return 'The calculated sum for forecast is %.5f'%(sumx)
    else:
        sumx1=0
        for i in range(len(date)):
            sumx21=float(date[i]['SKU_Calculated_percent'])
            sumx1 +=sumx21
            sumx1=round(sumx1)
        return 'The calculated sum for forecast is %.5f'%(sumx1)
        

"""          
             
@app.callback(
    Output('filter_container', "children"),
    [Input('Ahooga_table', "data")])
def update_graph(rows):
    if rows is None:
        dff = ahooga_table_group
    else:
        dff = pd.DataFrame(rows)

    return html.Div()        
"""
@app.callback(
    dash.dependencies.Output('dropy2', 'options'),
    [dash.dependencies.Input('dropy', 'value')]
)
def update_date_dropdown(name):
    if name =='':
        return []
    else:
        return [{'label': i, 'value': i} for i in dict[name]]      
@app.callback(
        [Output('graphic_manual','figure'),
        Output('graphic_actual','figure'), 
],      [Input('table2','data'),
        Input('table2','columns'),
        Input('dropdown_family_sku','value'),
        Input('dropdown_family','value')],
        [State('switch-2','on'),
        State('switch-3','on')])
def output(data,cols,value2,value,switch1,switch2):
    if switch1==False and switch2==False:
        if '<All>' in value:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Created_date_year','Created_date_month','Product_family','Actual_quantity']])
            datasets=['']
            family=list(ahooga_bike_family['Product_family'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product_family'] == fam]
                datasets.append(df_filtered)
    
            datasets.pop(0)
        elif '' in value or value==[]:
            ahooga_bike_family=pd.DataFrame(data,columns=[c['name'] for c in cols])
            datasets=['']
            family=list(ahooga_bike_family['Product_family'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product_family'] == fam]
                datasets.append(df_filtered)
            datasets.pop(0)
        else:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Created_date_year','Created_date_month','Product_family','Actual_quantity']])
            if type(value) == str:
                value= [value]
            datasets=['']
            for fam in value:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product_family'] == fam]
                datasets.append(df_filtered)
            datasets.pop(0)
        traces=['']
        for dataset in datasets:
            
            traces.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['Actual_quantity'],'type':'bar'
                              ,'name':list(dataset['Product_family'].unique())[0]
                              }))
        traces.pop(0)
        layout=go.Layout(barmode='stack', title = 'Per month grouped by family for bikes(actual)',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')
        layout2=go.Layout(barmode='stack', title = 'Per month grouped by family for bikes(predicted)',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')
         
        fig = {'data': traces, 'layout': layout}
        fig2 = {'data': traces, 'layout': layout2}
        
        return go.Figure(fig),go.Figure(fig2)
    
    elif switch1==False and switch2==True:
        if '<All>' in value:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Created_date_year','Created_date_month','Product_family','Actual_quantity','manual_forecast']])
            datasets=['']
            family=list(ahooga_bike_family['Product_family'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product_family'] == fam]
                datasets.append(df_filtered)
    
            datasets.pop(0)
        elif '' in value or value==[]:
            ahooga_bike_family=pd.DataFrame(data,columns=[c['name'] for c in cols])
            datasets=['']
            family=list(ahooga_bike_family['Product_family'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product_family'] == fam]
                datasets.append(df_filtered)
            datasets.pop(0)
        else:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Created_date_year','Created_date_month','Product_family','Actual_quantity','manual_forecast']])
            if type(value) == str:
                value= [value]
            datasets=['']
            for fam in value:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product_family'] == fam]
                datasets.append(df_filtered)
            datasets.pop(0)
        traces=['']
        traces2=['']
        for dataset in datasets:
            
            traces.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['Actual_quantity'],'type':'bar'
                              ,'name':list(dataset['Product_family'].unique())[0]
                              }))
            traces2.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['manual_forecast'],'type':'bar'
                              ,'name':list(dataset['Product_family'].unique())[0]
                              }))
        traces.pop(0)
        traces2.pop(0)
        layout1=go.Layout(barmode='stack', title = 'Per month grouped by family for bikes(actual)',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')
        layout2=go.Layout(barmode='stack', title = 'Per month grouped by family for bikes(predicted)',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')
         
        fig = {'data': traces, 'layout': layout1}
        fig2= {'data': traces2, 'layout': layout2}
        return go.Figure(fig),go.Figure(fig2)
        
            
    
            
    elif switch1==True and switch2==False:
        if '<All>' in value2:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Created_date_year','Created_date_month','New_SKU_Name','Actual_quantity']])
            datasets=['']
            family=list(ahooga_bike_family['New_SKU_Name'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['New_SKU_Name'] == fam]
                datasets.append(df_filtered)
    
            datasets.pop(0)
        elif '' in value2 or value2==[]:
            ahooga_bike_family=pd.DataFrame(data,columns=[c['name'] for c in cols])
            datasets=['']
            family=list(ahooga_bike_family['New_SKU_Name'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['New_SKU_Name'] == fam]
                datasets.append(df_filtered)
            datasets.pop(0)
        else:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Created_date_year','Created_date_month','New_SKU_Name','Actual_quantity']])
            if type(value2) == str:
                value2= [value2]
            datasets=['']
            for fam in value2:
                df_filtered = ahooga_bike_family[ahooga_bike_family['New_SKU_Name'] == fam]
                datasets.append(df_filtered)
            datasets.pop(0)
        traces=['']
        for dataset in datasets:
            
            traces.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['Actual_quantity'],'type':'bar'
                              ,'name':list(dataset['New_SKU_Name'].unique())[0]
                              }))
        traces.pop(0)
        layout=go.Layout(barmode='stack', title = 'Per month grouped by SKU for bikes(actual)',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')
        layout2=go.Layout(barmode='stack', title = 'Per month grouped by SKU for bikes(predicted)',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')
         
        fig = {'data': traces, 'layout': layout}
        fig2 = {'data': traces, 'layout': layout2}
        
        return go.Figure(fig),go.Figure(fig2)    
        
    else:
        if '<All>' in value2:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Created_date_year','Created_date_month','New_SKU_Name','Actual_quantity','manual_forecast']])
            datasets=['']
            family=list(ahooga_bike_family['New_SKU_Name'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['New_SKU_Name'] == fam]
                datasets.append(df_filtered)
    
            datasets.pop(0)
        elif '' in value2 or value2==[]:
            ahooga_bike_family=pd.DataFrame(data,columns=[c['name'] for c in cols])
            datasets=['']
            family=list(ahooga_bike_family['New_SKU_Name'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['New_SKU_Name'] == fam]
                datasets.append(df_filtered)
            datasets.pop(0)
        else:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Created_date_year','Created_date_month','New_SKU_Name','Actual_quantity','manual_forecast']])
            if type(value2) == str:
                value2 = [value2]
            datasets=['']
            for fam in value2:
                df_filtered = ahooga_bike_family[ahooga_bike_family['New_SKU_Name'] == fam]
                datasets.append(df_filtered)
            datasets.pop(0)
        traces=['']
        traces2=['']
        for dataset in datasets:
            
            traces.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['Actual_quantity'],'type':'bar'
                              ,'name':list(dataset['New_SKU_Name'].unique())[0]
                              }))
            traces2.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['manual_forecast'],'type':'bar'
                              ,'name':list(dataset['New_SKU_Name'].unique())[0]
                              }))
        traces.pop(0)
        traces2.pop(0)
        layout1=go.Layout(barmode='stack', title = 'Per month grouped by SKU for bikes(actual)',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')
        layout2=go.Layout(barmode='stack', title = 'Per month grouped by SKU for bikes(predicted)',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')
         
        fig = {'data': traces, 'layout': layout1}
        fig2= {'data': traces2, 'layout': layout2}
        return go.Figure(fig),go.Figure(fig2)

    
@app.callback(Output('graphic2', 'figure'),
              [Input('dropdown', 'value')])

def update_output(value):
    if '<All>' in value:
        datasets=['']
        family=list(ahooga_bike_family['Product_family'].unique())
        for fam in family:
            df_filtered = ahooga_bike_family[ahooga_bike_family['Product_family'] == fam]
            datasets.append(df_filtered)
        datasets.pop(0)
        
    
    elif '' in value or value==[]:
        datasets=['']
        family=list(ahooga_bike_family['Product_family'].unique())
        for fam in family:
            df_filtered = ahooga_bike_family[ahooga_bike_family['Product_family'] == fam]
            datasets.append(df_filtered)
        datasets.pop(0)
        
    else:
        if type(value) == str:
            value= [value]
        datasets=['']
        for fam in value:
             df_filtered = ahooga_bike_family[ahooga_bike_family['Product_family'] == fam]
             datasets.append(df_filtered)
        datasets.pop(0)       
    traces=['']
    for dataset in datasets:
        
        traces.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['Actual_quantity'],'type':'bar'
                              ,'name':list(dataset['Product_family'].unique())[0]
                              }))
        
        
    traces.pop(0)
    layout=go.Layout(barmode='stack', title = 'Per month grouped by family for bikes',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')

    fig = {'data': traces, 'layout': layout}
    return go.Figure(fig)
        
@app.callback(Output('graphic3', 'figure'),
              [Input('dropdown1', 'value')])

def update_output(value):
    if '<All>' in value:
        datasets=['']
        family=list(ahooga_component_family['Product_family'].unique())
        for fam in family:
            df_filtered = ahooga_component_family[ahooga_component_family['Product_family'] == fam]
            datasets.append(df_filtered)
        datasets.pop(0)
        
    
    elif '' in value or value==[]:
        datasets=['']
        family=list(ahooga_component_family['Product_family'].unique())
        for fam in family:
            df_filtered = ahooga_component_family[ahooga_component_family['Product_family'] == fam]
            datasets.append(df_filtered)
        datasets.pop(0)
    else:
        if type(value) == str:
            value= [value]
        datasets=['']
        for fam in value:
             df_filtered = ahooga_component_family[ahooga_component_family['Product_family'] == fam]
             datasets.append(df_filtered)
        datasets.pop(0)
    
        
        
        
    
    
    traces=['']
    for dataset in datasets:
        
        traces.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['Actual_quantity'],'type':'bar'
                              ,'name':list(dataset['Product_family'].unique())[0]
                              }))
        
        
    traces.pop(0)
    layout=go.Layout(barmode='stack', title = 'Per month grouped by family for components',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')

    fig = {'data': traces, 'layout': layout}
    return go.Figure(fig)
        


@app.callback(Output('graphic5', 'figure'),
              [Input('dropdown4', 'value')])

def update_output(value):
    if '<All>' in value:
        datasets=['']
        family=list(ahooga_component_SKU['New_SKU_Name'].unique())
        for fam in family:
            df_filtered = ahooga_component_SKU[ahooga_component_SKU['New_SKU_Name'] == fam]
            datasets.append(df_filtered)
        datasets.pop(0)
        
    elif '' in value or value==[]:
        datasets=['']
        family=list(ahooga_component_SKU['New_SKU_Name'].unique())
        for fam in family:
            df_filtered = ahooga_component_SKU[ahooga_component_SKU['New_SKU_Name'] == fam]
            datasets.append(df_filtered)
        datasets.pop(0)
    else:
        if type(value) == str:
            value= [value]
        datasets=['']
        for fam in value:
            df_filtered = ahooga_component_SKU[ahooga_component_SKU['New_SKU_Name'] == fam]
            datasets.append(df_filtered)
        datasets.pop(0)
    
    
    traces=['']
    for dataset in datasets:
        
        traces.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['Actual_quantity'],'type':'bar'
                              ,'name':list(dataset['New_SKU_Name'].unique())[0]
                              }))
        
        
    traces.pop(0)
    layout=go.Layout(barmode='stack', title = 'Per month grouped by SKU for component',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')

    fig = {'data': traces, 'layout': layout}
    return go.Figure(fig)
@app.callback(
    dash.dependencies.Output('dropy2', 'options'),
    [dash.dependencies.Input('dropy', 'value')]
)
def update_date_dropdown(name):
    if name =='':
        return []
    else:
        return [{'label': i, 'value': i} for i in dict[name]]      



@app.callback(
    Output('test_graph', 'figure'),
    [Input('dropy2', 'value'),
     Input('dropy', 'value')])
def update_graph(SKU, family):
    if '<All>' in SKU:
        df=bikes_frame[bikes_frame['Product_family']==family]
        nam=list(df['New_SKU_Name'].unique())
        datasets=['']
        for na in nam:
            df_filtered=bikes_frame[bikes_frame['New_SKU_Name']==na]
            datasets.append(df_filtered)
        datasets.pop(0)
        
    elif '' in SKU or SKU==[]:
        df=bikes_frame[bikes_frame['Product_family']==family]
        nam=list(df['New_SKU_Name'].unique())
        datasets=['']
        for na in nam:
            df_filtered=bikes_frame[bikes_frame['New_SKU_Name']==na]
            datasets.append(df_filtered)
        datasets.pop(0)
    else:
        if type(SKU) == str:
             SKU = [SKU]   
        datasets = ['']
        for SK in SKU:
            df_filtered=bikes_frame[bikes_frame['New_SKU_Name']==SK]
            datasets.append(df_filtered)
                 
        datasets.pop(0)
            
            
       
    # df_filtered[['Product_1', 'YearMonth']]
    
        
            
    #df_filtered = bikes_frame[bikes_frame['Product_family'] == family]
    
        
        
        
    
        
    traces = ['']
    for dataset in datasets:
        dataset=dataset.groupby(['Created_date_month','New_SKU_Name'],as_index=False).count()
        
        
        
        traces.append(
            go.Bar({
                'x': dataset['Created_date_month'],
                'y': dataset['Actual_quantity'],
                
                'name': list(dataset['New_SKU_Name'].unique())[0]
        }))
    traces.pop(0)
    layout=go.Layout(barmode='stack', title = 'Per month grouped by SKU for bikes',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold')

    fig = {'data': traces, 'layout': layout}
    return go.Figure(fig)

if __name__ == '__main__':
    app.run_server(debug=True)
    


        
    