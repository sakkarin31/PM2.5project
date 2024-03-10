import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pycaret
from pycaret.classification import *
from pycaret.regression import *
from pycaret.datasets import get_data

from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc


# Incorporate data
df = pd.read_csv('air4thai_44t_2024-02-19_2024-02-20.csv')

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Add controls to build the interaction
@app.callback(
    Output(component_id='prediction-graph', component_property='figure'),
    Input(component_id='prediction-button', component_property='n_clicks')
)
def update_prediction_graph(n_clicks):
    prediction_data = pd.read_csv('new_model_predict.csv')
    fig = px.line(prediction_data, x='DATETIMEDATA', y='RH', title='Predicted RH for Next Week')
    fig.update_xaxes(title='Date and Time')
    fig.update_yaxes(title='Relative Humidity (%)')
    return fig

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('My First App with Data, Graph, and Controls', className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        dbc.RadioItems(options=[{"label": x, "value": x} for x in ['pop', 'lifeExp', 'gdpPercap']],
                        value='lifeExp',
                        inline=True,
                        id='radio-buttons-final')
    ]),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(data=df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
        ], width=6),

        dbc.Col([
            dcc.Graph(figure={}, id='my-first-graph-final')
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='prediction-graph')
        ], width=12),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Button("Update Prediction Graph", id='prediction-button', color="primary", className="mb-3")
        ], width=12),
    ]),

], fluid=True)

# Add controls to build the interaction
@app.callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8080)
