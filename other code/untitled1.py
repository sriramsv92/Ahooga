import dash_html_components as html
import dash_core_components as dcc
import dash

import plotly

from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np
"""
import json
import datetime
import operator
import os
"""
import base64
import io
import dash_table

dff=pd.read_csv('example_air_passengers.csv')
rss=dff.to_dict('records')

app = dash.Dash()

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

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
        placeholder='Filter Column'),


    html.Br(),
    html.H5("Updated Table"),
    html.Div(dash_table.DataTable(data=[], id='table'))


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
        elif 'xls' in filename:
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
dff2=dff.copy()
drops=[]
for i in range(len(dff2.columns)):
    print(i)
    if dff2.dtypes[i]=='O':
        drops.append(dff2.columns[i])
dff2=dff2.drop(drops,axis=1)
    

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
        drops=[]
        for i in range(len(dff2.columns)):
            if dff2.dtypes[i]=='O':
                drops.append(dff2.columns[i])
        dff2=dff2.drop(drops,axis=1)
        return [{'label': i, 'value': i} for i in sorted(list(dff2))]


app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
    app.run_server(debug=True)