import dash

from dash import html

import dash_bootstrap_components as dbc


####### Initialize the Dash app #######

dash.register_page(__name__, path='/about-data', title='About The Data')


########## Set up the layout ##########

intro_txt = [
    'This project explores various research questions related to Formula 1, '
    'aiming to uncover how race results are influenced by different factors. '
    'Our approach combines detailed visualizations with insightful analysis to '
    'present our findings. Data collection was accomplished using the ',
    html.A('Jolpica F1 API', href='https://jolpica.com/api',
           target='_blank', className='text-light'),
    ' for comprehensive Formula 1 data and the ',
    html.A('Open Meteo API', href='https://open-meteo.com/',
           target='_blank', className='text-light'),
    ' for precise weather data tailored to each race\'s location and time. '
]

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Img(
                        src=dash.get_asset_url('racing_f1_car.jpg'),
                        width='70%',
                    ),
                    className="d-flex justify-content-center align-items-center",
                    width=5,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H4(
                                'What was the process?',
                                className='text-center text-light',
                            ),
                            html.P(intro_txt),
                        ],
                    ),
                    className="d-flex align-items-center",
                    width=7,
                ),
            ],
            align="center",
            className="pb-5 pt-5",
        ),
        dbc.Row(
            dbc.Col(
                html.Div(className="chequered-flag"),
            ),
            className="pt-5 pb-5",
        ),
        dbc.Row(
            dbc.Col(
                html.Div(className="chequered-flag"),
            ),
        ),
    ]
)
