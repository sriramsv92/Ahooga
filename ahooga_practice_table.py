# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:59:49 2019

@author: Sriram Sivaraman
"""
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output
import plotly.graph_objs as go
ahoo = pd.read_csv('ahooga_table_practice.csv')
ahoo_product_bike=ahoo[ahoo['Product_group']=='Bike']
ahoo_product_component=ahoo[ahoo['Product_group']=='Component']

import flask

server = flask.Flask(__name__)

@server.route('/')
def index():
    return 'Hello Flask app'

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)

app.layout = html.Div("My Dash app")

if __name__ == '__main__':
    app.run_server(debug=True)  