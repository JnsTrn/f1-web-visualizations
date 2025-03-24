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


########## Set up the layout ##########

all_time_standings_explanation = ''' Test
'''

circuit_explanation =''' Test
'''

specific_driver_standings_explanation =''' Test
'''

weather_explanation = ''' Test
'''

sample_text = '''
This is a short explanation about what the graph is suppposed to show and what
we did to create it.
'''


layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    [
                        'How does the starting grid position influence the finishing '
                        'position of drivers in the seasons from 1994 - 2024?',
                    ],
                    className='text-center page-header',
                ),
                width={'size': 12, 'order': 1},
            ),
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
                            }

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
                    children=[
                        dcc.Graph(
                        figure= figure_all_time_standings,
                        config={'responsive': True}
                        ),
                    ],                  
                    style={
                        'margin': '0 auto',
                        'width': '92%',
                        #'display': 'flex',
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
                        'width': '92%',
                        #'display': 'flex',
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
                        'How does this differ between circuits that have '
                        'been driven on at least X times?',
                    ],
                    className='text-center page-header',
                ),
                width={'size': 12, 'order': 1},
            ),
            style={
                'backgroundImage': 'linear-gradient(to bottom, #b30412, #eb0e20)',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '5px 5px 15px rgba(0,0,0,0.2)',
            },
        ),

        dbc.Row(
            dbc.Col(
                html.Div([
                    html.Div(
                        [
                        html.Label(
                                'Choose mininum races driven on this circuit'
                        ),
                        dcc.Slider(
                            id='number-slider',
                            min=0,
                            max=30,  
                            step=1,
                            value=15,  
                            marks={i: str(i) for i in range(1, 31)},
                            ),
                        ],
                        style={'textAlign': 'center', 'margin': '20px'},
                    ),
                    html.Div(
                        [
                            html.Label(
                            'List of circuits',
                            style={'textAlign': 'center'},
                             ),
                            dcc.Dropdown(
                            id='circuit-dropdown',
                               options=[],  
                            value='silverstone',  
                            style={'width': '50%', 'margin': 'auto', 'color': 'black'},
                            ),
                        ],
                        style={'textAlign': 'center', 'margin': '20px'},
                    ),
                    dcc.Graph(id='heatmap'),
                ],                  
                ),
            ),
        className='mb-4',
        ),

        dbc.Row(
            dbc.Col(
                html.H1(
                    [
                        'Are there specific drivers who excel or struggle '
                        'more in wet conditions compared to dry conditions?',
                    ],
                    className='text-center page-header',
                ),
                width={'size': 12, 'order': 1},
            ),
            style={
                'backgroundImage': 'linear-gradient(to bottom, #b30412, #eb0e20)',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '5px 5px 15px rgba(0,0,0,0.2)',
            },
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
                            style={
                                'fontSize': '18px',
                                'lineHeight': '1.6',
                                'width': '93%',
                                'margin': '0 auto',
                                'textAlign': 'justify',
                            }

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
                html.H1(
                    [
                        'How does this differ between drivers of different experience'
                        'levels (as determined by the amount of races they participated in)',
                    ],
                    className='text-center page-header',
                ),
                width={'size': 12, 'order': 1},
            ),
            style={
                'backgroundImage': 'linear-gradient(to bottom, #b30412, #eb0e20)',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '5px 5px 15px rgba(0,0,0,0.2)',
            },
        ),

        dbc.Row(
            dbc.Col(
                html.Div([
                    html.Div(
                        children=[
                            html.Label(
                                'Choose mininum races driven',
                                style={'color': 'white'},
                            ),
                            dcc.Slider(
                                id='driver-count-slider',
                                min=0,  
                                max=400,  
                                step=10,  
                                value=200,  
                                marks={
                                    i: str(i) for i in range(0, 401, 10)
                                },  
                                tooltip={'placement': 'bottom', 'always_visible': True},
                            ),
                        ],
                        style={'width': '80%', 'margin': '0 auto', 'textAlign': 'center'},
                    ),
                    html.Div(
                        children=[
                            html.Label(
                                'List of Drivers with chosen amount of races:',
                                style={'color': 'white'},
                            ),
                            dcc.Dropdown(
                                id='driver-dropdown',
                                value='Michael Schumacher',
                                style={'width': '50%', 'margin': 'auto', 'color': 'black'},
                            ),
                        ],
                        style={
                            'width': '80%',
                            'margin': '20px auto',
                            'textAlign': 'center',
                        },
                    ), 
                    dcc.Graph(id='grid-finish-positions'),
                ],                  
                ),
            ),
            className='mb-4',
        ),

        dbc.Row(
            dbc.Col(
                html.Div([
                    dcc.Slider(
                        id='races-slider',
                        min=0,
                        max=400,  
                        step=10,
                        value=200, 
                        marks={
                        i: str(i) for i in range(0, 401, 10)
                        },  
                    ),
                    dcc.Graph(id='driver-placements'),                      
                ],
                ),
            ),
            className='mb-4'
        ),

        dbc.Row(
            dbc.Col(
                html.Div(                   

                ),
            ),
        ),

        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.P(

                        ),
                    ],

                ),
            ),
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


############ Callbacks #############

# Callback zum Aktualisieren der Dropdown-Optionen basierend auf dem Slider-Wert
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
def update__grid_finish_figure(selected_driver):
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
    return dsv.update_dropdown_and_heatmap(slider_value, selected_circuit, df)


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