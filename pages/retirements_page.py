import dash
import dash_bootstrap_components as dbc
import modules.crash_vis_mod as cvm
import modules.weather_crash_vis_mod as wcvm
import pandas as pd
from dash import Input, Output, dcc, html

####### Initialize the Dash app #######

dash.register_page(__name__, path='/retirements')

############## Load Data ##############

DATA_PATH = 'data/'

df = pd.read_csv(
    DATA_PATH + 'f1_1994_2024_categorized_by_race_status.csv',
    parse_dates=['date'],
)

df_CraWeath = pd.read_csv(DATA_PATH + 'crashes_and_weather.csv')

# ############ Define Graphs ############

wcvm.init_figs()
fig_CraWeath = wcvm.create_fig_CraWeath(df_CraWeath)
fig_total_incidents = cvm.total_incidents_by_year(df)
fig_retirements_rate = cvm.yearly_retirements_rate(df)
fig_retirements_race = cvm.average_yearly_retirements(df)
incidents_layout = cvm.create_interactive_incidents_dashboard(df)

# Update all figures to be responsive with consistent margins
for fig in [
    fig_total_incidents,
    fig_retirements_rate,
    fig_retirements_race,
    fig_CraWeath,
]:
    fig.update_layout(
        autosize=True,
        margin=dict(l=70, r=40, t=80, b=40),
    )

########## Set up the layout ##########

total_incidents_explanation = """
This is an explanation about what the plot depicts and what it means.
This graph shows the total number of incidents per year in Formula 1 from 1994
to 2024. Incidents include accidents, mechanical failures, and other reasons
for non-finishes. We can observe that the total number of incidents has
decreased over time, likely due to improved safety standards and car
reliability. The peaks in certain years may correspond to regulation changes
or particularly challenging seasons.
"""

retirement_rate_explanation = """
The retirement rate represents the percentage of cars that did not finish the
race compared to the total number of starters. This metric helps us understand
the reliability and safety evolution in F1 over three decades. The downward
trend suggests that modern F1 cars are significantly more reliable than their
predecessors. Notably, the introduction of hybrid power units in 2014 initially
caused a spike in retirements as teams adapted to the new technology, but
reliability quickly improved in subsequent seasons.
"""

retirements_race_explanation = """
This visualization shows the average number of retirements per race for each
season. It provides insight into how race attrition has changed over time.
Early seasons in our dataset show significantly higher average retirements per
race, sometimes exceeding 13 cars per race, while recent seasons typically see
fewer than 4 retirements per race. This improvement reflects advancements in
engineering, manufacturing processes, and overall design philosophy in modern
Formula 1.
"""

crash_weather_explanation = """
This analysis examines the relationship between weather conditions and crash
frequency. Wet or changing conditions have historically been associated with
higher crash rates in motorsport. The data reveals that races with rain or
changing weather conditions do indeed show a higher proportion of crash-related
retirements compared to races held in consistently dry conditions. This
information is valuable for understanding risk factors in race strategy and
safety planning.
"""

interactive_dashboard_explanation = """
The interactive dashboard above allows you to explore incident data in more
detail. You can filter by year, team, driver, and incident type to identify
patterns and trends. This tool is particularly useful for investigating
specific periods or comparing performance across different teams and drivers.
"""

sample_text = """
This is a short explanation about what the graph is suppposed to show and what
we did to create it.
"""

layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    [
                        'How has the total number of crashes and retirements '
                        'evolved in the seasons from 1994 - 2024?',
                    ],
                    className='text-center page-header',
                ),
                width={'size': 12, 'order': 1},
            ),
            # className='mb-4 border border-dark rounded bg-danger bg-gradient p-3',
            style={
                'backgroundImage': 'linear-gradient(to bottom, #b30412, #eb0e20)',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '5px 5px 15px rgba(0,0,0,0.2)',
            },
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            sample_text,
                            style={
                                'fontSize': '18px',
                                'lineHeight': '1.6',
                                'width': '93%',
                                'margin': '0 auto',
                                'textAlign': 'justify',
                            },
                        ),
                    ],
                    className='p-3 bg-dark text-light',
                ),
                width={'size': 12, 'order': 1},
            ),
            className='mb-2 mt-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            dcc.Graph(
                                figure=fig_total_incidents,
                                config={'responsive': True},
                            ),
                            style={
                                'margin': '0 auto',
                                'width': '92%',
                            },
                        ),
                    ]
                ),
                width={'size': 12, 'order': 1},
            ),
            className='mb-2',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            total_incidents_explanation,
                            style={
                                'fontSize': '18px',
                                'lineHeight': '1.6',
                                'width': '93%',
                                'margin': '0 auto',
                                'textAlign': 'justify',
                            },
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
                html.Div(
                    [
                        html.Div(
                            dcc.Graph(
                                figure=fig_retirements_rate,
                                config={'responsive': True},
                            ),
                            style={
                                'margin': '0 auto',
                                'width': '92%',
                            },
                        ),
                    ]
                ),
                width={'size': 12, 'order': 1},
            ),
            className='mb-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H4(
                            'Weather Impact Analysis',
                            className='text-center',
                            style={'fontSize': '20px'},
                        ),
                        html.P(
                            retirement_rate_explanation,
                            style={
                                'fontSize': '18px',
                                'lineHeight': '1.6',
                                'width': '93%',
                                'margin': '0 auto',
                                'textAlign': 'justify',
                            },
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
                html.Div(
                    [
                        html.Div(
                            dcc.Graph(
                                figure=fig_retirements_race,
                                config={'responsive': True},
                            ),
                            style={
                                'margin': '0 auto',
                                'width': '92%',
                            },
                        ),
                    ]
                ),
                width={'size': 12, 'order': 1},
            ),
            className='mb-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H4(
                            'Weather Impact Analysis',
                            className='text-center',
                            style={'fontSize': '20px'},
                        ),
                        html.P(
                            retirements_race_explanation,
                            style={
                                'fontSize': '18px',
                                'lineHeight': '1.6',
                                'width': '93%',
                                'margin': '0 auto',
                                'textAlign': 'justify',
                            },
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
                html.H1(
                    [
                        'Which tracks have the highest frequency of crashes '
                        'or retirements compared to others?',
                    ],
                    className='text-center page-header',
                ),
                width={'size': 12, 'order': 1},
            ),
            className='mb-4 border border-dark rounded bg-danger bg-gradient p-3',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    incidents_layout,
                    style={
                        'width': '92%',
                        'margin': '0 auto',
                    },
                ),
                width={'size': 12, 'order': 1},
            ),
            className='mb-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H4(
                            'Weather Impact Analysis',
                            className='text-center',
                            style={'fontSize': '20px'},
                        ),
                        html.P(
                            interactive_dashboard_explanation,
                            style={
                                'fontSize': '18px',
                                'lineHeight': '1.6',
                                'width': '93%',
                                'margin': '0 auto',
                                'textAlign': 'justify',
                            },
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
                html.H1(
                    [
                        'How does weather affect race completion rates and ',
                        html.Br(),
                        'the likelihood of crashes or retirements in the '
                        'seasons from 2005 - 2024?',
                    ],
                    className='text-center page-header',
                ),
                width={'size': 12, 'order': 1},
            ),
            # className='mb-4 border border-dark rounded bg-danger bg-gradient p-3',
            style={
                'backgroundColor': '#eb0e20',
                'color': 'white',
                'padding': '5px',
                #'border': '0.5px solid black',
                'borderRadius': '7px',
                'boxShadow': '5px 5px 15px rgba(0,0,0,0.2)',
            },
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            dcc.Graph(
                                figure=fig_CraWeath,
                                config={'responsive': True},
                            ),
                            style={
                                'margin': '0 auto',
                                'width': '92%',
                            },
                        ),
                    ]
                ),
                width={'size': 12, 'order': 1},
            ),
            className='mb-4 mt-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            crash_weather_explanation,
                            style={
                                'fontSize': '18px',
                                'lineHeight': '1.6',
                                'width': '93%',
                                'margin': '0 auto',
                                'textAlign': 'justify',
                            },
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
                html.Div(
                    html.A(
                        'Back to Top', href='#top', className='btn btn-danger'
                    ),
                    className='text-center',
                ),
                width={'size': 12, 'order': 1},
            ),
            className='mb-4',
        ),
    ],
    className='container-fluid px-4 bg-dark text-light',
)


@dash.callback(
    Output('incidents-graph', 'figure'),
    [
        Input('year-slider', 'value'),
        Input('race-slider', 'value'),
        Input('type-slider', 'value'),
    ],
)
def update_figure(selected_years, min_race_count, type_value):
    start_year, end_year = selected_years
    type_mapping = {0: 'per_race', 1: 'per_race_driver'}
    type_str = type_mapping[type_value]

    return cvm.create_incidents_figure(
        df, start_year, end_year, min_race_count, type_str
    )
