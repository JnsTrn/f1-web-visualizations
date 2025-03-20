import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from plots import *
import dash_bootstrap_components as dbc


####### Initialize the Dash app #######

style_sheet = [dbc.themes.SLATE]
app = dash.Dash(__name__, external_stylesheets=style_sheet, use_pages=True)
app.title = "DSP 2025 - Team 897"
server=app.server

############## Load Data ##############

DATA_PATH = 'data/'

df_CraWeath = pd.read_csv(DATA_PATH + 'crashes_and_weather.csv')


# ########### Create Graphs ###########

init_figs()
fig_CraWeath = create_fig_CraWeath(df_CraWeath)


########## Create Bootstrap Components ##########

navbar = dbc.NavbarSimple(
    brand="DSP 2025 - Team 897",
    brand_href="/",
    color="dark",
    dark=True,
    fluid=True
)


########## Set up the layout ##########

app.layout = dbc.Container([
    navbar,
    html.Br(),
    html.H2(
        "Welcome to DSP 2025! These are our research questions:",
        className="text-center text-light"
    ),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_CraWeath)
        ])
    ]),
    dbc.Row([
        dbc.Col(dbc.Button("Page 1", href="/page-1", color="primary", size="lg", className="w-100"), width=4),
        dbc.Col(dbc.Button("Page 2", href="/page-2", color="success", size="lg", className="w-100"), width=4),
        dbc.Col(dbc.Button("Page 3", href="/page-3", color="danger", size="lg", className="w-100"), width=4),
    ], className="text-center"),
    html.Br(),
    dash.page_container
], fluid=True, className="bg-dark text-light")


############# Run the app #############

if __name__ == '__main__':
    app.run(debug=True)
