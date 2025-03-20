import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from plots import *
import dash_bootstrap_components as dbc


####### Initialize the Dash app #######

style_sheet = [dbc.themes.LUX]
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

ASSET_PATH = 'assets/'

navbar = dbc.NavbarSimple(
    children=[
        #html.Img(src=ASSET_PATH + 'formula-1-vector-826415.jpg', height="50px"),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Research Questions", href="/"),
                dbc.DropdownMenuItem("Grid Position Analysis", href="/gridPosition"),
                dbc.DropdownMenuItem("Retirement Analysis", href="/retirements"),
                dbc.DropdownMenuItem("Pitstop Analysis", href="/pitstops"),
            ],
            nav=True,
            in_navbar=True,
            label="Navigation",
        ),
        dbc.NavItem(dbc.NavLink("Home", href="/")),
    ],
    brand="DSP 2025 - Team 897",
    brand_href="/",
    dark=True,
    fluid=True
)

imprint_section = html.Footer([
    dbc.Container([
        html.Hr(),
        dbc.Row([
            dbc.Col([
                html.P([
                    '',
                    html.A(
                        'Christian-Albrechts-Universität zu Kiel',
                        href='https://www.uni-kiel.de/de/impressum',
                        target='_blank',
                        className='text-center text-light'
                    )
                ], className='text-center text-light'),
                html.P('Christian-Albrechts-Platz 4', className='text-center text-light'),
                html.P('24118 Kiel, Germany', className='text-center text-light'),
                html.P([
                    "Telephone: ",
                    html.A("+49 (0431) 880-00", href="tel:+4943188000", className="text-light")
                ], className="text-center text-light"),
                html.P([
                    "E-Mail: ",
                    html.A("mail@uni-kiel.de", href="mailto:mail@uni-kiel.de", className="text-light")
                ], className="text-center text-light")
            ], width=12)
        ], justify='center')
    ], fluid=True, className='text-light')
])


########## Set up the layout ##########

app.layout = dbc.Container([
    navbar,
    html.Br(),
    dash.page_container,
    html.Br(),
    imprint_section
], fluid=True, className="bg-dark text-light")


############# Run the app #############

if __name__ == '__main__':
    app.run(debug=True)