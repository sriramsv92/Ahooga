import dash_html_components as html
import dash_core_components as dcc
import dash
import datetime
import plotly
from sklearn.linear_model import LinearRegression
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from dateutil.parser import parse
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

"""
import json
import datetime
import operator
import os
"""
import base64
import io
import dash_table

def x_y_create(start,train_set,date_set):
    X_train=[]
    y_train=[]
    date_sets=[]
    for i in range(start,len(train_set)):
        X_train.append(train_set[i-start:i])
        y_train.append(train_set[i])
        date_sets.append(date_set[i])
    return np.array(X_train),np.array(y_train),np.array(date_sets)

def rotate(l,n):
    l=l.T
    lx= np.concatenate((l[n:],l[:n]), axis=0)
    return lx.T


dff=pd.read_csv('example_air_passengers.csv')
rss=dff.to_dict('records')
dff2=dff.copy()
drops=[]
for i in range(len(dff2.columns)):
    print(i)
    if dff2.dtypes[i]=='O':
        drops.append(dff2.columns[i])
dff2=dff2.drop(drops,axis=1)

listx=[]
dffx=dff.copy()
for i in range(len(dffx.columns)):
    try:
        parse(dffx.loc[1][i])
    except TypeError:
        listx.append(dffx.columns[i])
steps=10     
forest= RandomForestRegressor(n_estimators=200,n_jobs=1) 
datset=dff['Date'].values
valset=dff['Volume'].values
xtrains,ytrains,dattrains=x_y_create(steps,valset,datset)
dxxx=dff['Volume']
trainn=dxxx.iloc[-steps:].values     
trainn=trainn.reshape(-1,1).T
lrr=LinearRegression()
forest.fit(xtrains,ytrains)
lrr.fit(xtrains,ytrains)
pss=forest.predict(trainn)

DATE=dff['Date'].values
VOLUME=dff['Volume'].values
lengs=len(DATE)
lengs=int(0.8*lengs)
trains,tests,dates=x_y_create(steps,VOLUME,DATE)
X_train=trains[:lengs]
y_train=tests[:lengs]
y_test=tests[lengs:]
X_test=trains[lengs:]
lrr.fit(X_train,y_train)
forest.fit(X_train,y_train)
liss=[]
liss_r=[]
trainx=X_test[0]
trainxunchanged=trainx.reshape(-1,1).T

trainx=trainx.reshape(-1,1).T
trainxr=trainx.reshape(-1,1).T

print(trainx)
for i in range(len(y_test)):
    predix=forest.predict(trainx)
    predixr=lrr.predict(trainxr)
    trainx=rotate(trainx,1)
    trainxr=rotate(trainxr,1)
    trainx[0][-1]=predix
    trainxr[0][-1]=predixr
    print(trainx)
    liss.append(int(predix[0]))
    liss_r.append(int(predixr[0]))
pred_forest=forest.predict(X_test)
pred_lrr=lrr.predict(X_test)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets,   
    )
server=app.server
"""
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True
"""

app.layout = html.Div([

    html.H5("Upload Files"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False),
    html.Br(),
    html.Button(
        id='propagate-button',
        n_clicks=0,
        children='Propagate Table Data'
    ),


    html.Br(),
    html.H5("Filter Column"),
    dcc.Dropdown(id='dropdown_table_filterColumn',
        multi = False,
        placeholder='Filter Column'),html.H5('Date Column'),
                 dcc.Dropdown(id='date-dropdown',multi=False,placeholder='Date Column'),


    html.Br(),
    html.H5("Updated Table"),
    html.Div(dash_table.DataTable(data=[], id='table')),html.Div(
    dcc.Graph(id='graphic2',figure=go.Figure())),html.Div([html.H6('Select the number of time steps'),dcc.Input(id='time-steps',
             type='number',min=1,max=100,value=10,step=1)]),
    html.Br(),
    html.Div(dash_table.DataTable(data=[],id='predictions')),
    html.Br(),html.H6('The predictions based on regression model'),
    html.Div(dcc.Graph(id='predictiongraph',figure=go.Figure())),html.Div(
            [html.P('the r2 value of the model is'),html.H6(id='R2 value')]),


])


# Functions

# file upload function
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' or 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(e)
        return None

    return df


# callback table creation
@app.callback([Output('table', 'data'),
               Output('table','columns')],
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is not None:
        df = parse_contents(contents, filename)
        if df is not None:
            dicty=df.to_dict('records')
            s=list(dicty[0].keys())
            
            columns=[{'name':i,'id':i}for i in s]
            return df.to_dict('records'),columns
        else:
            return [{}],[]
    else:
        return [{}],[]

        
        
@app.callback(Output('time-steps','max'),
              [Input('table','data')])
def max_value(data):
    if data:
        frame=pd.DataFrame(data)
        value=int(len(frame)*0.6)
        return value
    
        
    
        


#callback update options of filter dropdown
@app.callback(Output('dropdown_table_filterColumn', 'options'),
              [Input('propagate-button', 'n_clicks'),
               Input('table', 'data')])
def update_filter_column_options(n_clicks_update, tablerows):
    if n_clicks_update < 1:
        print( "df empty")
        return []

    else:
        dff = pd.DataFrame(tablerows) # <- problem! dff stays empty even though table was uploaded

        print ("updating... dff empty?:", dff.empty) #result is True, labels stay empty
        dff2=dff.copy()
        dff3=dff.copy()
        drops=[]
        drops2=[]
        for i in range(len(dff2.columns)):
            if dff2.dtypes[i]=='O':
                drops.append(dff2.columns[i])
        dff2=dff2.drop(drops,axis=1)
        return [{'label': i, 'value': i} for i in sorted(list(dff2))]
    
    
listx=[]
dffx=dff.copy()
for i in range(len(dffx.columns)):
    try:
        parse(dffx.loc[1][i])
    except TypeError:
        listx.append(dffx.columns[i])
    
@app.callback(Output('date-dropdown', 'options'),
              [Input('propagate-button', 'n_clicks'),
               Input('table', 'data')])
    
    
    
    
    
    
def update_filter_column_options(n_clicks_update, tablerows):
    if n_clicks_update < 1:
        print( "df empty")
        return []

    else:
        dff = pd.DataFrame(tablerows) # <- problem! dff stays empty even though table was uploaded

        print ("updating... dff empty?:", dff.empty) #result is True, labels stay empty
        dff2=dff.copy()
        dff3=dff.copy()
        drops=[]
        drops2=[]
        for i in range(len(dff2.columns)):
            try:
                parse(dff2.loc[1][i])
            except TypeError:
                drops.append(dff2.columns[i])
        dff2=dff2.drop(drops,axis=1)
        return [{'label': i, 'value': i} for i in sorted(list(dff2))]
        
        
            
          

@app.callback(Output('graphic2','figure'),
              [Input('dropdown_table_filterColumn','value'),
               Input('date-dropdown','value')],
              [State('table','data')])
def update_graph2(filters,filters_date,tablex):
    if tablex and filters:
        dff=pd.DataFrame(tablex)
        dff2=dff.copy()
        dff2=dff2[filters]
        dff3=pd.DataFrame(pd.concat([dff[filters],dff[filters_date]],axis=1))
        dff3[filters_date]=dff3[filters_date].apply(lambda x:parse(x))
        trace2=go.Scatter(x=dff3[filters_date],y=dff3[filters],mode='lines')
    layout=go.Layout(yaxis_title=filters)
    data=[trace2]
    fig={'data':data,'layout':layout}
    return go.Figure(fig)
@app.callback([Output('predictiongraph','figure'),
              Output('R2 value','children')
],            [Input('time-steps','value')],
              [State('dropdown_table_filterColumn','value'),
               State('date-dropdown','value'),
               State('table','data')])
def update_graphx(timest,filters,filters_date,tablex):
    if tablex and timest:
        dff=pd.DataFrame(tablex)
        dff2=dff.copy()
        dff2=dff2[filters]
        dff3=pd.DataFrame(pd.concat([dff[filters],dff[filters_date]],axis=1))
        number_of_days = len(dff3)
        traindays=int(0.8*number_of_days)
        DATES=dff3[filters_date].values
        SALES=dff3[filters].values
        trains,tests,dates=x_y_create(timest,SALES,DATES)
        X_train=trains[:traindays]
        y_train=tests[:traindays]
        dates_train=dates[:traindays]
        X_test=trains[traindays:]
        y_test=tests[traindays:]
        dates_test=dates[traindays:]
        
        forest= RandomForestRegressor(n_estimators=200,n_jobs=1)
        lr=LinearRegression()
        lr.fit(X_train,y_train)
        predictions=lr.predict(X_test)
        date_set_train=list(dates_train)
        for i in range(len(date_set_train)):
            date_set_train[i]=parse(date_set_train[i])
        date_set_test=list(dates_test)
        for i in range(len(date_set_test)):
            date_set_test[i]=parse(date_set_test[i])
        predi_list=[]
        trainy_set=X_test[0]
        trainy_set=trainy_set.reshape(-1,1).T
        #daty_set=train_dates[-timest:].values
        for i in range(len(y_test)):
            predix=lr.predict(trainy_set)
            trainy_set=rotate(trainy_set,1)
            trainy_set[0][-1]=predix
            predi_list.append(int(predix[0]))
        
        trace=go.Scatter(x=date_set_test,y=list(predictions),mode='lines',name='predicted sales')
        trace2=go.Scatter(x=date_set_test,y=list(y_test),mode='lines',name='actual sales')
        trace3=go.Scatter(x=date_set_test,y=predi_list,mode='lines',name='predicted sales2')
    layout=go.Layout(yaxis_title='predictions')
    data=[trace,trace2,trace3]
    fig={'data':data,'layout':layout}
    scores=lr.score(X_test,y_test)
    return go.Figure(fig),scores
        



app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
    app.run_server(debug=True)