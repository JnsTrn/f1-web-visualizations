import crash_vis_mod as cvm
import dash_bootstrap_components as dbc
import pandas as pd
import plots as plt
from dash import dcc, html

############## Load Data ##############

DATA_PATH = 'data/'

df = pd.read_csv(
    DATA_PATH + 'f1_1994_2024_categorized_by_race_status.csv',
    parse_dates=['date'],
)

df_CraWeath = pd.read_csv(DATA_PATH + 'crashes_and_weather.csv')


# ############ Define Graphs ############

plt.init_figs()
fig_CraWeath = plt.create_fig_CraWeath(df_CraWeath)
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
This graph shows the total number of incidents per year in Formula 1 from 1994
to 2024.Incidents include accidents, mechanical failures, and other reasons
for non-finishes. We can observe that the total number of incidents has
decreased over time, likely due to improved safety standards and car
reliability. The peaks in certain years may correspond to regulation changes
or particularly challenging seasons.
"""

retirement_rate_explanation = """
The retirement rate represents the percentage of cars that did not finish the
race compared to the total number of starters.This metric helps us understand
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


layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    'Retirement Analysis', className='text-center text-light'
                ),
                width=22,
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
                            total_incidents_explanation,
                            style={
                                'fontSize': '16px',
                                'lineHeight': '1.6',
                                'width': '86%',
                                'margin': '0 auto',
                            },
                        ),
                    ],
                    className='p-3 bg-dark text-light',
                ),
                width=12,
            ),
            className='mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H3(
                            'Total Incidents by Year',
                            className='text-center',
                            style={'fontSize': '22px'},
                        ),
                        html.Div(
                            dcc.Graph(
                                figure=fig_total_incidents,
                                config={'responsive': True},
                            ),
                            style={
                                'margin': '0 auto',
                                'width': '85%',
                            },
                        ),
                    ]
                ),
                width=22,
            ),
            className='mb-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H3(
                            'Retirement Rate by Year',
                            className='text-center',
                            style={'fontSize': '22px'},
                        ),
                        html.Div(
                            dcc.Graph(
                                figure=fig_retirements_rate,
                                config={'responsive': True},
                            ),
                            style={
                                'margin': '0 auto',
                                'width': '85%',
                            },
                        ),
                    ]
                ),
                width=22,
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
                                'fontSize': '16px',
                                'lineHeight': '1.6',
                                'width': '86%',
                                'margin': '0 auto',
                            },
                        ),
                    ],
                    className='p-3 bg-dark text-light',
                ),
                width=12,
            ),
            className='mb-5',
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
                                'fontSize': '16px',
                                'lineHeight': '1.6',
                                'width': '86%',
                                'margin': '0 auto',
                            },
                        ),
                    ],
                    className='p-3 bg-dark text-light',
                ),
                width=12,
            ),
            className='mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H3(
                            'Average Retirements per Race by Year',
                            className='text-center',
                            style={'fontSize': '22px'},
                        ),
                        html.Div(
                            dcc.Graph(
                                figure=fig_retirements_race,
                                config={'responsive': True},
                            ),
                            style={
                                'margin': '0 auto',
                                'width': '85%',
                            },
                        ),
                    ]
                ),
                width=22,
            ),
            className='mb-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H3(
                            'Crash Rate by Weather',
                            className='text-center',
                            style={'fontSize': '22px'},
                        ),
                        html.Div(
                            dcc.Graph(
                                figure=fig_CraWeath,
                                config={'responsive': True},
                            ),
                            style={
                                'margin': '0 auto',
                                'width': '85%',
                            },
                        ),
                    ]
                ),
                width=22,
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
                            crash_weather_explanation,
                            style={
                                'fontSize': '16px',
                                'lineHeight': '1.6',
                                'width': '86%',
                                'margin': '0 auto',
                            },
                        ),
                    ],
                    className='p-3 bg-dark text-light',
                ),
                width=12,
            ),
            className='mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    incidents_layout,
                    style={
                        'width': '85%',
                        'margin': '0 auto',
                    },
                ),
                width=22,
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
                                'fontSize': '16px',
                                'lineHeight': '1.6',
                                'width': '86%',
                                'margin': '0 auto',
                            },
                        ),
                    ],
                    className='p-3 bg-dark text-light',
                ),
                width=12,
            ),
            className='mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.A(
                        'Back to Top', href='#top', className='btn btn-success'
                    ),
                    className='text-center',
                ),
                width=12,
            ),
            className='mb-4',
        ),
    ],
    className='container-fluid px-4 bg-dark text-light',
)


###### Register Callbacks ################
def retirement_callbacks(app):
    cvm.register_callbacks(app, df)
