import dash

from dash import html

import dash_bootstrap_components as dbc


####### Initialize the Dash app #######

dash.register_page(__name__, path='/')


########## Set up the layout ##########

intro_txt = '''
    We want to show you the world. We want to show you the world.
    We want to show you the world. We want to show you the world.
    We want to show you the world. We want to show you the world.
    We want to show you the world. We want to show you the world.
'''
question1_txt = '''
    The starting grid position is an important factor in determining
    the finishing position of drivers in Formula 1 and is likely to
    be a key factor in the outcome of a race. We will analyze
    the data from the seasons 1994 - 2024 to determine the
    relationship between the starting grid position and the finishing
    position of drivers.
'''
question2_txt = '''
    Crashes and retirements are a common occurence in Formula 1. We
    will analyze the data from the seasons 1994 - 2024 to determine
    how the total number of crashes and retirements has evolved
    over the years.
'''
question3_txt = '''
    Pitstops are an important part of Formula 1. We will analyze the
    data from the seasons 2011 - 2024 to determine how the number
    and the average duration of pitstops for a driver has evolved
    over the years and how it relates to his finishing position.
'''


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
                                'What to expect from this project?',
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
                html.A(
                    html.Div(
                        [
                            html.H1(
                                'How does the starting grid position influence the finishing '
                                'position of drivers in the seasons from 1994 - 2024?',
                                className='text-center page-header text-light',
                                style={'marginBottom': '20px'},
                            ),
                            html.P(
                                question1_txt,
                            ),
                        ],
                        className='p-3 text-light hover-box',
                    ),
                    href='/gridPosition',
                    className='custom-hover-link',
                ),
            ),
            className='mt-2 mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.A(
                    html.Div(
                        [
                            html.H1(
                                'How has the total number of crashes and retirements evolved '
                                'in the seasons from 1994 - 2024?',
                                className='text-center page-header text-light',
                                style={'marginBottom': '20px'},
                            ),
                            html.P(
                                question2_txt,
                            ),
                        ],
                        className='p-3 text-light hover-box',
                    ),
                    href='/retirements',
                    className='custom-hover-link',
                ),
            ),
            className='mt-2 mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.A(
                    html.Div(
                        [
                            html.H1(
                                'How does the number and the average duration of pitstops for '
                                'a driver in a race relate to his finishing position?',
                                className='text-center page-header text-light',
                                style={'marginBottom': '20px'},
                            ),
                            html.P(
                                question3_txt,
                            ),
                        ],
                        className='p-3 text-light hover-box',
                    ),
                    href='/pitstops',
                    className='custom-hover-link',
                ),
            ),
            className='mt-2 mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(className="chequered-flag"),
            ),
        ),
    ]
)
