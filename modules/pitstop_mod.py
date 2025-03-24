import numpy as np
import pandas as pd
import plotly.express as px

from dash import dcc, html


def create_pitstop_layout(unique_circuits):
    layout = html.Div(
        style={
            'backgroundColor': 'black',
            'color': 'white',
            'padding': '20px',
        },
        children=[
            # html.H1('F1 Pitstop Analyse', style={'textAlign': 'center'}),
            # Dropdown für Rennstrecke
            html.Label('Choose a circuit:', style={'fontSize': '20px'}),
            dcc.Dropdown(
                id='circuit-pitstops-dropdown',
                options=[
                    {'label': circuit, 'value': circuit}
                    for circuit in sorted(unique_circuits)
                ],
                value='German Grand Prix',
                clearable=False,
                style={'backgroundColor': 'white', 'color': 'black'},
            ),
            # Dropdown für Jahr (abhängig von Rennstrecke)
            html.Label(
                'Choose a year:',
                style={'fontSize': '20px', 'marginTop': '10px'},
            ),
            dcc.Dropdown(
                id='year-dropdown',
                clearable=False,
                style={'backgroundColor': 'white', 'color': 'black'},
            ),
            # Boxplot für Pitstop-Zeiten und Endplatzierung
            dcc.Graph(id='pitstop-boxplot', style={'marginTop': '20px'}),
            # Balkendiagramm für die Gesamt-Pitstop-Zeit pro Fahrer
            dcc.Graph(id='pitstop-barplot', style={'marginTop': '20px'}),
            # Info-Text zur Anzahl der Rennen und Zeitbereiche
            html.Div(
                id='race-info', style={'fontSize': '18px', 'marginTop': '20px'}
            ),
        ],
    )
    return layout


# Layout der App mit Dark Mode Styling
def create_pitstop_layout_boxplot(eligible_drivers):
    layout = html.Div(
        style={
            'backgroundColor': 'black',
            'color': 'white',
            'padding': '20px',
        },
        children=[
            # html.H1('F1 Pitstop Analyse', style={'textAlign': 'center'}),
            html.Label('Choose a driver:', style={'fontSize': '20px'}),
            dcc.Dropdown(
                id='driver-pitstop-dropdown',
                options=[
                    {'label': driver, 'value': driver}
                    for driver in eligible_drivers
                ],
                value='Max Verstappen',
                style={'backgroundColor': 'white', 'color': 'black'},
            ),
            dcc.Graph(id='boxplot', style={'backgroundColor': 'black'}),
            html.Div(
                id='race-boxplot-info',
                style={'fontSize': '18px', 'marginTop': '20px'},
            ),
        ],
    )
    return layout


def convert_duration_to_seconds(duration):
    if pd.isna(duration):
        return np.nan

    # Convert to string to handle all input types
    duration_str = str(duration)

    if ':' not in duration_str:
        try:
            return float(duration_str)
        except ValueError:
            return np.nan

    # MM:SS.sss format
    try:
        parts = duration_str.split(':')
        minutes = float(parts[0])
        seconds = float(parts[1])
        return minutes * 60 + seconds
    except (ValueError, IndexError):
        return np.nan

def create_circuit_plot(selected_circuit, selected_year, driver_pitstops_sorted):

    driver_pitstops_sorted['duration_category'] = pd.cut(
        driver_pitstops_sorted['duration'],
        bins=[driver_pitstops_sorted['duration'].min()]
        + driver_pitstops_sorted['duration']
        .quantile([0.33, 0.66, 1.0])
        .tolist(),
        labels=['Fast', 'Average', 'Slow'],
        include_lowest=True,
    )

    # **Boxplot für Pitstop-Kategorie vs. Endplatzierung**
    fig_box = px.box(
        driver_pitstops_sorted,
        x='duration_category',
        y='finish_position',
        color='duration_category',
        labels={
            'duration_category': 'Pitstop Speed',
            'finish_position': 'Finishing Position',
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
            [0, 'rgb(255, 0, 0)'],
            [0.2, 'rgb(255, 100, 100)'],
            [0.4, 'rgb(255, 150, 150)'],
            [0.6, 'rgb(255, 200, 200)'],
            [0.8, 'rgb(255, 255, 255)'],
            [1, 'rgb(255, 255, 255)'],
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
                f'Fast ({category_counts.get("Fast", 0)} Drivers): '
                f'{fast_range[0]:.2f}s - {fast_range[1]:.2f}s'
            ),
            html.P(
                f'Average ({category_counts.get("Average", 0)} Drivers): '
                f'{medium_range[0]:.2f}s - {medium_range[1]:.2f}s'
            ),
            html.P(
                f'Slow ({category_counts.get("Slow", 0)} Drivers): '
                f'{slow_range[0]:.2f}s - {slow_range[1]:.2f}s'
            ),
        ],
        className="info-text",
    )

    return fig_box, fig_bar, info_text

def create_driver_plot(driver_name, df_driver_sorted, total_races):
     # Pitstop-Dauer in 3 Kategorien aufteilen
    df_driver_sorted['duration_category'] = pd.cut(
        df_driver_sorted['duration'],
        bins=[df_driver_sorted['duration'].min()]
        + df_driver_sorted['duration'].quantile([0.33, 0.66, 1.0]).tolist(),
        labels=['Fast', 'Average', 'Slow'],
        include_lowest=True,
    )

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
                f'Fast ({category_counts.get("Fast", 0)} Races): '
                f'{fast_range[0]:.2f}s - {fast_range[1]:.2f}s'
            ),
            html.P(
                f'Average ({category_counts.get("Average", 0)} Races): '
                f'{medium_range[0]:.2f}s - {medium_range[1]:.2f}s'
            ),
            html.P(
                f'Slow ({category_counts.get("Slow", 0)} Races): '
                f'{slow_range[0]:.2f}s - {slow_range[1]:.2f}s'
            ),
        ],
        className="info-text",
    )

    return fig, info_text
