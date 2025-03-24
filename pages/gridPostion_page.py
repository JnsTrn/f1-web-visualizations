import pandas as pd
import dash

from dash import Input, Output, dcc, html

import dash_bootstrap_components as dbc

import modules.driver_standings_mod as ds
import modules.driver_standings_vis_mod as dsv


####### Initialize the Dash app #######

dash.register_page(__name__, path='/gridPosition')


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

graph_dry = dcc.Graph(
    id='graph-dry',
    figure=figure_driver_dry
)

graph_wet = dcc.Graph(
    id='graph-wet',
    figure=figure_driver_mw
)

circuit_heatmap = dsv.create_circuit_heatmap_layout()
driver_grid_start_finish = dsv.create_grid_finish_figure_layout()
all_drivers_avg = dsv.create_avg_all_drivers_figure_layout()

########## Set up the layout ##########

all_time_standings_explanation = '''
This is a great analysis of what the plot depicts and totally not just some
filler text for the sole purpose of seeing how more text looks inside the
boxes.
'''

circuit_explanation ='''
This is a great analysis of what the plot depicts and totally not just some
filler text for the sole purpose of seeing how more text looks inside the
boxes.
'''

specific_driver_standings_explanation ='''
This is a great analysis of what the plot depicts and totally not just some
filler text for the sole purpose of seeing how more text looks inside the
boxes.
'''

weather_explanation = '''
This is a great analysis of what the plot depicts and totally not just some
filler text for the sole purpose of seeing how more text looks inside the
boxes.
'''

sample_text = '''
This is a short explanation about what the graph is suppposed to show and what
we did to create it.
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
                        'finishing position',
                        html.Br(),
                        ' of drivers in the seasons from 1994 - 2024?',
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
                            sample_text,
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
            className='mb-4',
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
                html.Div([
                    html.Div([
                        html.Button('Dry', id='dry-button', n_clicks=0),
                        html.Button('Wet', id='wet-button', n_clicks=0),
                    ], style={'marginBottom': '20px'}),
                    dcc.Store(id='last-clicked', data='dry-button'),
                    dcc.Graph(id='graph', figure=figure_driver_dry)
                ]),
            ),
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
                html.H1(
                    [
                        'How does this differ between drivers of different '
                        'experience levels ',
                        html.Br(),
                        '(as determined by the amount of races '
                        'they participated in)?',
                    ],
                    className='text-center page-header text-light',
                ),
            ),
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
            className='mb-4',
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

# Callback zum Aktualisieren der Dropdown-Optionen basierend
# auf dem Slider-Wert
@dash.callback(
    Output('driver-dropdown', 'options'),
    Input('driver-count-slider', 'value'),
)
def update_driver_dropdown(driver_count):
    # Holen Sie sich die Liste der Fahrer basierend auf dem Wert des Sliders
    drivers = ds.driver_list(driver_count, df)
    drivers = sorted(drivers)  # Alphabetisch sortieren
    return [{'label': driver, 'value': driver} for driver in drivers]


# Callback zum Aktualisieren der Grafik basierend auf der Auswahl des Fahrers
@dash.callback(
    Output('grid-finish-positions', 'figure'),
    Input('driver-dropdown', 'value'),
)
def update_grid_finish_figure(selected_driver):
    return dsv.create_grid_finish_figure(selected_driver, df)


# Callback zum Abrufen der Dropdown-Optionen und Aktualisieren der Heatmap
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


# Callback zur Aktualisierung der Grafik basierend auf dem Schieberegler-Wert
@dash.callback(
    Output('driver-placements', 'figure'),
    Input('races-slider', 'value'),
)
def update_avg_all_drivers_graph(amount_of_races):
    return dsv.create_avg_all_drivers_figure(
        amount_of_races, df, df_race_completed
    )

@dash.callback(
    Output('last-clicked', 'data'),
    [Input('dry-button', 'n_clicks'),
     Input('wet-button', 'n_clicks')]
)
def store_last_clicked(dry_clicks, wet_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return button_id

@dash.callback(
    Output('graph', 'figure'),
    [Input('last-clicked', 'data')]
)
def update_graph(last_clicked):
    if last_clicked == 'dry-button':
        return figure_driver_dry
    elif last_clicked == 'wet-button':
        return figure_driver_mw
    return dash.no_update
