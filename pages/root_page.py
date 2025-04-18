import dash

from dash import html

import dash_bootstrap_components as dbc


####### Initialize the Dash app #######

dash.register_page(__name__, path='/', title='Home')


########## Set up the layout ##########

intro_txt = [
    'This project explores various research questions related to Formula 1, '
    'aiming to uncover how race results are influenced by different factors. '
    'Our approach combines detailed visualizations with insightful analysis to'
    ' present our findings. Data collection was accomplished using the ',
    html.A(
        'Jolpica F1 API',
        href='https://github.com/jolpica/jolpica-f1/blob/main/README.md',
        target='_blank',
        className='text-light',
    ),
    ' for comprehensive Formula 1 data and the ',
    html.A(
        'Open Meteo API',
        href='https://open-meteo.com/en/docs/historical-weather-api',
        target='_blank',
        className='text-light',
    ),
    " for precise weather data tailored to each race's location and time. "
    'Further details on the data gathering process can be found ',
    html.A('here', href='/about-data', className='text-light'),
    '. This project was conducted as part of the "Data Science Project" ',
    'course at ',
    html.A('CAU',
           href='/https://www.uni-kiel.de/en/imprint',
           target='_blank', className='text-light'),
    '.'
]

question1_txt = '''
    A driver's starting grid position is determined by qualification races.
    It is likely that the starting grid position influences the finishing
    position  in the final race. We will analyze data from the 1994–2024
    seasons to uncover the relationship between these two factors.
    Additionally, we will explore how this relationship differs between
    drivers based on their experience levels.
'''

question2_txt = '''
    Drivers are classified as retired if they are unable or not allowed to
    complete a race. Retirements caused by crashes or technical failures are a
    common occurrence in Formula 1. We will analyze data from the 1994–2024
    seasons to examine how retirements have evolved over the years.
    Additionally, we will explore the relationship between weather conditions
    and retirements, limited to data from 2005–2024.
'''

question3_txt = '''
    In Formula 1, pit stops are necessary for tasks like changing tires and
    making minor technical repairs. We will analyze data from the 2011–2024
    seasons to investigate how the number and average duration of pit stops
    for a driver have changed over the years, and how these factors relate to
    their finishing position.
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
                    className='d-flex justify-content-center align-items-center',
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
                    className='d-flex align-items-center',
                    width=7,
                ),
            ],
            align='center',
            className='pb-5 pt-5',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(className='chequered-flag'),
            ),
            className='pt-5 pb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.A(
                    html.Div(
                        [
                            html.H1(
                                'How does the starting grid position influence'
                                ' the finishing '
                                'position of drivers in the seasons from'
                                ' 1994 - 2024?',
                                className='text-center page-header text-light',
                                style={'marginBottom': '20px'},
                            ),
                            html.P(
                                question1_txt,
                            ),
                        ],
                        className='p-3 text-light hover-box',
                    ),
                    href='/grid-position',
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
                                'How has the total number of crashes and '
                                'retirements evolved '
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
                                'How does the number and the average duration'
                                'of pit stops for a driver in a race relate to'
                                ' his finishing position from 2011 - 2024?',
                                className='text-center page-header text-light',
                                style={'marginBottom': '20px'},
                            ),
                            html.P(
                                question3_txt,
                            ),
                        ],
                        className='p-3 text-light hover-box',
                    ),
                    href='/pit-stops',
                    className='custom-hover-link',
                ),
            ),
            className='mt-2 mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(className='chequered-flag'),
            ),
        ),
    ]
)
