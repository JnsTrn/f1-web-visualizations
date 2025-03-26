import pandas as pd
import dash

from dash import Input, Output, dcc, html

import dash_bootstrap_components as dbc

import modules.crash_vis_mod as cvm
import modules.weather_crash_vis_mod as wcvm


####### Initialize the Dash app #######

dash.register_page(__name__, path='/retirements', title='Retirement Analysis')


############## Load Data ##############


DATA_PATH = 'data/'

df = pd.read_csv(
    DATA_PATH + 'f1_1994_2024_categorized_by_race_status.csv',
    parse_dates=['date'],
)
df_CraWeath = pd.read_csv(DATA_PATH + 'crashes_and_weather.csv')


############# Define Graphs ############


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


########### Set up the layout ###########

total_incidents_explanation = '''
In the early years of the dataset, technical failures were the primary cause of
retirements, consistently outnumbering crash-related retirements. It wasn't
until 2005 that they declined to comparable levels. The spikes observed in 2006
and 2010 can largely be attributed to an increased number of technical failures.

These increases correlate with major regulation changes: In 2006, Formula 1
transitioned from V10 to V8 engines, requiring teams to adapt to new cooling,
fuel efficiency, and durability demands, while the grid expanded from 20 to 22
drivers. Similarly, in 2010, the grid size increased to 24 drivers (up from 20),
and new rules such as the ban on in-race refueling and the 8-engine season
limit introduced in 2009 along with a higher number of races, likely
contributed to this rise in technical failures.

Crash-related retirements have also declined but followed a different pattern
than technical failures. After dropping from 90 in 1994 to 29 in 2003, they
rebounded to around 50 per season from 2003 to 2013 before stabilizing at 30
per season from 2013 onward.
'''

retirement_rate_explanation = '''
The retirement rate represents the percentage of cars that did not finish the
race compared to the total number of starters. This metric helps us understand
the reliability and safety evolution in F1 over three decades. The downward
trend suggests that modern F1 cars are significantly more reliable than their
predecessors. Notably, the introduction of hybrid power units in 2014 initially
caused a spike in retirements as teams adapted to the new technology, but
reliability quickly improved in subsequent seasons.
'''

retirements_race_explanation = '''
This visualization shows the average number of retirements per race for each
season. It provides insight into how race attrition has changed over time.
Early seasons in our dataset show significantly higher average retirements per
race, sometimes exceeding 13 cars per race, while recent seasons typically see
fewer than 4 retirements per race. This improvement reflects advancements in
engineering, manufacturing processes, and overall design philosophy in modern
Formula 1.
'''

crash_weather_explanation = '''
Observations reveal that wet weather is associated with a significantly higher
incident rate compared to dry and mixed weather conditions. Interestingly, the
technical failure rate is lower during mixed and wet weather compared to dry
conditions. This may be because lower driving speeds in wet weather reduce
stress on the car. Additionally, races in wet conditions are more likely to
end prematurely (race abandonment), leaving less opportunity for technical
failures to occur.
'''

crash_weather_chi2 = '''
It is worth noting that the data for wet weather, and especially mixed weather
conditions, is relatively sparse, meaning single events could have a larger
impact on the results.

To determine whether there is a significant relationship between weather
conditions and race completion status in generel, a Chi-Square test was
conducted. The test produced a Chi-Square value of 59.38 and a P-value of 6e-11,
indicating a statistically significant relationship at a significance level of
6e-11.
'''

interactive_dashboard_explanation_monaco = '''
Among circuits raced on 5 or more times from 1994-2024, Monaco stands out with
the highest average number of crashes per race. This isn't surprising given
its reputation as one of the most challenging tracks. With a narrow layout
surrounded by walls and barriers and almost no runoff areas, it offers drivers
little margin for error, making crashes more likely.
'''

interactive_dashboard_explanation_australia = '''
Albert Park, home to the Australian Grand Prix, has one of the highest
retirement rates across nearly all time periods. It often serves as the first
race of the season, which may explain this trend. As the first real-world test
for many cars, previously unknown technical issues may arise, leading to a
higher rate of retirements.
'''

interactive_dashboard_explanation_imola = '''
Imola stands out for its high technical failure rates, especially from 1994 to
2006, a period marked by frequent mechanical issues across many circuits.
However, since its return to the F1 calendar in 2019, its technical failure
rate has been below average in the four times it has been raced, suggesting
that past failures at the track were likely more related to the era's overall
technical challenges than the circuit itself.
'''

retirements_text = '''
In Formula 1, a driver may be forced to retire from a race due to either
technical failures or crashes. Technical Failures include mechanical and
reliability issues such as engine failures, hydraulic problems, brake
malfunctions, and other mechanical defects. Incidents/Crashes refer to
race-ending collisions, whether caused by driver errors (such as oversteering
into a barrier) or contact with other cars. Total Retirements is the sum of
these two categories, representing all cases where a driver was unable to
finish the race.
'''


layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.Div(className="chequered-flag"),
            ),
            className='mb-4'
        ),
        dbc.Row(
            dbc.Col(
                html.H1(
                    [
                        'How has the total number of crashes and retirements '
                        'evolved in the seasons from 1994 - 2024?',
                    ],
                    className='text-center page-header text-light',
                ),
            ),
            className='mb-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            retirements_text,
                        ),
                    ],
                    className='p-3 text-light',
                    style={
                        'width': '89%',
                        'margin': '0 auto',
                        'backgroundColor': '#212529',
                        'border-radius': '10px',
                    }
                ),
            ),
            className='mb-4 mt-4',
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
                                'width': '89%',
                            },
                        ),
                    ]
                ),
            ),
            className='mb-2'
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
                                'width': '89%',
                            },
                        ),
                    ],
                ),
            ),
            className='mb-2'
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
                                'width': '89%',
                            },
                        ),
                    ]
                ),
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            total_incidents_explanation,
                        ),
                    ],
                    className='p-3 text-light',
                    style={
                        'width': '89%',
                        'margin': '0 auto',
                        'backgroundColor': '#212529',
                        'border-radius': '10px',
                    }
                ),
            ),
            className='mt-2 mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(className="chequered-flag"),
            ),
            className='mb-4 mt-4'
        ),
        dbc.Row(
            dbc.Col(
                html.H1(
                    [
                        'Which tracks have the highest frequency of crashes '
                        'or retirements compared to others?',
                    ],
                    className='text-center page-header text-light',
                ),
            ),
            className='mb-4 mt-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    incidents_layout,
                    style={
                        'width': '89%',
                        'margin': '0 auto',
                    },
                ),
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            [
                                interactive_dashboard_explanation_monaco,
                                html.Br(),
                                interactive_dashboard_explanation_australia,
                                html.Br(),
                                interactive_dashboard_explanation_imola,
                            ],
                        ),
                    ],
                    className='p-3 text-light',
                    style={
                        'width': '89%',
                        'margin': '0 auto',
                        'backgroundColor': '#212529',
                        'border-radius': '10px',
                    }
                ),
            ),
            className='mt-2 mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(className="chequered-flag"),
            ),
            className='mb-4 mt-4'
        ),
        dbc.Row(
            dbc.Col(
                html.H1(
                    [
                        'How does weather affect race completion rates and '
                        'the likelihood of crashes or retirements in the '
                        'seasons from 2005 - 2024?',
                    ],
                    className='text-center page-header text-light',
                ),
            ),
            className='mb-4 mt-4',
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
                                'width': '89%',
                            },
                        ),
                    ]
                ),
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            [
                                crash_weather_explanation,
                                html.Br(),
                                crash_weather_chi2,
                            ],
                        ),
                    ],
                    className='p-3 text-light',
                    style={
                        'width': '89%',
                        'margin': '0 auto',
                        'backgroundColor': '#212529',
                        'border-radius': '10px',
                    }
                ),
            ),
            className='mt-2 mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(className="chequered-flag"),
            ),
            className='mb-4 mt-4'
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.A(
                        'Back to Top',
                        href='#top',
                        className='btn',
                        style={
                        'backgroundColor': '#a36664',
                        'color': 'white',
                        }
                    ),
                    className='text-center',
                ),
            ),
        ),
    ],
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
