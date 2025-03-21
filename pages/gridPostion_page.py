import dash
import modules.driver_standings_mod as ds
import modules.driver_standings_vis_mod as dsv
import pandas as pd
from dash import Input, Output, dcc, html

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


############ Create Graphs ############
# somehow they are not created here
figure_all_time_standings = dsv.create_figure_all_time_standings(df)
figure_start_avg_placements = dsv.create_fig_start_avg_placements(
    df, df_race_completed
)

########## Set up the layout ##########

# Layout für das Dashboard
layout = html.Div(
    style={'fontFamily': 'Arial', 'margin': '20px'},
    children=[
        html.H1(
            'All time Grid and Finish Positions',
            style={'textAlign': 'center', 'color': 'white'},
        ),
        # Slider zur Eingabe der Anzahl der Fahrer
        html.Div(
            children=[
                html.Label(
                    'Choose the number of mininum races driven',
                    style={'color': 'white'},
                ),
                dcc.Slider(
                    id='driver-count-slider',
                    min=0,  # Minimumwert für die Anzahl der Fahrer
                    max=400,  # Maximumwert für die Anzahl der Fahrer
                    step=10,  # Schrittgröße
                    value=200,  # Startwert
                    marks={
                        i: str(i) for i in range(0, 401, 10)
                    },  # Markierungen bei jedem 10. Wert
                    tooltip={'placement': 'bottom', 'always_visible': True},
                ),
            ],
            style={'width': '80%', 'margin': '0 auto', 'textAlign': 'center'},
        ),
        # Dropdown-Menü zur Auswahl des Fahrers
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
        # Diagramm zur Anzeige der Positionen
        dcc.Graph(id='grid-finish-positions'),
        ############# Zweite Grafik
        html.H1('Grid and Finish position', style={'textAlign': 'center'}),
        # Slider, um den Wert von "number" festzulegen
        html.Div(
            [
                html.Label(
                    'Choose the number of mininum races on this circuit'
                ),
                dcc.Slider(
                    id='number-slider',
                    min=0,
                    max=30,  # Passen Sie den Max-Wert entsprechend an
                    step=1,
                    value=15,  # Standardwert
                    marks={i: str(i) for i in range(1, 31)},
                ),
            ],
            style={'textAlign': 'center', 'margin': '20px'},
        ),
        # Dropdown für die Streckenwahl, initial mit einer Beispiel-Strecke
        html.Div(
            [
                html.Label(
                    'List of circuits that have been driven on',
                    style={'textAlign': 'center'},
                ),
                dcc.Dropdown(
                    id='circuit-dropdown',
                    options=[],  # Optionen werden später dynamisch gesetzt
                    value='silverstone',  # Standardwert, der später dynamisch gesetzt wird
                    style={'width': '50%', 'margin': 'auto', 'color': 'black'},
                ),
            ],
            style={'textAlign': 'center', 'margin': '20px'},
        ),
        # Graph zur Anzeige der Heatmap
        dcc.Graph(id='heatmap'),
        ############## Dritte Grafik
        html.H1('Driver Placement Analysis'),
        # Interaktiver Schieberegler für die Anzahl der Rennen
        html.Label('Select the minimum number of races:'),
        dcc.Slider(
            id='races-slider',
            min=0,
            max=400,  # Maximale Anzahl der Rennen, die der Benutzer auswählen kann
            step=10,
            value=200,  # Standardwert
            marks={
                i: str(i) for i in range(0, 401, 10)
            },  # Markierungen auf dem Schieberegler
        ),
        # Graph-Komponente zur Anzeige der Grafik
        dcc.Graph(id='driver-placements'),
        ############################## Heatmap für standings aller driver
        dcc.Graph(figure=figure_all_time_standings),
        ########################## Avg Placements depending on start position
        dcc.Graph(figure=figure_start_avg_placements),
    ],
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
