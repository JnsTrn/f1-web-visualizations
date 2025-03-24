import dash

from dash import html

import dash_bootstrap_components as dbc


####### Initialize the Dash app #######

dash.register_page(__name__, path='/')


########## Set up the layout ##########

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
        html.H4(
            'Welcome to our Project! We want to answer these questions:',
            className='text-center text-light',
        ),
        html.Br(),
        html.A(
            html.H1(
                'How does the starting grid position influence the finishing '
                'position of drivers in the seasons from 1994 - 2024?',
                className='text-center page-header',
            ),
            href='/gridPosition',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            question1_txt,
                        ),
                    ],
                    className='p-3 bg-dark text-light',
                ),
                width={'size': 12, 'order': 1},
            ),
            className='mb-5',
        ),
        html.A(
            html.H1(
                'How has the total number of crashes and retirements evolved '
                'in the seasons from 1994 - 2024?',
                className='text-center page-header',
            ),
            href='/retirements',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            question2_txt,
                        ),
                    ],
                    className='p-3 bg-dark text-light',
                ),
                width={'size': 12, 'order': 1},
            ),
            className='mb-5',
        ),
        html.A(
            html.H1(
                'How does the number and the average duration of pitstops for '
                'a driver in a race relate to his finishing position?',
                className='text-center page-header',
            ),
            href='/pitstops',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            question3_txt,
                        ),
                    ],
                    className='p-3 bg-dark text-light',
                ),
                width={'size': 12, 'order': 1},
            ),
            className='mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(className="chequered-flag"),
            ),
        ),
    ]
)
