import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

####### Initialize the Dash app #######

dash.register_page(__name__, path="/pitstops")


############## Load Data ##############
############ Create Graphs ############

########## Set up the layout ##########

layout = dbc.Container([
    html.H1(
        "How does the number and the average duration of pitstops for a driver in a race relate to his finishing position?",
        className="text-center page-header"
    ),
    html.Br(),
    # Subquestion 1
    html.H2(
        "How does the number and the average duration of pitstops for a driver in a race relate to his finishing position? ",
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

