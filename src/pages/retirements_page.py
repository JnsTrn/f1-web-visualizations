import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from plots import *

####### Initialize the Dash app #######

dash.register_page(__name__, path="/retirements")


############## Load Data ##############

DATA_PATH = 'data/'

df_CraWeath = pd.read_csv(DATA_PATH + 'crashes_and_weather.csv')


############ Create Graphs ############

init_figs()
fig_CraWeath = create_fig_CraWeath(df_CraWeath)

layout = dbc.Container([
    html.H1(
        "How has the total number of crashes and retirements evolved in the seasons from 1994 - 2024?",
        className="text-center page-header"
    ),
    html.Br(),
    # Subquestion 1
    html.H2(
        "Which tracks have the highest frequency of crashes or retirements compared to others?",
        className='text-light'
    ),
    dbc.Row([
        dbc.Col([
            #dcc.Graph(figure=)
        ])
    ]),
    html.Br(),
    html.P("Description and Analysis"),
    html.Br(),
    # Subquestion 2
    html.H2(
        "How does weather affect race completion rates and the likelihood of crashes or retirements in the seasons from 2005 - 2024?",
        className='text-light'
    ),
    dbc.Row([
        dbc.Col([
            #dcc.Graph(figure=)
        ])
    ]),
    html.Br(),
    html.P("Description and Analysis"),
    html.Br(),
])