import pandas as pd
import dash

from dash import Input, Output, dcc, html

import dash_bootstrap_components as dbc

import modules.driver_standings_mod as ds
import modules.driver_standings_vis_mod as dsv


####### Initialize the Dash app #######

dash.register_page(__name__, path='/gridPosition', title='Grid Position Analysis')

############## Load Data ##############

df = pd.read_csv('data/f1_1994_2024_season_results.csv')

race_status = set(
    [
        'Finished',
        '+1 Lap',
        '+2 Laps',
        '+3 Laps',
        '+4 Laps',
        '+5 Laps',
        '+7 Laps',
        '+6 Laps',
        '+8 Laps',
        '+12 Laps',
        '+11 Laps',
        '+26 Laps',
        '+17 Laps',
        '+10 Laps',
        '+9 Laps',
        '+42 Laps',
        '+14 Laps',
    ]
)

df_race_completed = df
df_race_completed['race_completed'] = df['status'].isin(race_status)
df_race_completed = df_race_completed[
    df_race_completed['race_completed']
].drop(columns=['race_completed'])
name =''

df_weather = pd.read_csv('data/f1_1994_2024_season_results_completed_weather.csv')


############ Create Graphs ############

figure_all_time_standings = dsv.create_figure_all_time_standings(df)
figure_start_avg_placements = dsv.create_fig_start_avg_placements(
    df, df_race_completed
)
spcific_driver_layout = dsv.create_grid_finish_figure(name,df)

figure_driver_mw = dsv.driver_standings_mw(df_weather)
figure_driver_dry = dsv.driver_standings_dry(df_weather)


circuit_heatmap = dsv.create_circuit_heatmap_layout()
driver_grid_start_finish = dsv.create_grid_finish_figure_layout()
all_drivers_avg = dsv.create_avg_all_drivers_figure_layout()
driver_conditions = dsv.create_driver_conditions_layout()

########## Set up the layout ##########
question_1_exp= '''Qualifying takes place a day before the race and determines
the starting grid positions. How much impact does the starting position have
on the outcome? Is the race essentially decided before it even begins?
'''

question_2_exp = '''Formula 1 has many different tracks that 
not only vary in their geographical location but also in their layout. Do 
different circuits lead to different race results? Do certain circuits 
provide better chances for winning a race?
'''

question_3_exp = '''
Some Formula 1 drivers have long careers, with numerous seasons and races 
under their belts. Can these long careers be justified by looking at the 
race results ?
'''

question_4_exp = ''' Wet races are not common in Formula 1. Not only 
are they rare, but driving in wet conditions is also usually more 
challenging for a driver, as the tracks are slipperier and visibility 
is significantly reduced. Which driver handles these difficult conditions 
the best?
'''

graph_one = '''This heatmap shows the relationship between starting positions 
and their corresponding finishing positions. While starting from pole position 
significantly increases the likelihood of winning, in most
cases, the finishing position tends to fall within a 2-place range of the 
starting position.'''

all_time_standings_explanation = '''To account for the impact of retirements 
or disqualifications, which can skew the race results, the data has been 
categorized into 'races completed' and 'all races'.  '''

circuit_explanation ='''In this interactive graph, you can select a number for
races driven. The dropdown menu will then display the different circuits that have
been raced on at least the number of times you selected. Similar to the first
graph, a heatmap is shown to illustrate the relationship between starting
and finishing positions
'''

specific_driver_standings_explanation ='''
Similar to the graph above, you can also filter by a minimum number of races 
driven. This graph displays and compares the average placement of each driver.
Additionally, the graph was also categorized in completed races and all 
races. For example, two-time World Champion Mika Häkkinen was an excellent
driver when he finished races which might not be apparent looking at only
the data for 'all races'.
'''

weather_explanation = '''
Reliable weather data has been available only since 2005. Since wet and mixed 
conditions are relatively rare, these two categories have been combined. To 
ensure representative data, the focus is on drivers who have participated in 
at least 20 wet and/or mixed races. The option to switch between dry and 
wet/mixed conditions allows for viewing a driver's average placement based on 
the specific weather condition.
'''


graph_four = ''' This bar chart shows the all-time starting and finishing
positions of a driver. You can select the number of races driven, and a dropdown
menu of drivers who have competed in the selected number of races will be displayed.
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
                        'How does the starting grid position influence the '
                        'finishing position of drivers in the seasons '
                        'from 1994 - 2024?',
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
                            question_1_exp,
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
            className='mb-2 mt-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=
                    [
                        dcc.Graph(
                        figure= figure_all_time_standings,
                        config={'responsive': True}
                        ),
                    ],
                    style={
                        'margin': '0 auto',
                        'width': '89%',
                        'justifyContent': 'center'
                    },
                ),
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            graph_one,
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
                html.Div(
                    children=[
                        dcc.Graph(
                        figure= figure_start_avg_placements,
                        config={'responsive': True}
                        ),
                    ],
                    style={
                        'margin': '0 auto',
                        'width': '89%',
                        'justifyContent': 'center'
                    },
                ),
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            all_time_standings_explanation,
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
            className='mb-4'
        ),
        dbc.Row(
            dbc.Col(
                html.H1(
                    [
                        'How does this differ between circuits that have '
                        'been driven on at least X times?',
                    ],
                    className='text-center page-header text-light',
                ),
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            question_2_exp,
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
            className='mb-2 mt-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    circuit_heatmap,
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
                            circuit_explanation,
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
            className='mb-4'
        ),
        dbc.Row(
            dbc.Col(
                html.H1(
                    [
                        'How does this differ between drivers of different '
                        'experience levels (as determined by the amount of '
                        'races they participated in)?',
                    ],
                    className='text-center page-header text-light',
                ),
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            question_3_exp,
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
            className='mb-2 mt-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    driver_grid_start_finish,
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
                            graph_four,
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
                html.Div(
                    all_drivers_avg,
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
                            specific_driver_standings_explanation,
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
            className='mb-5',
        ),
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
                        'Are there specific drivers who excel or struggle '
                        'more in wet conditions compared to dry conditions?',
                    ],
                    className='text-center page-header text-light',
                ),
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            question_4_exp,
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
            className='mb-2 mt-4',
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    driver_conditions,
                    style={
                        'width': '89%',
                        'margin': '0 auto',
                    }
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            weather_explanation,
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
            className='mb-4'
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


############ Callbacks #############

@dash.callback(
    Output('driver-dropdown', 'options'),
    Input('driver-count-slider', 'value'),
)
def update_driver_dropdown(driver_count):
    drivers = ds.driver_list(driver_count, df)
    drivers = sorted(drivers)
    return [{'label': driver, 'value': driver} for driver in drivers]


@dash.callback(
    Output('grid-finish-positions', 'figure'),
    Input('driver-dropdown', 'value'),
)
def update_grid_finish_figure(selected_driver):
    return dsv.create_grid_finish_figure(selected_driver, df)


@dash.callback(
    [
        Output('circuit-dropdown', 'options'),
        Output('circuit-dropdown', 'value'),
        Output('heatmap', 'figure'),
    ],
    [
        Input('number-slider', 'value'),
        Input('circuit-dropdown', 'value'),
    ],
)
def update_dropdown_and_heatmap(slider_value, selected_circuit):
    return dsv.create_circuit_heatmap(slider_value, selected_circuit, df)


@dash.callback(
    Output('driver-placements', 'figure'),
    Input('races-slider', 'value'),
)
def update_avg_all_drivers_graph(amount_of_races):
    return dsv.create_avg_all_drivers_figure(
        amount_of_races, df, df_race_completed
    )

@dash.callback(
    Output('graph', 'figure'),
    [Input('dry-button', 'n_clicks'),
     Input('wet-button', 'n_clicks')],
    prevent_initial_call=False
)
def update_graph(dry_clicks, wet_clicks):
    # Determine which button was last clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        # If no button has been clicked, return the default (dry) figure
        return figure_driver_dry

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'dry-button':
        return figure_driver_dry
    elif button_id == 'wet-button':
        return figure_driver_mw
