import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

####### Initialize the Dash app #######

dash.register_page(__name__, path="/gridPosition")


############## Load Data ##############


############ Create Graphs ############


########## Set up the layout ##########

layout = dbc.Container([
    html.H1(
        "How does the starting grid position influence the finishing position of drivers in the seasons from 1994 - 2024?",
        className="text-center page-header"
    ),
    html.Br(),
    # Subquestion 1
    html.H2(
        "How does this differ between circuits that have been driven on at least X times?",
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
        "How do weather conditions impact the differences between start and finish position across different Formula 1 circuits hat have been driven on at least X times in the seasons from 2005 - 2024?",
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
    # Subquestion 3
    html.H2(
        "Are there specific drivers who excel or struggle more in wet conditions compared to dry conditions?",
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
    # Subquestion 4
    html.H2(
        "How does this differ between drivers of different experience levels (as determined by the amount of races they participated in)",
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
