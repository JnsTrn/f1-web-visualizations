import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from plots import *


####### Initialize the Dash app #######

app = dash.Dash(__name__)
server=app.server

############## Load Data ##############

DATA_PATH = 'data/'

df_CraWeath = pd.read_csv(DATA_PATH + 'crashes_and_weather.csv')


# ############ Define Graphs ############

init_figs()
fig_CraWeath = create_fig_CraWeath(df_CraWeath)


########## Set up the layout ##########

app.layout = html.Div(children=[
    html.H1("Testing Server"),
    html.Div(children='''
    Hello from from testing server.
    '''),
    dcc.Graph(figure=fig_CraWeath)
])


############# Run the app #############

if __name__ == '__main__':
    app.run(debug=True)
