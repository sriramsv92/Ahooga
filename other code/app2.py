# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:25:22 2019

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
import io
import dash_table_experiments as dt
import datetime


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df

#plot(fig)
    
def parse_contents(contents, filename, date):
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
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # Use the DataTable prototype component:
        # github.com/plotly/dash-table-experiments
        dt.DataTable(rows=df.to_dict('records')),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all',
            
        })
    ])

app = dash.Dash(__name__,external_stylesheets=external_stylesheets,   
    )


server = app.server

app.layout = html.Div(children=[html.Div([dcc.Upload(id='upload-data',children=html.Div(['Drag and Drop or ', html.A('Select Files')
                ]),
                
                # Allow multiple files to be uploaded
                multiple=True
            
                                                     ),
html.Div(id='upload-data-df',),dash_table.DataTable(
        id='datatable',
        data=[],),
                                          ])])

@app.callback(dash.dependencies.Output('datatable', 'data'),
              [dash.dependencies.Input('upload-data', 'contents'),
               dash.dependencies.Input('upload-data', 'filename'),
               dash.dependencies.Input('upload-data', 'last_modified'),])

def update_figure(content,rowss,datas):
    if not content:
        return []
    dff = pd.read_csv(io.StringIO(content))
    return dff.to_dict('records')
        
        
    
       
    
    
    

if __name__ == '__main__':
    app.run_server(debug=True)