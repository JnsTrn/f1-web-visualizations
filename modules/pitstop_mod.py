import numpy as np
import pandas as pd
import plotly.express as px

from dash import dcc, html


def convert_duration_to_seconds(duration):
    """
    Converts a given duration into seconds.
    Supports MM:SS.sss format or numeric values.
    Returns NaN for invalid inputs.
    """
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


def create_pitstop_layout(unique_circuits):
    """
    Generates the layout for the pitstop data visualization based on the
    provided unique circuits. This function creates an HTML layout that
    allows the user to select a circuit and a year to visualize pitstop
    data. It displays two dropdown menus: one for selecting the circuit
    and one for selecting the year. Additionally, two plots
    (a box plot and a bar plot) for visualizing pitstop data,
    along with a text area for additional race information, are included.

    Args:
        unique_circuits (list of str): A list of unique circuits to be shown as
        options in the dropdown menu.

    Returns:
        layout (html.Div): A Dash layout containing the dropdown menus, plots,
        and information section.
    """
    layout = html.Div(
        style={
            'backgroundColor': 'black',
            'color': 'white',
            'padding': '20px',
        },
        children=[
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
            html.Label(
                'Choose a year:',
                style={'fontSize': '20px', 'marginTop': '10px'},
            ),
            dcc.Dropdown(
                id='year-dropdown',
                clearable=False,
                style={'backgroundColor': 'white', 'color': 'black'},
            ),
            dcc.Graph(id='pitstop-boxplot', style={'marginTop': '20px'}),
            dcc.Graph(id='pitstop-barplot', style={'marginTop': '20px'}),
            html.Div(
                id='race-info', style={'fontSize': '18px', 'marginTop': '20px'}
            ),
        ],
    )
    return layout


def create_pitstop_layout_boxplot(eligible_drivers):
    """
    Generates the layout for the pitstop boxplot visualization based on the 
    provided eligible drivers. This function creates an HTML layout that allows
    the user to select a driver from a dropdown list to visualize their pitstop
    data in a boxplot. It includes a dropdown menu for driver selection,
    a boxplot for pitstop data visualization, and a section for displaying
    additional race information.

    Args:
        eligible_drivers (list of str): A list of eligible drivers to be shown 
        as options in the dropdown menu.

    Returns:
        layout (html.Div): A Dash layout containing the driver dropdown menu, 
        boxplot, and information section.
    """
    layout = html.Div(
        style={
            'backgroundColor': 'black',
            'color': 'white',
            'padding': '20px',
        },
        children=[
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


def create_circuit_plot(
    selected_circuit, selected_year, driver_pitstops_sorted
):
    """
    Generates pitstop analysis plots (boxplot and bar plot) for a selected
    circuit and year. This function creates two visualizations based on
    pitstop data for a specific circuit and year:
    1. A boxplot comparing pit stop speed categories with finishing positions.
    2. A bar plot showing the total pit stop time for each driver, with
    finishing positions represented by a color scale.
    Additionally, it provides a summary of the number of drivers in each pit
    stop speed category and the min/max times for each category.

    Args:
        selected_circuit (str): The name of the selected racing circuit.
        selected_year (int): The year of the race.
        driver_pitstops_sorted (DataFrame): A sorted DataFrame containing the
        pitstop data of drivers.

    Returns:
        fig_box (plotly.graph_objs.Figure): A boxplot showing pit stop speed
        vs. finish position.
        fig_bar (plotly.graph_objs.Figure): A bar plot showing total pit stop
        times per driver.
        info_text (html.Div): A div containing information about the number of
        drivers and time ranges for each pit stop speed category.
    """
    # Categorize pit stop durations into Fast, Average, and Slow
    driver_pitstops_sorted['duration_category'] = pd.cut(
        driver_pitstops_sorted['duration'],
        bins=[driver_pitstops_sorted['duration'].min()]
        + driver_pitstops_sorted['duration']
        .quantile([0.33, 0.66, 1.0])
        .tolist(),
        labels=['Fast', 'Average', 'Slow'],
        include_lowest=True,
    )

    # Create a boxplot showing pit stop speed categories vs. finish positions
    fig_box = px.box(
        driver_pitstops_sorted,
        x='duration_category',
        y='finish_position',
        color='duration_category',
        labels={
            'duration_category': 'Pit Stop Speed',
            'finish_position': 'Finishing Position',
        },
        title=f'Pit Stop Analysis: {selected_circuit} ({selected_year})',
        template='plotly_dark',
    )

    # Create a bar plot for total pit stop time per driver with finish position
    # as a color scale
    fig_bar = px.bar(
        driver_pitstops_sorted,
        x='driver_name',
        y='duration',
        labels={
            'driver_name': 'Driver',
            'duration': 'Total Pit Stop Time (s)',
            'finish_position': 'Finish Position',
        },
        title=f'Total Pit Stop Time per Driver({selected_circuit}, '
        f'{selected_year})',
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

    # Calculate the number of drivers in each category (Fast, Average, Slow)
    category_counts = (
        driver_pitstops_sorted['duration_category'].value_counts().to_dict()
    )

    # Calculate min and max pit stop times for each category 
    # (Fast, Average, Slow)
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
        # If there's an issue with the data (e.g., no data in any category),
        # return empty plots and an info message
        return fig_box, fig_bar, html.P('No Data Available')

    # Create an info text summarizing the number of drivers and the time
    # ranges for each category
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
        className='info-text',
    )

    # Return the generated boxplot, bar plot, and the info text
    return fig_box, fig_bar, info_text


def create_driver_plot(driver_name, df_driver_sorted, total_races):
    """
    Generates a pit stop analysis boxplot for a specific driver, based on their
    pit stop duration and finish positions. This function creates a boxplot
    comparing the pit stop duration categories (Fast, Average, Slow) with the
    finishing positions of a specific driver. Additionally, it calculates the
    number of races in each category and provides the min/max durations
    for each category.

    Args:
        driver_name (str): The name of the driver for whom the pit stop
        nalysis is being created. df_driver_sorted (DataFrame):
        A DataFrame containing the pit stop data for the selected driver,
        sorted by pit stop duration. total_races (int): The total number 
        of races for the selected driver.

    Returns:
        fig (plotly.graph_objs.Figure): A boxplot showing pit stop duration
        categories vs. finishing positions for the driver. info_text
        (html.Div): A div containing information about the number of races
        in each category and the time ranges.
    """

    # Categorize pit stop durations into Fast, Average, and Slow categories
    df_driver_sorted['duration_category'] = pd.cut(
        df_driver_sorted['duration'],
        bins=[df_driver_sorted['duration'].min()]
        + df_driver_sorted['duration'].quantile([0.33, 0.66, 1.0]).tolist(),
        labels=['Fast', 'Average', 'Slow'],
        include_lowest=True,
    )

    # Create a boxplot comparing pit stop speed categories with
    # finish positions
    fig = px.box(
        df_driver_sorted,
        x='duration_category',
        y='finish_position',
        color='duration_category',
        labels={
            'duration_category': 'Pit Stop Speed',
            'finish_position': 'Finishing Position',
        },
        title=f'Pit Stop Analysis: {driver_name}',
        template='plotly_dark',
    )

    # Calculate the number of races in each pit stop category
    category_counts = (
        df_driver_sorted['duration_category'].value_counts().to_dict()
    )

    # Calculate the min and max pit stop durations for each category
    # (Slow, Average, Fast)
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

    # Create a summary text with information about the number of races per
    #  category and the time ranges
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
        className='info-text',
    )

    # Return the generated boxplot and the information text
    return fig, info_text
