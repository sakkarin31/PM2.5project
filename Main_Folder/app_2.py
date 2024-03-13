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
app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, 'assets/style.css'])
# Incorporate data
df = pd.read_csv('data_cleaned_air4thai.csv')
dt = pd.read_csv('data_model_predict.csv')
# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('Air Quality Analysis Forecast', className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        html.Div('Historical Air Quality Statistics ', className="text-dark text-start fs-5")
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([  # Wrap your table in a div for styling
                dash_table.DataTable(
                    id='datatable',
                    columns=[{'name': col, 'id': col} for col in df.columns],
                    data=df.to_dict('records'),
                    page_size=16,
                    style_table={'overflowX': 'auto'},
                    style_cell={'color': 'black', 'textAlign': 'left', 'backgroundColor': 'white'},
                )
            ], style={'width': '80%', 'margin': '0 auto'})  # Center the table
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='pollutant-dropdown',
                options=[
                    {'label': 'PM2.5', 'value': 'PM25'},
                    {'label': 'Relative Humidity', 'value': 'RH'},
                ],
                value='PM25'  # Default selection
            )
        ], width=3),

        dbc.Col([
            dcc.Graph(id='pollutant-bar-chart')
        ], width=9)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='prediction-graph')
        ], width=6),

        dbc.Col([
            dcc.Graph(id='prediction-graph-2')
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Button("Update Prediction Graph", id='prediction-button', color="primary", className="mb-3")
        ], width=12),
    ]),


], fluid=True)


@app.callback(
    Output(component_id='pollutant-bar-chart', component_property='figure'),
    Input(component_id='pollutant-dropdown', component_property='value')
)
def update_bar_chart(selected_pollutant):
    if selected_pollutant == 'PM25':
        fig = px.bar(df, x='DATETIMEDATA', y='PM25', title='Historical PM2.5 Statistics')
        fig.update_traces(marker_color='green', selector=dict(type='bar'))
        fig.update_xaxes(title='Date and Time')
        fig.update_yaxes(title='Particulate Matter 2.5 (µg/m³)')
    elif selected_pollutant == 'RH':
        fig = px.bar(df, x='DATETIMEDATA', y='RH', title='Historical Relative Humidity Value Statistics')
        fig.update_traces(marker_color='darkblue', selector=dict(type='bar'))
        fig.update_xaxes(title='Date and Time')
        fig.update_yaxes(title='Relative Humidity (%)')
    else:
        # Handle other pollutants here
        pass
    return fig

# Add controls to build the interaction
@app.callback(
    Output(component_id='prediction-graph', component_property='figure'),
    Input(component_id='prediction-button', component_property='n_clicks')
)
def update_prediction_graph(n_clicks):
    prediction_data = pd.read_csv('data_model_predict.csv')
    fig = px.line(prediction_data, x='DATETIMEDATA', y='RH', title='Predicted RH Graph for Next Week')
    fig.update_xaxes(title='Date and Time')
    fig.update_yaxes(title='Relative Humidity (%)')
    return fig

# Add controls to build the interaction
@app.callback(
    Output(component_id='prediction-graph-2', component_property='figure'),
    Input(component_id='prediction-button', component_property='n_clicks')
)
def update_prediction_graph_2(n_clicks):
    prediction_data = pd.read_csv('data_model_predict.csv')
    fig = px.line(prediction_data, x='DATETIMEDATA', y='PM25', title='Predicted PM Graph for Next Week')
    fig.update_xaxes(title='Date and Time')
    fig.update_yaxes(title='Particulate Matter 2.5 (µg/m³)')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
