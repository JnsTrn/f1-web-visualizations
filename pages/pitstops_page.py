import dash
import pandas as pd
import plotly.express as px

from dash import Input, Output, html

import dash_bootstrap_components as dbc

import modules.pitstop_mod as ptm


####### Initialize the Dash app #######

dash.register_page(__name__, path='/pitstops')


############## Load Data ##############

DATA_PATH = 'data/'

df = pd.read_csv(
    DATA_PATH + 'merged_pitstops.csv',
)

# Konvertiere 'duration' in numerische Werte und entferne NaN-Werte
df_unique = df
df_unique['duration'] = df_unique['duration'].apply(
    ptm.convert_duration_to_seconds
)
df_unique = df_unique.dropna(subset=['duration'])

# Einzigartige Rennstrecken abrufen
unique_circuits = df_unique['race_name'].unique()

df_filtered = df[['year', 'driver_name', 'duration', 'finish_position']].copy()
df_filtered['duration'] = df_filtered['duration'].apply(
    ptm.convert_duration_to_seconds
)
df_filtered = df_filtered.dropna(subset=['duration'])

# Fahrer filtern, die mindestens 3 Jahre gefahren sind
driver_years = df_filtered.groupby('driver_name')['year'].nunique()
eligible_drivers = driver_years[driver_years >= 2].index


############## Create Graphs ##############

pitstops_layout = ptm.create_pitstop_layout(unique_circuits)
pitstops_boxplot = ptm.create_pitstop_layout_boxplot(eligible_drivers)


############ Set up the layout ############

sample_text = '''
This is a short explanation about what the graph is suppposed to show and what
we did to create it.
'''

explanation_text = '''
This is an analysis.
'''

layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    [
                        'How does the number and the average duration of '
                        'pitstops ',
                        html.Br(),
                        'for a driver in a race relate to his '
                        'finishing position? ',
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
                    pitstops_boxplot,
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
                        html.P(
                            explanation_text,
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
            className='mb-8 mt-4',
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
                    pitstops_layout,
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
                        html.P(
                            explanation_text,
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
            className='mb-8 mt-4',
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


########### Initialize Callbacks ############

# Callback zur Aktualisierung der Jahr-Dropdown-Liste basierend auf
# der Rennstrecke
@dash.callback(
    [Output('year-dropdown', 'options'), Output('year-dropdown', 'value')],
    Input('circuit-pitstops-dropdown', 'value'),
)
def update_year_dropdown(selected_circuit):
    filtered_years = df[df['race_name'] == selected_circuit]['year'].unique()
    year_options = [
        {'label': str(year), 'value': year} for year in sorted(filtered_years)
    ]
    return year_options, filtered_years[0] if len(filtered_years) > 0 else None


# Callback zur Erstellung der Visualisierungen
@dash.callback(
    [
        Output('pitstop-boxplot', 'figure'),
        Output('pitstop-barplot', 'figure'),
        Output('race-info', 'children'),
    ],
    [
        Input('circuit-pitstops-dropdown', 'value'),
        Input('year-dropdown', 'value'),
    ],
)
def update_pitstop_plot(selected_circuit, selected_year):
    if not selected_circuit or not selected_year:
        return (
            px.box(title='No Data Available'),
            px.bar(title='No Data Available'),
            html.P('No Data Available'),
        )

    # Daten für das ausgewählte Rennen und Jahr filtern
    filtered_df = df_unique[
        (df_unique['race_name'] == selected_circuit)
        & (df_unique['year'] == selected_year)
    ]

    # Nur Fahrer berücksichtigen, die das Rennen beendet haben
    filtered_df = filtered_df[(filtered_df['race_completed'] == True)]

    # Pitstop-Zeiten pro Fahrer summieren & Endplatzierung hinzufügen
    driver_pitstops = (
        filtered_df.groupby(['driver_name', 'finish_position'])['duration']
        .sum()
        .reset_index()
    )

    # Einteilung in 3 Kategorien nach Gesamt-Pitstop-Zeit (hohe Zahlen = langsam)
    driver_pitstops_sorted = driver_pitstops.sort_values(
        'duration', ascending=True
    )  # Aufsteigend für bessere Kategorisierung

    driver_pitstops_sorted['duration_category'] = pd.cut(
        driver_pitstops_sorted['duration'],
        bins=[driver_pitstops_sorted['duration'].min()]
        + driver_pitstops_sorted['duration']
        .quantile([0.33, 0.66, 1.0])
        .tolist(),
        labels=['Fast', 'Average', 'Slow'],  # Niedrige Werte = Schnell
        include_lowest=True,
    )

    # **Boxplot für Pitstop-Kategorie vs. Endplatzierung**
    fig_box = px.box(
        driver_pitstops_sorted,
        x='duration_category',
        y='finish_position',
        color='duration_category',
        labels={
            'duration_category': 'Pitstop-Kategorie',
            'finish_position': 'Endplatzierung',
        },
        title=f'Pitstop Analysis: {selected_circuit} ({selected_year})',
        template='plotly_dark',
    )

    # Balkendiagramm für Gesamt-Pitstop-Zeit pro Fahrer mit Endplatzierung
    # als Farbskala
    fig_bar = px.bar(
        driver_pitstops_sorted,
        x='driver_name',
        y='duration',
        text='duration',
        labels={
            'driver_name': 'Driver',
            'duration': 'Total Pitstop Time (s)',
        },
        title=f'Total Pitstop Time per Driver({selected_circuit}, {selected_year})',
        template='plotly_dark',
        color='finish_position',
        color_continuous_scale=[
            [0, 'rgb(255, 0, 0)'],  # Rot für Platz 1
            [0.2, 'rgb(255, 100, 100)'],  # Helles Rot
            [0.4, 'rgb(255, 150, 150)'],  # Etwas helleres Rot
            [0.6, 'rgb(255, 200, 200)'],  # Sehr helles Rot
            [0.8, 'rgb(255, 255, 255)'],  # Weiß für höhere Platzierungen
            [1, 'rgb(255, 255, 255)'],  # Weiß für die letzten Plätze
        ],
    )
    fig_bar.update_traces(texttemplate='%{text:.2f}s', textposition='outside')

    # Anzahl der Fahrer pro Kategorie berechnen
    category_counts = (
        driver_pitstops_sorted['duration_category'].value_counts().to_dict()
    )

    # Min- und Max-Zeiten für jede Kategorie berechnen
    try:
        fast_range = (
            driver_pitstops_sorted[
                driver_pitstops_sorted['duration_category'] == 'Fast'
            ]['duration'].min(),
            driver_pitstops_sorted[
                driver_pitstops_sorted['duration_category'] == 'Fast'
            ]['duration'].max(),
        )
        medium_range = (
            driver_pitstops_sorted[
                driver_pitstops_sorted['duration_category'] == 'Average'
            ]['duration'].min(),
            driver_pitstops_sorted[
                driver_pitstops_sorted['duration_category'] == 'Average'
            ]['duration'].max(),
        )
        slow_range = (
            driver_pitstops_sorted[
                driver_pitstops_sorted['duration_category'] == 'Slow'
            ]['duration'].min(),
            driver_pitstops_sorted[
                driver_pitstops_sorted['duration_category'] == 'Slow'
            ]['duration'].max(),
        )
    except ValueError:
        return fig_box, fig_bar, html.P('No Data Available')

    # Info-Text mit Anzahl der Rennen und Zeitbereichen
    info_text = html.Div(
        [
            html.P(f'Number of Drivers: {len(driver_pitstops_sorted)}'),
            html.P(
                f'Fast ({category_counts.get('Fast', 0)} Drivers): {fast_range[0]:.2f}s - {fast_range[1]:.2f}s'
            ),
            html.P(
                f'Average ({category_counts.get('Average', 0)} Drivers): {medium_range[0]:.2f}s - {medium_range[1]:.2f}s'
            ),
            html.P(
                f'Slow ({category_counts.get('Slow', 0)} Drivers): {slow_range[0]:.2f}s - {slow_range[1]:.2f}s'
            ),
        ]
    )

    return fig_box, fig_bar, info_text


# Callback für die Aktualisierung des Diagramms
@dash.callback(
    [Output('boxplot', 'figure'), Output('race-boxplot-info', 'children')],
    [Input('driver-pitstop-dropdown', 'value')],
)
def update_plot(driver_name):
    df_driver = df_filtered[df_filtered['driver_name'] == driver_name].copy()
    total_races = len(df_driver)

    # Sortieren nach Pitstop-Dauer
    df_driver_sorted = df_driver.sort_values('duration')

    # Pitstop-Dauer in 3 Kategorien aufteilen
    df_driver_sorted['duration_category'] = pd.cut(
        df_driver_sorted['duration'],
        bins=[df_driver_sorted['duration'].min()]
        + df_driver_sorted['duration'].quantile([0.33, 0.66, 1.0]).tolist(),
        labels=['Fast', 'Average', 'Slow'],  # Kategorien umkehren
        include_lowest=True,
    )

    # Boxplot erstellen mit dunklem Design
    fig = px.box(
        df_driver_sorted,
        x='duration_category',
        y='finish_position',
        color='duration_category',
        labels={
            'duration_category': 'Pitstop-Speed',
            'finish_position': 'Finishing Position',
        },
        title=f'Pitstop Analysis: {driver_name}',
        template='plotly_dark',
    )

    # Anzahl der Rennen pro Kategorie und Zeitbereiche berechnen
    category_counts = (
        df_driver_sorted['duration_category'].value_counts().to_dict()
    )

    slow_range = (
        df_driver_sorted[df_driver_sorted['duration_category'] == 'Slow'][
            'duration'
        ].min(),
        df_driver_sorted[df_driver_sorted['duration_category'] == 'Slow'][
            'duration'
        ].max(),
    )
    medium_range = (
        df_driver_sorted[df_driver_sorted['duration_category'] == 'Average'][
            'duration'
        ].min(),
        df_driver_sorted[df_driver_sorted['duration_category'] == 'Average'][
            'duration'
        ].max(),
    )
    fast_range = (
        df_driver_sorted[df_driver_sorted['duration_category'] == 'Fast'][
            'duration'
        ].min(),
        df_driver_sorted[df_driver_sorted['duration_category'] == 'Fast'][
            'duration'
        ].max(),
    )

    # Infos zur Anzahl der Rennen je Kategorie + Zeitbereiche
    info_text = html.Div(
        [
            html.P(f'Number of Races: {total_races}'),
            html.P(
                f'Fast ({category_counts.get('Fast', 0)} Races): {fast_range[0]:.2f}s - {fast_range[1]:.2f}s'
            ),
            html.P(
                f'Average ({category_counts.get('Average', 0)} Races): {medium_range[0]:.2f}s - {medium_range[1]:.2f}s'
            ),
            html.P(
                f'Slow ({category_counts.get('Slow', 0)} Races): {slow_range[0]:.2f}s - {slow_range[1]:.2f}s'
            ),
        ]
    )

    return fig, info_text
