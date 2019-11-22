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
dictsx={}
for i in bikes_frame['Product_family'].unique():
    data_frame=bikes_frame[bikes_frame['Product_family']==i]
    dict[i]=list(data_frame['New_SKU_Name'].unique())
    dictsx[i]=list(data_frame['New_SKU_Name'].unique())

names = list(dict.keys())
names2= list(dict.keys())
names2.append('<All>')
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
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#plot(fig)

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

server = app.server
ahooga_bikes=ahooga_tablex[ahooga_tablex['Product_group']=='Bike']
ahooga_table=ahooga_bikes[['Actual_quantity','Product_family','New_SKU_Name','Created_date_month','Created_date_year']]
ahooga_tidy=ahooga_bikes[['Actual_quantity','Product_family','New_SKU_Name','Created_date_month','Created_date_year']]
ahooga_tidy=ahooga_tidy.groupby(['Created_date_year','Created_date_month','Product_family','New_SKU_Name'],as_index=False).count()
#ahooga_tidy.to_csv('ahooga_tidy.csv',index=False)
ahooga_table_group=ahooga_table[['Actual_quantity','New_SKU_Name']].groupby(['New_SKU_Name'],as_index=False).count()
ahooga_table_group_test=ahooga_table[['Actual_quantity','New_SKU_Name','Product_family']].groupby(['New_SKU_Name','Product_family'],as_index=False).count()
table_sum=ahooga_table_group['Actual_quantity'].sum()
for i in range(len(ahooga_table_group)):
    ahooga_table_group.loc[i,'SKU_Calculated_percent']=round((ahooga_table_group.loc[i,'Actual_quantity']/table_sum)*100,2)
ahooga_table_group['forecast']=ahooga_table_group['SKU_Calculated_percent']
    #ahooga_table_group.loc[i,'SKU_Calculated_percent']=ahooga_table_group.loc[i,'SKU_Calculated_percent']*100

ahooga_tidy2=pd.read_csv('ahooga_tidy.csv',index_col=False)
ahooga_tidy3=ahooga_tidy2.groupby(['New_SKU_Name'],as_index=False).sum()

table_sum2=ahooga_tidy3['Actual_quantity'].sum()
for i in range(len(ahooga_tidy3)):
    ahooga_tidy3.loc[i,'Actual growth SKU']=round((ahooga_tidy3.loc[i,'Actual_quantity']/table_sum2)*100,2)
ahooga_tidy3['Forecasted SKU growth']=ahooga_tidy3['Actual growth SKU']

ahooga_tidy3.columns=['SKU Name','Created Year','Created Month','Bikes Sold','% of total sales','Manual input % of total sales']










unique_bike_sku=list(ahooga_table['New_SKU_Name'].unique())
unique_bike_sku2=list(ahooga_table['New_SKU_Name'].unique())
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
    
sku_names=list(ahooga_table_group['New_SKU_Name'].unique()) 
sku_names.append('<All>')        

app.layout = html.Div(children=[html.Div([html.Img(src='https://ahooga.bike/wp-content/uploads/2018/07/Ahooga-Logo-HO-White-2019-uai-516x141.png'),
                                        html.H2('Ahooga Forecasting tool'),],style={'width':'100%','display': 'inline-block','backgroundColor':'black','color':'white','fontFamily':'helvetica'})
    ,
                     dcc.Tabs(id="tabs",
                             children=[dcc.Tab(label='Historical Sales Dashboard',children=[html.H2('Bikes'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in unique_bike_family],
        value='',multi=True,style={'color':'black','backgroundColor':'white'}
    ),
    dcc.Graph(id='graphic2',figure=go.Figure()),dcc.Dropdown(id='dropy',options=[{'label':name, 'value':name} for name in names2],
            value = list(dict.keys())[0],clearable=False,
            style=
            {'color':'black','backgroundColor':'white'}),dcc.Dropdown(id='dropy2',value='<All>',
            multi=True,style={'color':'black','backgroundColor':'white'}),
        dcc.Graph(id='test_graph',figure=go.Figure()),html.H2('Components'),
    dcc.Dropdown(
        id='dropdown1',
        options=[{'label': i, 'value': i} for i in unique_component_family],
        value=ahooga_component_family['Product_family'].unique(),multi=True
        ,style={'color':'black','backgroundColor':'white'}),
    dcc.Graph(id='graphic3',figure=go.Figure()),
     
             dcc.Dropdown(
        id='dropdown4',
        options=[{'label': i, 'value': i} for i in unique_component_SKU],
        value=ahooga_component_SKU['New_SKU_Name'].unique(),multi=True,style={'color':'black','backgroundColor':'white'}),
             dcc.Graph(id='graphic5',figure=go.Figure()),
    
],style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold','color':'black'
},

selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}),dcc.Tab(label='Interactive Forecasting Tool',children=[html.P(['The forecast is calculated as  follows:',
        html.Br(), "1. Assume last year's growth, or input growth manually.",
        html.Br(), "2. Assume last year's product mix per SKU or per family, or change manually if needed.",
        html.Br()," 3. Review forecast (table or graph), adjust manually if needed"],style={'color':'black','font':'helveltica','fontSize':20}), 
        html.Div([html.Div([html.H6(id='total bikes'),html.P('No of bikes sold')],
                            id='bikes',className='row',style={'marginLeft':500}),
                  html.Div([html.H6(id='manual growth input'),html.P('Manual Growth Input')],
                            id='growth',className='two columns',
                            style={'marginLeft':700,'marginBottom':1}),],id="rowf",
                            className="row",),
                  
                  
                html.Div([daq.BooleanSwitch(
  id='my-switch',
  on=False,label='turn on for including forecast manual percentage calculation',color='#9B51E0'
,style={'marginLeft':1250,'marginTop':50,'marginBottom':-100})],style={'display': 'inline-block'}) , 
html.Div(id='filter_container'),html.Div(id='boolean-switch-output',style={'color': 'blue', 'fontSize': 24}),dash_table.DataTable(id='table',data=[],
        fixed_rows={ 'headers': True, 'data': 0 },style_table={'overflowX': 'scroll','maxHeight':'300px','maxWidth':'1300px'},
         style_cell={'textAlign': 'right','minWidth': '30px', 'maxWidth': '250px','font_size': '20px',
                     'color':'black','backgroundColor':'white'},
         style_cell_conditional=[{'if':{'column_id':'SKU Name'},'textAlign':'left'},
                                 {'if':{'column_id':'Product Family'},'textAlign':'left'}],filter_action="native",
                                 style_header={'backgroundColor': 'white'}
                                 ),daq.BooleanSwitch(id='switch-2',on=False,
                                label='turn on for using SKU instead of bikes',color='blue',
                                style={'marginLeft':1250,'marginTop':10,'marginBottom':-30}),daq.BooleanSwitch(id='switch-3',on=False,
                                label='turn on for adding an extra column for editing forecast',color='blue',
                                style={'marginLeft':1250,'marginTop':50,'marginBottom':-1}),html.Div(
                                        [
                                                
 dash_table.DataTable(id='table2',data=[],
        fixed_rows={ 'headers': True, 'data': 0 },style_table={'overflowX': 'scroll','maxHeight':'300px','maxWidth':'1300px'},
         style_cell={'textAlign': 'right','minWidth': '50px', 'maxWidth': '200px','font_size': '20px','color':'black','backgroundColor':'white'},
         style_cell_conditional=[{'if':{'column_id':'SKU Name'},'textAlign':'left'},
                                 {'if':{'column_id':'Product Family'},'textAlign':'left'}],filter_action="native",
                                 style_header={'backgroundColor': 'white'}),],className='row',style={'marginLeft':300}),html.Div(
                      
        [html.A(html.Button('Download as csv file',id='button'),id='download-link',
        download="ahooga_datafile.csv",
        href="",
        target="_blank",style={'textAlign':'center'})],className='row',style={'marginTop':-50}),html.H4('Select the bike family'),dcc.Dropdown(
        id='dropdown_family',
        options=[{'label': i, 'value': i} for i in unique_bike_family],
        value='<All>',multi=True
    ),html.H4('Select the SKU'),dcc.Dropdown(id='dropyx',options=[{'label':name, 'value':name} for name in names2]
    ,value = list(dict.keys())[0],clearable=False),
                      dcc.Dropdown(
        id='dropdown_family_sku',
        value='<All>',multi=True
    ),dcc.Graph(id='graphic_actual',figure=go.Figure()),
        dcc.Graph(id='graphic_manual',figure=go.Figure()),],style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold','color':'black'
},

selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}),

            
],style={'display': 'inline-block'})
             ],style={'fontFamily':'helvetica','backgroundColor':'lightgrey','color':'black'})
ahooga_table_group=ahooga_table_group[['New_SKU_Name','SKU_Calculated_percent','forecast']]      
data2=ahooga_table_group[['New_SKU_Name','SKU_Calculated_percent']]

@app.callback(
        [Output('total bikes','children'),
         Output('manual growth input','children'),
],      [Input('table2','data'),
],      [State('switch-3','on')])
def bikes_sold(data,switch):
    if switch==True:
        sumx=0
        for i in range(len(data)):
            sums=int(data[i]['Forecast Bikes Sold'])
            sumx+=sums
        sumxx=sumx/1000
        return sumx,sumxx
    else:
        sumx=0
        for i in range(len(data)):
            sums=int(data[i]['Bikes Sold'])
            sumx+=sums
        sumxx=sumx/1000
        return sumx,sumxx
        
        

@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('table2', 'data')])
def data_download(data):
    df=pd.DataFrame(data)
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    return csv_string
    
ahooga_tidy2.columns=['Year','Month','Product Family','SKU Name','Bikes Sold']        
    
@app.callback([
        Output('table2','data'),
        Output('table2','columns'),
],     [Input('switch-2','on'),
        Input('switch-3','on')])
    
def toggle_bikes_SKU(switch,switch2):
    if switch == True and switch2==False:
        data=ahooga_tidy2.groupby(['Year','Month','Product Family','SKU Name'],as_index=False).sum()
        data=data[data['Month']>7]
        col = [{'name':i,'id':i,'editable':False,'hideable':False} if i!='Product Family' else {'name':i,'id':i,'editable':False,'hideable':True} for i in data.columns]
        dat=data.to_dict('records')
        return dat,col
    elif switch == False and switch2 == False:
        data=ahooga_tidy2[['Bikes Sold','Product Family','Year','Month']].groupby(['Year','Month','Product Family'],as_index=False).sum()
        data=data[data['Month']>7]
        col = [{'name':i,'id':i,'editable':False}for i in data.columns]
        dat=data.to_dict('records')
        return dat,col
        
    elif switch == True and switch2== True:
        data=ahooga_tidy2.groupby(['Year','Month','Product Family','SKU Name'],as_index=False).sum()
        
        data=data[data['Month']>7]
        col = [{'name':i,'id':i,'editable':False,'hideable':False} if i!='Product Family' else {'name':i,'id':i,'editable':False,'hideable':True} for i in data.columns]
        data['Forecast Bikes Sold']=data['Bikes Sold']
        col.append({'name':'Forecast Bikes Sold','id':'Forecast Bikes Sold','editable':True,'hideable':False})
        dat=data.to_dict('records')
        return dat,col
    else:
        data=ahooga_tidy2[['Bikes Sold','Product Family','Month','Year']].groupby(['Year','Month','Product Family'],as_index=False).sum()
        data['Forecast Bikes Sold']=data['Bikes Sold']
        data=data[data['Month']>7]
        col = [{'name':i,'id':i,'editable':False}for i in data.columns if i != 'Forecast Bikes Sold']
        col.append({'name':'Forecast Bikes Sold','id':'Forecast Bikes Sold','editable':True})
        dat=data.to_dict('records')
        return dat,col
        
        
@app.callback([
    Output('table', 'data'),
    Output('table', 'columns'),
], [Input('my-switch', 'on')])
def create_table(on):
    
    if on == True:
        columns=[
{'name':'SKU Name' , 'id': 'SKU Name', 'editable': False},
{'name':'% of total sales' , 'id': '% of total sales', 'editable': False},
{'name':'Manual input % of total sales' , 'id': 'Manual input % of total sales', 'editable':True }
]
        data=ahooga_tidy3.to_dict('records')
        
        return data, columns
            
        
    else:
        
        columns=[
{'name':'SKU Name' , 'id': 'SKU Name', 'editable': False},
{'name':'% of total sales' , 'id': '% of total sales', 'editable': False},
]
        data=ahooga_tidy3.to_dict('records')
        
        return data, columns
  


@app.callback(
        Output('boolean-switch-output','children'),
        [Input('table','data')],
        [State('my-switch','on')])
def calculation(date,on):
   
    if on == True:
        sumx=0
    
        for dat in range(len(date)):
            i=str((date[dat]['Manual input % of total sales']))
            for j in i:
                
                if j not in ['1','2','3','4','5','6','7','8','9','0','.']:
                    sums=0
                    return 'Wrong type %.1f'%(sums)
            sumx2 = float(date[dat]['Manual input % of total sales'])
            sumx+=sumx2
            sumx=round(sumx)
        if sumx>100:
            return 'The calculated percentage is %4d %s, please select a new value'%(int(sumx),'%')
        else:
            return 'The calculated percentage for forecast is %4d %s'%(int(sumx),'%')
    else:
        sumx1=0
        for i in range(len(date)):
            sumx21=float(date[i]['% of total sales'])
            sumx1 +=sumx21
            sumx1=round(sumx1)
        return 'The calculated percentage for forecast is %4d %s'%(int(sumx1),'%')
        

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

dict_2={}
dictsx_2={}
for i in ahooga_tidy2['Product Family'].unique():
    data_frame2=ahooga_tidy2[ahooga_tidy2['Product Family']==i]
    dict_2[i]=list(data_frame2['SKU Name'].unique())
    dictsx_2[i]=list(data_frame2['SKU Name'].unique())
    dictsx_2[i].append('<All>')

sku_names_x= list(ahooga_tidy2['SKU Name'].unique())
sku_names_x.append('<All>')
@app.callback(
    dash.dependencies.Output('dropdown_family_sku', 'options'),
    [dash.dependencies.Input('dropyx', 'value')]
)
def update_date_dropdown(name):
    if name =='':
        return [{'label': i, 'value': i} for i in sku_names_x]
    elif name=='<All>':
        return [{'label': i, 'value': i} for i in sku_names_x]
    else:
        return [{'label': i, 'value': i} for i in dictsx_2[name]]   
    
ahooga_actual=ahooga_tidy[ahooga_tidy['Created_date_month']<8]
ahooga_actual.columns=['Year','Month','Product Family','SKU Name','Bikes Sold']
ahooga_actual=ahooga_actual.groupby(['Year','Month','Product Family','SKU Name'],as_index=False).sum()
    

@app.callback(
        [Output('graphic_manual','figure'),
        Output('graphic_actual','figure'), 
],      [Input('table2','data'),
        Input('table2','columns'),
        Input('dropdown_family_sku','value'),
        Input('dropyx','value'),
        Input('dropdown_family','value')],
        [State('switch-2','on'),
        State('switch-3','on')])
def output(data,cols,value2,value3,value,switch1,switch2):
    if switch1==False and switch2==False:
        if '<All>' in value:
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','Product Family'],as_index=False).sum()
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Year','Month','Product Family','Bikes Sold']])
            
            datasets=['']
            datasets2=['']
            family=list(ahooga_bike_family['Product Family'].unique())
            family2=list(ahooga_actual2['Product Family'].unique())
            
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product Family'] == fam]
                datasets.append(df_filtered)
            for fam in family2:
                df_filtered = ahooga_actual2[ahooga_actual2['Product Family'] == fam]
                datasets2.append(df_filtered)
    
            datasets.pop(0)
            datasets2.pop(0)
        elif '' in value or value==[]:
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','Product Family'],as_index=False).sum()
            ahooga_bike_family=pd.DataFrame(data,columns=[c['name'] for c in cols])
            datasets=['']
            datasets2=['']
            family=list(ahooga_bike_family['Product Family'].unique())
            family2=list(ahooga_actual2['Product Family'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product Family'] == fam]
                datasets.append(df_filtered)
            for fam in family2:
                df_filtered = ahooga_actual2[ahooga_actual2['Product Family'] == fam]
                datasets2.append(df_filtered)
            datasets.pop(0)
            datasets2.pop(0)
        else:
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','Product Family'],as_index=False).sum()
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Year','Month','Product Family','Bikes Sold']])
            if type(value) == str:
                value= [value]
            datasets=['']
            datasets2=['']
            for fam in value:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product Family'] == fam]
                df_filtered2=ahooga_actual2[ahooga_actual2['Product Family']==fam]
                datasets.append(df_filtered)
                datasets2.append(df_filtered2)
            datasets.pop(0)
            datasets2.pop(0)
        traces=['']
        traces2=['']
        for dataset in datasets2:
             
            
             traces.append(go.Bar({'x':dataset['Month'],'y':dataset['Bikes Sold'],'type':'bar'
                              ,'name':list(dataset['Product Family'].unique())[0]
                              }))
        for dataset in datasets:
             traces2.append(go.Bar({'x':dataset['Month'],'y':dataset['Bikes Sold'],'type':'bar'
                              ,'name':list(dataset['Product Family'].unique())[0]
                              }))
        traces.pop(0)
        traces2.pop(0)
        layout=go.Layout(barmode='stack', title = 'Per month grouped by family for bikes(actual)',
                         xaxis_title='The Month of the year',yaxis_title='Number of bikes sold',plot_bgcolor='white',
                paper_bgcolor='white',)
        layout2=go.Layout(barmode='stack', title = 'Per month grouped by family for bikes(predicted)',
                          xaxis_title='The Month of the year',yaxis_title='Number of bikes sold',plot_bgcolor='white',
                paper_bgcolor='white',)
         
        fig = {'data': traces, 'layout': layout}
        fig2 = {'data': traces2, 'layout': layout2}
        
        return go.Figure(fig),go.Figure(fig2)
    
    elif switch1==False and switch2==True:
        if '<All>' in value:
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','Product Family'],as_index=False).sum()
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Year','Month','Product Family','Bikes Sold','Forecast Bikes Sold']])
            datasets=['']
            datasets2=['']
            family=list(ahooga_bike_family['Product Family'].unique())
            family2=list(ahooga_actual2['Product Family'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product Family'] == fam]
                datasets.append(df_filtered)
            for fam in family2:
                df_filtered = ahooga_actual2[ahooga_actual2['Product Family'] == fam]
                datasets2.append(df_filtered)
    
            datasets.pop(0)
            datasets2.pop(0)
        elif '' in value or value==[]:
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','Product Family'],as_index=False).sum()
            ahooga_bike_family=pd.DataFrame(data,columns=[c['name'] for c in cols])
            datasets=['']
            datasets2=['']
            family=list(ahooga_bike_family['Product Family'].unique())
            family2=list(ahooga_actual2['Product Family'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product Family'] == fam]
                datasets.append(df_filtered)
            for fam in family2:
                df_filtered = ahooga_actual2[ahooga_actual2['Product Family'] == fam]
                datasets2.append(df_filtered)
            datasets.pop(0)
            datasets2.pop(0)
        else:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Year','Month','Product Family','Bikes Sold','Forecast Bikes Sold']])
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','Product Family'],as_index=False).sum()
            if type(value) == str:
                value= [value]
            datasets=['']
            datasets2=['']
            for fam in value:
                df_filtered = ahooga_bike_family[ahooga_bike_family['Product Family'] == fam]
                df_filtered2 = ahooga_actual2[ahooga_actual2['Product Family'] == fam]
                datasets.append(df_filtered)
                datasets2.append(df_filtered2)
            datasets.pop(0)
            datasets2.pop(0)
        traces=['']
        traces2=['']
        for dataset in datasets2:
            
            
            
            traces.append(go.Bar({'x':dataset['Month'],'y':dataset['Bikes Sold'],'type':'bar'
                              ,'name':list(dataset['Product Family'].unique())[0]
                              }))
        for dataset in datasets:
            traces2.append(go.Bar({'x':dataset['Month'],'y':dataset['Forecast Bikes Sold'],'type':'bar'
                              ,'name':list(dataset['Product Family'].unique())[0]
                              }))
        traces.pop(0)
        traces2.pop(0)
        layout1=go.Layout(barmode='stack', title = 'Per month grouped by family for bikes(actual)',
                          xaxis_title='The Month of the year',yaxis_title='Number of bikes sold'
                          ,plot_bgcolor='white',
                paper_bgcolor='white',)
        layout2=go.Layout(barmode='stack', title = 'Per month grouped by family for bikes(predicted)',
                          xaxis_title='The Month of the year',yaxis_title='Number of bikes sold'
                          ,plot_bgcolor='white',
                paper_bgcolor='white',)
         
        fig = {'data': traces, 'layout': layout1}
        fig2= {'data': traces2, 'layout': layout2}
        return go.Figure(fig),go.Figure(fig2)
        
            
    
            
    elif switch1==True and switch2==False:
        if '<All>' in value3:
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','SKU Name'],as_index=False).sum()
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Year','Month','SKU Name','Bikes Sold']])
            if '<All>' in value2:
                datasets=['']
                datasets2=['']
                df=ahooga_tidy2
                df2=ahooga_actual2
                family=list(df['SKU Name'].unique())
                family2=list(df2['SKU Name'].unique())
                
                for fam in family:
                     df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                     datasets.append(df_filtered)
                for fam in family2:
                     df_filtered = ahooga_actual2[ahooga_actual2['SKU Name'] == fam]
                     datasets2.append(df_filtered)
                datasets.pop(0)
                datasets2.pop(0)
            elif '' in value2 or value2==[]:
                datasets=['']
                datasets2=['']
                df=ahooga_tidy2
                df2=ahooga_actual2
                family=list(df['SKU Name'].unique())
                family2=list(df2['SKU Name'].unique())
                for fam in family:
                    df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                    datasets.append(df_filtered)
                datasets.pop(0)
                for fam in family2:
                     df_filtered = ahooga_actual2[ahooga_actual2['SKU Name'] == fam]
                     datasets2.append(df_filtered)
                datasets2.pop(0)
            else:
                if type(value2) == str:
                    value2= [value2]
                datasets=['']
                datasets2=['']
                for fam in value2:
                    df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                    df_filtered2= ahooga_actual2[ahooga_actual2['SKU Name'] == fam]
                    datasets.append(df_filtered)
                    datasets2.append(df_filtered2)
                datasets.pop(0)
                datasets2.pop(0)
        elif '<All>' in value2:
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','SKU Name'],as_index=False).sum()
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Year','Month','SKU Name','Bikes Sold']])
            datasets=['']
            datasets2=['']
            df=ahooga_tidy2[ahooga_tidy2['Product Family']==value3]
            df2=ahooga_actual[ahooga_actual['Product Family']==value3]
            family=list(df['SKU Name'].unique())
            family2=list(df2['SKU Name'].unique())
            #family=list(ahooga_bike_family['New_SKU_Name'].unique())
            
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                datasets.append(df_filtered)
            for fam in family2:
                df_filtered2 = ahooga_actual2[ahooga_actual2['SKU Name'] == fam]
                datasets2.append(df_filtered2)   
    
            datasets.pop(0)
            datasets2.pop(0)
        elif '' in value2 or value2==[]:
            ahooga_bike_family=pd.DataFrame(data,columns=[c['name'] for c in cols])
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','SKU Name'],as_index=False).sum()
            datasets=['']
            datasets2=['']
            df=ahooga_tidy2[ahooga_tidy2['Product Family']==value3]
            df2=ahooga_actual[ahooga_actual['Product Family']==value3]
            family=list(df['SKU Name'].unique())
            family2=list(df2['SKU Name'].unique())
            #family=list(ahooga_bike_family['New_SKU_Name'].unique())
            #family=dictsx[value3]
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                datasets.append(df_filtered)
            datasets.pop(0)
            for fam in family2:
                df_filtered = ahooga_actual2[ahooga_actual2['SKU Name'] == fam]
                datasets2.append(df_filtered)   
            datasets2.pop(0)
        else:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Year','Month','SKU Name','Bikes Sold']])
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','SKU Name'],as_index=False).sum()
            if type(value2) == str:
                value2= [value2]
            datasets=['']
            datasets2=['']
            for fam in value2:
                df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                df_filtered2 = ahooga_actual2[ahooga_actual2['SKU Name'] == fam]
                datasets.append(df_filtered)
                datasets2.append(df_filtered2)
            datasets.pop(0)
            datasets2.pop(0)
        traces=['']
        traces2=['']
        for dataset in datasets2:
            
            
            traces.append(go.Bar({'x':dataset['Month'],'y':dataset['Bikes Sold'],'type':'bar'
                              ,'name':list(dataset['SKU Name'].unique())[0]
                              }))
        for dataset in datasets:
            traces2.append(go.Bar({'x':dataset['Month'],'y':dataset['Bikes Sold'],'type':'bar'
                              ,'name':list(dataset['SKU Name'].unique())[0]
                              }))
        traces.pop(0)
        traces2.pop(0)
        layout=go.Layout(barmode='stack', title = 'Per month grouped by SKU for bikes(actual)',
                         xaxis_title='The Month of the year',yaxis_title='Number of bikes sold'
                         ,plot_bgcolor='white',
                paper_bgcolor='white',)
        layout2=go.Layout(barmode='stack', title = 'Per month grouped by SKU for bikes(predicted)',
                          xaxis_title='The Month of the year',yaxis_title='Number of bikes sold'
                          ,plot_bgcolor='white',
                paper_bgcolor='white',)
         
        fig = {'data': traces, 'layout': layout}
        fig2 = {'data': traces2, 'layout': layout2}
        
        return go.Figure(fig),go.Figure(fig2)    
        
    else:
        if '<All>' in value3:
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','SKU Name'],as_index=False).sum()
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Year','Month','SKU Name','Bikes Sold','Forecast Bikes Sold']])
            if '<All>' in value2:
                datasets=['']
                datasets2=['']
                df=ahooga_tidy2
                df2=ahooga_actual2
                family=list(df['SKU Name'].unique())
                family2=list(df2['SKU Name'].unique())
                for fam in family:
                     df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                     datasets.append(df_filtered)
                for fam in family2:
                     df_filtered = ahooga_actual2[ahooga_actual2['SKU Name'] == fam]
                     datasets2.append(df_filtered)
                
                datasets.pop(0)
                datasets2.pop(0)
            elif '' in value2 or value2==[]:
                datasets=['']
                datasets2=['']
                df=ahooga_tidy2
                df2=ahooga_actual2
                family=list(df['SKU Name'].unique())
                family2=list(df2['SKU Name'].unique())
                for fam in family:
                    df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                    datasets.append(df_filtered)
                for fam in family2:
                     df_filtered = ahooga_actual2[ahooga_actual2['SKU Name'] == fam]
                     datasets2.append(df_filtered)
                datasets.pop(0)
                datasets2.pop(0)
            else:
                if type(value2) == str:
                    value2= [value2]
                datasets=['']
                datasets2=['']
                for fam in value2:
                    df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                    datasets.append(df_filtered)
                    df_filtered=ahooga_actual2[ahooga_actual2['SKU Name'] == fam]
                    datasets2.append(df_filtered)
                datasets.pop(0)
                datasets2.pop(0)
        
        elif '<All>' in value2:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Year','Month','SKU Name','Bikes Sold','Forecast Bikes Sold']])
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','SKU Name'],as_index=False).sum()
            datasets=['']
            datasets2=['']
            #family=list(ahooga_bike_family['New_SKU_Name'].unique())
            df2=ahooga_actual[ahooga_actual['Product Family']==value3]
            df=ahooga_tidy2[ahooga_tidy2['Product Family']==value3]
            family=list(df['SKU Name'].unique())
            family2=list(df['SKU Name'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                datasets.append(df_filtered)
            for fam in family2:
                df_filtered2 = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                datasets2.append(df_filtered2)
    
            datasets.pop(0)
            datasets2.pop(0)
        elif '' in value2 or value2==[]:
            ahooga_bike_family=pd.DataFrame(data,columns=[c['name'] for c in cols])
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','SKU Name'],as_index=False).sum()
            datasets=['']
            datasets2=['']
            #family=list(ahooga_bike_family['New_SKU_Name'].unique())
            df=ahooga_tidy2[ahooga_tidy2['Product Family']==value3]
            df2=ahooga_actual[ahooga_actual['Product Family']==value3]
            family=list(df['SKU Name'].unique())
            family2=list(df['SKU Name'].unique())
            for fam in family:
                df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                datasets.append(df_filtered)
            for fam in family2:
                df_filtered2 = ahooga_actual2[ahooga_actual2['SKU Name'] == fam]
                datasets2.append(df_filtered2)
            datasets.pop(0)
            datasets2.pop(0)
        else:
            ahooga_bike_family=pd.DataFrame(data,columns=[c for c in ['Year','Month','SKU Name','Bikes Sold','Forecast Bikes Sold']])
            ahooga_actual2=ahooga_actual.groupby(['Year','Month','SKU Name'],as_index=False).sum()
            if type(value2) == str:
                value2 = [value2]
            datasets=['']
            datasets2=['']
            for fam in value2:
                df_filtered = ahooga_bike_family[ahooga_bike_family['SKU Name'] == fam]
                datasets.append(df_filtered)
                df_filtered2 = ahooga_actual2[ahooga_actual2['SKU Name'] == fam]
                datasets2.append(df_filtered2)
            datasets.pop(0)
            datasets2.pop(0)
        traces=['']
        traces2=['']
        for dataset in datasets2:
            
            
            traces.append(go.Bar({'x':dataset['Month'],'y':dataset['Bikes Sold'],'type':'bar'
                              ,'name':list(dataset['SKU Name'].unique())[0]
                              }))
        for dataset in datasets:
            traces2.append(go.Bar({'x':dataset['Month'],'y':dataset['Forecast Bikes Sold'],'type':'bar'
                              ,'name':list(dataset['SKU Name'].unique())[0]
                              }))
        traces.pop(0)
        traces2.pop(0)
        layout1=go.Layout(barmode='stack', title = 'Per month grouped by SKU for bikes(actual)',
                          xaxis_title='The Month of the year',yaxis_title='Number of bikes sold'
                          ,plot_bgcolor='white',
                paper_bgcolor='white',)
        layout2=go.Layout(barmode='stack', title = 'Per month grouped by SKU for bikes(predicted)',
                          xaxis_title='The Month of the year',yaxis_title='Number of bikes sold'
                          ,plot_bgcolor='white',
                paper_bgcolor='white',)
         
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
        dataset=dataset[dataset['Created_date_month']<8]
        
        traces.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['Actual_quantity'],'type':'bar'
                              ,'name':list(dataset['Product_family'].unique())[0],'hovertemplate':'Quantity sold :%{y:4d} '+' bike family:',
                              }))
        
        
    traces.pop(0)
    layout=go.Layout(barmode='stack', title = 'Per family',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold',plot_bgcolor='white',
                paper_bgcolor='white',)

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
        dataset=dataset[dataset['Created_date_month']<8]
        
        traces.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['Actual_quantity'],'type':'bar'
                              ,'name':list(dataset['Product_family'].unique())[0],'hoverinfo':'y'
                              }))
        
        
    traces.pop(0)
    layout=go.Layout(barmode='stack', title = 'Per family',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold',plot_bgcolor='white',
                paper_bgcolor='white',)

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
        dataset=dataset[dataset['Created_date_month']<8]
        
        traces.append(go.Bar({'x':dataset['Created_date_month'],'y':dataset['Actual_quantity'],'type':'bar'
                              ,'name':list(dataset['New_SKU_Name'].unique())[0],'hoverinfo':'y'
                              }))
        
        
    traces.pop(0)
    layout=go.Layout(barmode='stack', title = 'Per SKU',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold',plot_bgcolor='white',
                paper_bgcolor='white',)

    fig = {'data': traces, 'layout': layout}
    return go.Figure(fig)


@app.callback(
    dash.dependencies.Output('dropy2', 'options'),
    [dash.dependencies.Input('dropy', 'value')]
)
def update_date_dropdown(name):
    if name =='':
        return []
    elif name=='<All>':
        return [{'label': i, 'value': i} for i in unique_bike_sku]
    else:
        return [{'label': i, 'value': i} for i in dict[name]]      



@app.callback(
    Output('test_graph', 'figure'),
    [Input('dropy2', 'value'),
     Input('dropy', 'value')])
def update_graph(SKU, family):
    if '<All>' in family:
        if '<All>' in SKU:
            df=bikes_frame
            nam=list(df['New_SKU_Name'].unique())
            datasets=['']
            for na in nam:
                df_filtered=bikes_frame[bikes_frame['New_SKU_Name']==na]
                datasets.append(df_filtered)
            datasets.pop(0)
        elif '' in SKU or SKU==[]:
            
            df=bikes_frame
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
                    
    elif '<All>' in SKU:
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
    
    traces = ['']
    for dataset in datasets:
        dataset=dataset.groupby(['Created_date_month','New_SKU_Name','Product_family'],as_index=False).count()
        dataset=dataset[dataset['Created_date_month']<8]
        
        
        traces.append(
            go.Bar({
                'x': dataset['Created_date_month'],
                'y': dataset['Actual_quantity'],'text':dataset['Product_family']
                ,'name': list(dataset['New_SKU_Name'].unique())[0],'hovertemplate':'Bike: <b>%{text}</b><br>'+ 
                'Quantity sold:%{y:4d}',
        }))
    traces.pop(0)
    layout=go.Layout(barmode='stack', title = 'Per SKU',xaxis_title='The Month of the year',yaxis_title='Number of bikes sold',plot_bgcolor='white',
                paper_bgcolor='white',)

    fig = {'data': traces, 'layout': layout}
    return go.Figure(fig)

if __name__ == '__main__':
    app.run_server(debug=True)
    


        
    