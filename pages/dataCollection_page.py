import dash

from dash import html

import dash_bootstrap_components as dbc


####### Initialize the Dash app #######

dash.register_page(__name__, path='/about-data', title='About The Data')


########## Set up the layout ##########

race_txt = [
    'The ',
    html.A(
        'Jolpica F1 API',
        href='https://github.com/jolpica/jolpica-f1/',
        target='_blank',
        className='text-light',
    ),
    ' was used to gather race data spanning a 30-year time frame, ',
    'from 1994 to 2024. This timeframe was chosen because in 1994 a major '
    'rule change was introduced. ',
    'The collected data includes metadata for each race and driver, race '
    'results like driver standings and finishing statuses for each driver '
    'and race. Detailed pit stop data, however, ',
    'was only available from the 2011 season onward.',
    html.Br(),
    html.Br(),
    'For analysis, we categorized the different finishing statuses into four '
    'groups based on the status column in the race results:',
    html.Br(),
    '1. Race Status – Drivers who completed the race on different positions',
    html.Br(),
    '2. Incidents/Crashes – Drivers involved in accidents and collisions.',
    html.Br(),
    '3. Technical Failures – Retirements caused by mechanical or technical '
    'issues.',
    html.Br(),
    '4. Other – Statuses that did not fit into the above categories. '
    '(not very common)',
]

weather_txt = [
    'Weather data from 2005 to 2024 was collected using the ',
    html.A(
        'Open Meteo API',
        href='https://open-meteo.com/en/docs/historical-weather-api',
        target='_blank',
        className='text-light',
    ),
    ', which provided precise hourly precipitation data based on race '
    'locations and times. The ',
    'race start times, available only from 2005 onwards, together with '
    'geo-coordinates, served as the basis for merging ',
    'weather data with race data. This integration allowed us to assess '
    'how weather conditions affected race outcomes.',
    html.Br(),
    html.Br(),
    'To classify weather conditions for each race, precipitation thresholds '
    'were defined as follows:',
    html.Br(),
    '1. Dry: Minimal or no precipitation.',
    html.Br(),
    '2. Mixed: Alternating dry and wet periods during the race.',
    html.Br(),
    '3. Wet: Consistent precipitation throughout the race.',
]

final_txt = [
    'All analyses were based on data sourced from the ',
    html.A(
        'Jolpica F1 API',
        href='https://github.com/jolpica/jolpica-f1/',
        target='_blank',
        className='text-light',
    ),
    ' and the ',
    html.A(
        'Open Meteo API',
        href='https://open-meteo.com/en/docs/historical-weather-api',
        target='_blank',
        className='text-light',
    ),
    ', ensuring consistency and reliability across the selected time spans. '
    'Remarkably, there was no missing data within the defined time frames. '
    'Both datasets are publicly accessible.',
    html.Br(),
    html.Br(),
    'Additionally, the source code for this website is available in a public '
    'GitHub repository, which can be accessed ',
    html.A(
        'here',
        href='https://github.com/JnsTrn/f1-web-visualizations',
        target='_blank',
        className='text-light',
    ),
    '. Note that data collection was conducted in a private repository, '
    'which is not publicly accessible.',
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
                    className='d-flex justify-content-center align-items-center',
                    width=5,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H4(
                                'Race Data', className='text-center text-light'
                            ),
                            html.P(race_txt),
                            html.H4(
                                'Weather Data',
                                className='text-center text-light mt-4',
                            ),
                            html.P(weather_txt),
                            html.H4(
                                'Data Availability and Resources',
                                className='text-center text-light mt-4',
                            ),
                            html.P(final_txt),
                        ]
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
    ]
)
