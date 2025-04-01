import plotly.graph_objects as go
import pandas as pd

from dash import dcc, html

import modules.driver_standings_mod as ds


# Modified by ChatGPT
def create_figure_all_time_standings(df):
    """
    Takes a dataframe

    Creates a heatmap for all time driver standings

    Returns the the heatmap as a plotly figure object
    """
    number = 22

    df_heatmap = ds.get_all_standings(df, (number + 1))
    df_heatmap = df_heatmap[df_heatmap['finish_position'] <= number]
    heatmap_data = df_heatmap.pivot(
        index='finish_position', columns='grid_position', values='count'
    )

    # Convert zeros to a custom hover text
    hover_data = heatmap_data.values.copy().astype(object)
    hover_data[hover_data == 0] = 'N/A'

    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Reds_r',
            text=heatmap_data.values,
            hovertext=hover_data,
            hovertemplate='Start: %{x}<br>Finish: %{y}<br>'
            'Count: %{hovertext}<extra></extra>',
        )
    )

    fig.update_layout(
        template='plotly_dark',
        title='Relation between Starting and Finishing Position 1994 - 2004',
        height=600,
        xaxis=dict(
            tickmode='array',
            tickvals=df_heatmap['grid_position'].unique(),
            showgrid=False,
            title='Starting position',
            linecolor='white',
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=df_heatmap['finish_position'].unique(),
            showgrid=False,
            title='Finishing position',
            linecolor='white',
        ),
    )
    return fig


# Modified by ChatGPT
def create_fig_start_avg_placements(df, df_race_completed):
    """
    Takes the completed dataframe and the dataframe where only the
    completed races are in

    Creates a scatterplot for the avg placement for each starting position
    and considered all races and race that were driven from start to finish

    Returns the scatterplot as a plotly figure object
    """
    # Calculation of mean for races that were completed
    standings = ds.get_all_standings(df_race_completed, 23)
    standings['Produkt'] = standings.prod(axis=1)

    df_final = pd.DataFrame({'grid_position': [], 'avg_placement': []})

    for pos in range(1, 28):
        temp = standings[standings['grid_position'] == pos]
        sum_pro = temp['Produkt'].sum() / pos
        sum_count = temp['count'].sum()
        if sum_count != 0:
            mittelwert = sum_pro / sum_count
            df_final.loc[len(df_final)] = [pos, mittelwert]

    # Calculation of mean for all races
    df_all_races = ds.get_all_standings(df, 23)
    df_all_races['Produkt'] = df_all_races.prod(axis=1)
    df_final_all = pd.DataFrame({'grid_position': [], 'avg_placement': []})

    for pos in range(1, 28):
        temp = df_all_races[df_all_races['grid_position'] == pos]
        sum_pro = temp['Produkt'].sum() / pos
        sum_count = temp['count'].sum()
        if sum_count != 0:
            mittelwert = sum_pro / sum_count
            df_final_all.loc[len(df_final_all)] = [pos, mittelwert]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_final['grid_position'],
            y=df_final['avg_placement'],
            mode='lines+markers',
            name='Race completed',
            marker=dict(color='blue'),
            hovertemplate='Average placement: %{y:.2f}<extra></extra>',
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_final_all['grid_position'],
            y=df_final_all['avg_placement'],
            mode='lines+markers',
            name='All races ',
            marker=dict(color='red'),
            hovertemplate='Average placement: %{y:.2f}<extra></extra>',
        )
    )

    fig.update_layout(
        template='plotly_dark',
        title='Average placement depending on starting position',
        xaxis=dict(
            tick0=0,
            dtick=1,
            range=[0, 22.5],
            showgrid=False,
            linecolor='white',
            zeroline=False,
            title='Starting position',
        ),
        yaxis=dict(
            tick0=0,
            dtick=2,
            range=[0, 23],
            showgrid=False,
            linecolor='white',
            title='Average placement',
            zeroline=False,
        ),
    )

    return fig


# Modified by ChatGPT
def get_circuit_options(number, df):
    """
    Takes a dataframe and number which was choosen in the slider

    Filters all circuits that have been driven with choosen amount
    of races

    Returns the list of circuits which was droven at least
    choosen amount of times
    """
    circuit_list = ds.circuit_list(number=number, df=df)
    circuit_list = sorted(circuit_list)
    return [
        {'label': circuit.capitalize(), 'value': circuit}
        for circuit in circuit_list
    ]


# Modified by ChatGPT
def create_circuit_heatmap(slider_value, selected_circuit, df):
    """
    Takes a dataframe, the list of circuits created in
    'get_circuit_options' and the circuit name from the slider

    Creates a heatmap from the circuit with each starting and
    finish position

    Returns the the heatmap as a plotly figure object
    """
    number = slider_value * 20

    circuit_options = get_circuit_options(number, df)

    if selected_circuit is None or selected_circuit not in [
        option['value'] for option in circuit_options
    ]:
        selected_circuit = 'nurburgring'

    circuit = df[df['circuit_id'] == selected_circuit]

    a = ds.get_all_standings(circuit, 23)
    a = a[a['finish_position'] <= 22]

    heatmap_data = a.pivot(
        index='finish_position', columns='grid_position', values='count'
    )

    # Convert zeros to a custom hover text
    hover_data = heatmap_data.values.copy().astype(object)
    hover_data[hover_data == 0] = 'N/A'

    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Reds_r',
            text=heatmap_data.values,
            hovertext=hover_data,
            hovertemplate='Start: %{x}<br>Finish: %{y}<br>Count: %{hovertext}'
            '<extra></extra>',
        )
    )

    fig.update_layout(
        template='plotly_dark',
        title=f'Relation between Starting and Finishing Position '
        f'for {selected_circuit.capitalize()}',
        height=600,
        xaxis=dict(
            tickmode='array',
            tickvals=a['grid_position'].unique(),
            showgrid=False,
            title='Starting Position',
            linecolor='white',
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=a['finish_position'].unique(),
            showgrid=False,
            title='Finishing Position',
            linecolor='white',
        ),
    )

    return circuit_options, selected_circuit, fig


# Modified by ChatGPT
def create_circuit_heatmap_layout():
    """
    Creates the interactive layout for the circuit heatmap

    Returns HTML layout for slider and dropdown menu
    """
    layout = (
        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            'Circuits that have been driven on at least '
                            'this many times'
                        ),
                        dcc.Slider(
                            id='number-slider',
                            min=1,
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
                            value='Silverstone',
                            style={
                                'width': '50%',
                                'margin': 'auto',
                                'color': 'black',
                            },
                        ),
                    ],
                    style={'textAlign': 'center', 'margin': '20px'},
                ),
                dcc.Graph(
                    id='heatmap',
                    style={
                        'width': '100%',
                    },
                    config={'responsive': True},
                ),
            ],
        ),
    )
    return layout


# Modified by ChatGPT
def driver_standings_mw(df):
    """
    Takes a dataframe

    Creates a bar chart for the avg placement of drivers
    during wet and mixed condition.

    Returns the bar chart as a plotly figure object
    """
    df_weather_filtered_mw = df[df['condition'].isin(['Mixed', 'Wet'])]

    liste_mw = ds.driver_list(20, df_weather_filtered_mw)

    df_avg_placements_start_mw = pd.DataFrame(
        {'driver_name': [], 'avg_placement': []}
    )

    for name in liste_mw:
        finish_mw = ds.driver_grid_pos(name, df_weather_filtered_mw)
        finish_mw['Produkt'] = finish_mw.prod(axis=1)
        if finish_mw['count_grid'].sum() != 0:
            mittelwert = (
                finish_mw['Produkt'].sum() / finish_mw['count_grid'].sum()
            )
            df_avg_placements_start_mw.loc[len(df_avg_placements_start_mw)] = [
                name,
                mittelwert,
            ]

    df_avg_placements_start_mw = df_avg_placements_start_mw.sort_values(
        by='avg_placement', ascending=True
    )

    df_avg_placements_finish_mw = pd.DataFrame(
        {'driver_name': [], 'avg_placement': []}
    )

    for name in liste_mw:
        finish_mw = ds.driver_finish_pos(name, df_weather_filtered_mw)
        finish_mw['Produkt'] = finish_mw.prod(axis=1)
        if finish_mw['count_finish'].sum() != 0:
            mittelwert = (
                finish_mw['Produkt'].sum() / finish_mw['count_finish'].sum()
            )
            df_avg_placements_finish_mw.loc[
                len(df_avg_placements_finish_mw)
            ] = [name, mittelwert]

    df_avg_placements_finish_mw = df_avg_placements_finish_mw.sort_values(
        by='avg_placement', ascending=True
    )

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_avg_placements_start_mw['driver_name'],
            y=df_avg_placements_start_mw['avg_placement'],
            name='start',
            hovertemplate='Average starting position: %{y:.2f}<extra></extra>',
        )
    )

    fig.add_trace(
        go.Bar(
            x=df_avg_placements_finish_mw['driver_name'],
            y=df_avg_placements_finish_mw['avg_placement'],
            name='finish',
            hovertemplate='Average finishing position: %{y:.2f}<extra></extra>',
        )
    )

    fig.update_layout(
        template='plotly_dark',
        height=450,
        autosize=True,
        xaxis_title='Driver',
        yaxis_title='Position',
        title='Average placements of drivers with at least 20 races driven in '
        'mixed/wet conditions since 2005',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )
    return fig


# Modified by ChatGPT
def driver_standings_dry(df):
    """
    Takes a dataframe

    Creates a bar chart for the avg placement of drivers
    during dry condition.

    Returns the bar chart as a plotly figure object
    """
    df_weather_filtered = df[df['condition'].isin(['Dry'])]
    df_same_list = df[df['condition'].isin(['Mixed', 'Wet'])]

    liste = ds.driver_list(20, df_same_list)

    df_avg_placements_start = pd.DataFrame(
        {'driver_name': [], 'avg_placement': []}
    )

    for name in liste:
        finish = ds.driver_grid_pos(name, df_weather_filtered)
        finish['Produkt'] = finish.prod(axis=1)
        if finish['count_grid'].sum() != 0:
            mittelwert = finish['Produkt'].sum() / finish['count_grid'].sum()
            df_avg_placements_start.loc[len(df_avg_placements_start)] = [
                name,
                mittelwert,
            ]

    df_avg_placements_start = df_avg_placements_start.sort_values(
        by='avg_placement', ascending=True
    )

    df_avg_placements_finish = pd.DataFrame(
        {'driver_name': [], 'avg_placement': []}
    )

    for name in liste:
        finish = ds.driver_finish_pos(name, df_weather_filtered)
        finish['Produkt'] = finish.prod(axis=1)
        if finish['count_finish'].sum() != 0:
            mittelwert = finish['Produkt'].sum() / finish['count_finish'].sum()
            df_avg_placements_finish.loc[len(df_avg_placements_finish)] = [
                name,
                mittelwert,
            ]

    df_avg_placements_finish = df_avg_placements_finish.sort_values(
        by='avg_placement', ascending=True
    )

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_avg_placements_start['driver_name'],
            y=df_avg_placements_start['avg_placement'],
            name='start',
            hovertemplate='Average starting position: %{y:.2f}<extra></extra>',
        )
    )

    fig.add_trace(
        go.Bar(
            x=df_avg_placements_finish['driver_name'],
            y=df_avg_placements_finish['avg_placement'],
            name='finish',
            hovertemplate='Average finishing position: %{y:.2f}<extra></extra>',
        )
    )

    fig.update_layout(
        template='plotly_dark',
        height=450,
        autosize=True,
        xaxis_title='Driver',
        yaxis_title='Position',
        title='Average placements of drivers with at least 20 races driven in '
        'dry conditions since 2005',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )
    return fig


# Modified by ChatGPT
def create_driver_conditions_layout():
    """
    Creates the interactive layout for the dry and mixed/wet conditions graph

    Returns HTML layout for dry and Wet/Mixed button
    """
    layout = html.Div(
        [
            html.Div(
                [
                    html.Button('Dry', id='dry-button', n_clicks=0),
                    html.Button('Wet/Mixed', id='wet-button', n_clicks=0),
                ],
                style={
                    'marginBottom': '20px',
                    'width': '100%',
                    'textAlign': 'center',
                },
            ),
            dcc.Store(id='last-clicked', data='dry-button'),
            dcc.Graph(
                id='graph',
                style={'width': '100%'},
                config={'responsive': True},
            ),
        ],
        style={'min-height': '505px'},
    )

    return layout


# Modified by ChatGPT
def create_grid_finish_figure(name, df):
    """
    Takes a dataframe

    Creates a bar chart of all the starting and finish position of
    the choosen driver.

    Returns the bar chart as a plotly figure object
    """
    grid_counts = ds.driver_grid_pos(name, df)
    grid_counts = grid_counts[grid_counts['grid_position'] != 0]
    grid_counts.columns = ['grid_position', 'count_grid']

    finish_counts = ds.driver_finish_pos(name, df)
    finish_counts.columns = ['grid_position', 'count_finish']

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=grid_counts['grid_position'],
            y=grid_counts['count_grid'],
            name='Start',
            hovertemplate='Number of starts from position %{x}: %{y}'
            '<extra></extra>',
        )
    )

    fig.add_trace(
        go.Bar(
            x=finish_counts['grid_position'],
            y=finish_counts['count_finish'],
            name='Finish',
            hovertemplate='Number of finishes in position %{x}: %{y}'
            '<extra></extra>',
        )
    )

    fig.update_layout(
        template='plotly_dark',
        height=450,
        autosize=True,
        xaxis_title='Position',
        yaxis_title='Count',
        title=f'Amount of Times {name} has started and ended the race in a '
        f'position from 1994 - 2024',
        title_font=dict(color='white'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )

    return fig


# Modified by ChatGPT
def create_grid_finish_figure_layout():
    """
    Creates the interactive layout for a specific drivers start
    and finish position

    Returns HTML layout for slider and dropdown menu
    """
    layout = (
        html.Div(
            [
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
                            value=130,
                            marks={i: str(i) for i in range(0, 401, 10)},
                            tooltip={
                                'placement': 'bottom',
                                'always_visible': True,
                            },
                        ),
                    ],
                    style={
                        'width': '100%',
                        'margin': '0 auto',
                        'textAlign': 'center',
                    },
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
                            style={
                                'width': '50%',
                                'margin': 'auto',
                                'color': 'black',
                            },
                        ),
                    ],
                    style={
                        'width': '80%',
                        'margin': '20px auto',
                        'textAlign': 'center',
                    },
                ),
                dcc.Graph(
                    id='grid-finish-positions',
                    style={
                        'width': '100%',
                    },
                    config={'responsive': True},
                ),
            ],
            style={'min-height': '620px'},
        ),
    )
    return layout


# Modified by ChatGPT
def create_avg_all_drivers_figure(amount_of_races, df, df_race_completed):
    """
    Takes the completed dataframe, the dataframe where only the
    completed races are in and a number with at least this amount of races
    driven

    Creates a scatterplot for the avg placement for each driver that has
    participated in 'amount_of_races' races

    Returns the scatterplot as a plotly figure object
    """
    liste = ds.driver_list(amount_of_races, df)
    df_driver = pd.DataFrame({'driver_name': [], 'avg_placement': []})

    for name in liste:
        finish = ds.driver_finish_pos(name, df)
        finish['Produkt'] = finish.prod(axis=1)
        if finish['count_finish'].sum() != 0:
            mittelwert = finish['Produkt'].sum() / finish['count_finish'].sum()
            df_driver.loc[len(df_driver)] = [name, mittelwert]

    df_driver = df_driver.sort_values(by='avg_placement', ascending=True)

    df_driver_completed = pd.DataFrame(
        {'driver_name': [], 'avg_placement': []}
    )

    for name in liste:
        finish = ds.driver_finish_pos(name, df_race_completed)
        finish['Produkt'] = finish.prod(axis=1)
        if finish['count_finish'].sum() != 0:
            mittelwert = finish['Produkt'].sum() / finish['count_finish'].sum()
            df_driver_completed.loc[len(df_driver_completed)] = [
                name,
                mittelwert,
            ]

    df_driver_completed = df_driver_completed.sort_values(
        by='avg_placement', ascending=True
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_driver_completed['driver_name'],
            y=df_driver_completed['avg_placement'],
            name='Races completed',
            mode='markers',
            hovertemplate='Average placement: %{y:.2f}<extra></extra>',
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_driver['driver_name'],
            y=df_driver['avg_placement'],
            name='All Races',
            mode='markers',
            hovertemplate='Average placement: %{y:.2f}<extra></extra>',
        )
    )

    fig.update_layout(
        template='plotly_dark',
        height=450,
        autosize=True,
        title=f'Average placement of drivers with at least {amount_of_races}'
        f' races',
        xaxis=dict(
            # showgrid=False,
            linecolor='white',
            title='Driver',
        ),
        yaxis=dict(
            tick0=0,
            dtick=2,
            range=[0, 20],
            showgrid=False,
            linecolor='white',
            title='Average Placement',
        ),
        margin=dict(t=50, b=50, l=50, r=50),
    )

    return fig


# Modified by ChatGPT
def create_avg_all_drivers_figure_layout():
    """
    Creates the interactive layout for the avg placement
    of all drivers that has driven with a choosen amount of races

    Returns HTML layout for slider for the amount races driven
    """
    layout = (
        html.Div(
            [
                dcc.Slider(
                    id='races-slider',
                    min=0,
                    max=400,
                    step=10,
                    value=130,
                    marks={i: str(i) for i in range(0, 401, 10)},
                ),
                dcc.Graph(
                    id='driver-placements',
                    style={
                        'width': '100%',
                    },
                    config={'responsive': True},
                ),
            ],
            style={'position': 'relative', 'min-height': '500px'},
        ),
    )
    return layout
