import dash
import pandas as pd
import plotly.express as px

from dash import Input, Output, html

import dash_bootstrap_components as dbc

import modules.pitstop_mod as ptm


####### Initialize the Dash app #######


dash.register_page(__name__, path='/pitstops', title='Pitstop Analysis')


############## Load Data ##############

DATA_PATH = 'data/'

df = pd.read_csv(
    DATA_PATH + 'merged_pitstops.csv',
)


# Create Dataframe for circuit Plot

df_unique = df
df_unique['duration'] = df_unique['duration'].apply(
    ptm.convert_duration_to_seconds
)
df_unique = df_unique.dropna(subset=['duration'])

unique_circuits = df_unique['race_name'].unique()


# Create Dataframe for driver Plot

df_filtered = df[['year', 'driver_name', 'duration', 'finish_position']].copy()
df_filtered['duration'] = df_filtered['duration'].apply(
    ptm.convert_duration_to_seconds
)
df_filtered = df_filtered.dropna(subset=['duration'])

# Fahrer filtern, die mindestens 2 Jahre gefahren sind
driver_years = df_filtered.groupby('driver_name')['year'].nunique()
eligible_drivers = driver_years[driver_years >= 2].index


############## Create Graphs ##############


pitstops_layout = ptm.create_pitstop_layout(unique_circuits)
pitstops_boxplot = ptm.create_pitstop_layout_boxplot(eligible_drivers)


############ Set up the layout ############

text1 = """
The graph provides an overview of all races across all tracks and all seasons for a selected driver.

To analyze the impact of pitstop duration on the driver's finishing position, the pitstop duration is divided into three categories: Fast, Average, and Slow.

The final race positions within these three categories are then evaluated using box plots. These box plots illustrate the distribution of finishing positions, highlighting key statistical metrics such as the median, quartiles, and potential outliers.

This visualization helps identify how the driver’s race results vary depending on their pitstop times.
"""

text2 = """
The graph provides an overview of all drivers, their pitstop time and their finishing position for a selected Grand Prix and year. To analayze the impact of pitstop duration on the driver's finishing position, the pitstop duration is divided into three categories: Fast, Average, and Slow.
These are then evaluated using a box plot. This visualization helps identify how different pit stop times affect the driver's finishing position. 
    """

explanation_text1 = """
When analyzing all races for a selected driver, no clear correlation is found between pit stop duration and final race position. This is primarily due to variations in entry and exit times for pit stops across different races. These variations are often influenced by external race conditions rather than the performance of the driver’s pit crew, as all competitors are subject to the same factors.
"""

explanation_text2 = """
The following analysis provides a detailed examination of individual races, evaluating the relationship between pit stop times and drivers' final positions.

In some races, such as the Abu Dhabi Grand Prix 2024, a correlation between pit stop duration and finishing position was observed, while in others, like the German Grand Prix 2011, no clear pattern emerged. These findings suggest that pit stop times have a limited impact on final race results, as numerous other factors play a more decisive role in determining a driver's finishing position.
"""

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
                        'How does the number and the average duration of '
                        'pitstops for a driver in a race relate to his '
                        'finishing position? ',
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
                            text1,
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
                    pitstops_boxplot,
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
                            text2,
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
                    [
                        html.P(
                            explanation_text1,
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
                    pitstops_layout,
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
                            explanation_text2,
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


########### Initialize Callbacks ############

# Callback for the Year Dropdown
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


# Callback for the circuit pitstop Plot
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

    filtered_df = df_unique[
        (df_unique['race_name'] == selected_circuit)
        & (df_unique['year'] == selected_year)
    ]

    filtered_df = filtered_df[(filtered_df['race_completed'] == True)]

    # Sum Total Pitstop Time per Driver and add finishing Position
    driver_pitstops = (
        filtered_df.groupby(['driver_name', 'finish_position'])['duration']
        .sum()
        .reset_index()
    )

    # Sorted into 3 Categories by Total Pitstop Time
    driver_pitstops_sorted = driver_pitstops.sort_values(
        'duration', ascending=True
    )

    return ptm.create_circuit_plot(
        selected_circuit, selected_year, driver_pitstops_sorted)


# Callback for the driver pitstop plot
@dash.callback(
    [Output('boxplot', 'figure'), Output('race-boxplot-info', 'children')],
    [Input('driver-pitstop-dropdown', 'value')],
)

def update_plot(driver_name):
    df_driver = df_filtered[df_filtered['driver_name'] == driver_name].copy()
    total_races = len(df_driver)

    # Sort by pitstop time
    df_driver_sorted = df_driver.sort_values('duration')

    return ptm.create_driver_plot(driver_name, df_driver_sorted, total_races)
