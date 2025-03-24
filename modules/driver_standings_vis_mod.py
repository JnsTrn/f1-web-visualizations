import plotly.graph_objects as go
import pandas as pd

from dash import dcc, html

import modules.driver_standings_mod as ds


def create_figure_all_time_standings(df):
    # Creates a heatmap of all time Start and finish position
    number = 22

    df_heatmap = ds.get_all_standings(df, (number+1))
    df_heatmap = df_heatmap[df_heatmap['finish_position'] <= number]
    heatmap_data = df_heatmap.pivot(index='finish_position', columns='grid_position', values='count')

    # Convert zeros to a custom hover text
    hover_data = heatmap_data.values.copy().astype(object)
    hover_data[hover_data == 0] = 'N/A'

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Reds_r',
        text=heatmap_data.values,
        hovertext=hover_data,
        hovertemplate='Start: %{x}<br>Finish: %{y}<br>Count: %{hovertext}<extra></extra>',
    ))

    fig.update_layout(
        template='plotly_dark',
        title= 'Relation between Starting and Finishing Position 1994 - 2004',
        height=600,
        xaxis=dict(
            tickmode='array',
            tickvals=df_heatmap['grid_position'].unique(),
            showgrid=False,
            title= 'Start position',
            linecolor= 'white'
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=df_heatmap['finish_position'].unique(),
            showgrid=False,
            title= 'Finish position',
            linecolor='white'
        )
    )
    return fig


def create_fig_start_avg_placements(df, df_race_completed):
    # Calculation of mean for races that were completed
    standings = ds.get_all_standings(df_race_completed,23)
    standings['Produkt'] = standings.prod(axis=1)

    df_final = pd.DataFrame({'grid_position' : [], 'avg_placement' : []})

    for pos in range(1,28):
        temp = standings[standings['grid_position']== pos]
        sum_pro = temp['Produkt'].sum()/pos
        sum_count = temp['count'].sum()
        if sum_count != 0 :
            mittelwert = sum_pro / sum_count
            df_final.loc[len(df_final)] = [pos, mittelwert]

    # Calculation of mean for all races
    df_all_races = ds.get_all_standings(df,23)
    df_all_races['Produkt'] = df_all_races.prod(axis=1)
    df_final_all = pd.DataFrame({'grid_position' : [], 'avg_placement' : []})

    for pos in range(1,28):
        temp = df_all_races[df_all_races['grid_position']== pos]
        sum_pro = temp['Produkt'].sum()/pos
        sum_count = temp['count'].sum()
        if sum_count != 0 :
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
            hovertemplate='Average placement: %{y:.2f}<extra></extra>'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_final_all['grid_position'],
            y=df_final_all['avg_placement'],
            mode='lines+markers',
            name='All races ',
            marker=dict(color='red'),
            hovertemplate='Average placement: %{y:.2f}<extra></extra>'
        )
    )

    fig.update_layout(
        template='plotly_dark',
        title= 'Average placement depending on starting position',
        xaxis=dict(
            tick0=0,
            dtick=2,
            range=[0, 23],
            showgrid=False,
            linecolor= 'white',
            zeroline= False,
            title= 'Start position'
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


def get_circuit_options(number, df):
    circuit_list = ds.circuit_list(number=number, df=df)
    circuit_list = sorted(circuit_list)
    return [{'label': circuit.capitalize(), 'value': circuit} for circuit in circuit_list]


def create_circuit_heatmap(slider_value, selected_circuit, df):
    number = slider_value * 20

    circuit_options = get_circuit_options(number, df)

    if selected_circuit is None or selected_circuit not in [option['value'] for option in circuit_options]:
        selected_circuit = circuit_options[15]['value'] if circuit_options else 'Silverstone'

    circuit = df[df['circuit_id'] == selected_circuit]

    a = ds.get_all_standings(circuit,23)
    a = a[a['finish_position'] <= 22]

    heatmap_data = a.pivot(
        index='finish_position',
        columns='grid_position',
        values='count'
    )

    # Convert zeros to a custom hover text
    hover_data = heatmap_data.values.copy().astype(object)
    hover_data[hover_data == 0] = 'N/A'

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Reds_r',
        text=heatmap_data.values,
        hovertext=hover_data,
        hovertemplate='Start: %{x}<br>Finish: %{y}<br>Count: %{hovertext}<extra></extra>',
    ))

    fig.update_layout(
        template='plotly_dark',
        title=f'Relation between Starting and Finishing Position for {selected_circuit.capitalize()}',
        height=600,
        xaxis=dict(
            tickmode='array',
            tickvals=a['grid_position'].unique(),
            showgrid=False,
            title='Starting Position',
            linecolor='white'
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=a['finish_position'].unique(),
            showgrid=False,
            title='Finishing Position',
            linecolor='white'
        )
    )

    return circuit_options, selected_circuit, fig


def create_circuit_heatmap_layout():
    layout = html.Div(
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
                        style={'width': '50%',
                            'margin': 'auto',
                            'color': 'black'
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
    return layout


def driver_standings_mw(df):
    df_weather_filtered_mw = df[df['condition'].isin(['Mixed', 'Wet'])]

    liste_mw = ds.driver_list(20, df_weather_filtered_mw)

    df_avg_placements_start_mw = pd.DataFrame({'driver_name' : [], 'avg_placement' : []})

    for name in liste_mw:
        finish_mw = ds.driver_grid_pos(name, df_weather_filtered_mw)
        finish_mw['Produkt'] = finish_mw.prod(axis=1)
        if finish_mw['count_grid'].sum() != 0 :
            mittelwert = finish_mw['Produkt'].sum() / finish_mw['count_grid'].sum()
            df_avg_placements_start_mw.loc[len(df_avg_placements_start_mw)] = [name, mittelwert]

    df_avg_placements_start_mw= df_avg_placements_start_mw.sort_values(by='avg_placement', ascending=True)

    df_avg_placements_finish_mw = pd.DataFrame({'driver_name' : [], 'avg_placement' : []})

    for name in liste_mw:
        finish_mw = ds.driver_finish_pos(name, df_weather_filtered_mw)
        finish_mw['Produkt'] = finish_mw.prod(axis=1)
        if finish_mw['count_finish'].sum() != 0 :
            mittelwert = finish_mw['Produkt'].sum() / finish_mw['count_finish'].sum()
            df_avg_placements_finish_mw.loc[len(df_avg_placements_finish_mw)] = [name, mittelwert]

    df_avg_placements_finish_mw= df_avg_placements_finish_mw.sort_values(by='avg_placement', ascending=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_avg_placements_start_mw['driver_name'],
            y=df_avg_placements_start_mw['avg_placement'],
            name='start',
            hovertemplate='Average starting position: %{y:.2f}<extra></extra>'
        )
    )

    fig.add_trace(
        go.Bar(
            x=df_avg_placements_finish_mw['driver_name'],
            y=df_avg_placements_finish_mw['avg_placement'],
            name='finish',
            hovertemplate='Average finishing position: %{y:.2f}<extra></extra>'
        )
    )

    fig.update_layout(
        template='plotly_dark',
        height=450,
        autosize=True,
        xaxis_title='Driver',
        yaxis_title='Position',
        title='Average placements of drivers in mixed/wet conditions since 2005 and atleast 20 races driven',
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            showgrid=False
        )
    )
    return fig


def driver_standings_dry(df):
    df_weather_filtered = df[df['condition'].isin(['Dry'])]
    df_same_list =df[df['condition'].isin(['Mixed', 'Wet'])]

    liste = ds.driver_list(20, df_same_list)

    df_avg_placements_start = pd.DataFrame({'driver_name' : [], 'avg_placement' : []})

    for name in liste:
        finish = ds.driver_grid_pos(name, df_weather_filtered)
        finish['Produkt'] = finish.prod(axis=1)
        if finish['count_grid'].sum() != 0 :
            mittelwert = finish['Produkt'].sum() / finish['count_grid'].sum()
            df_avg_placements_start.loc[len(df_avg_placements_start)] = [name, mittelwert]

    df_avg_placements_start= df_avg_placements_start.sort_values(by='avg_placement', ascending=True)

    df_avg_placements_finish = pd.DataFrame({'driver_name' : [], 'avg_placement' : []})

    for name in liste:
        finish = ds.driver_finish_pos(name, df_weather_filtered)
        finish['Produkt'] = finish.prod(axis=1)
        if finish['count_finish'].sum() != 0 :
            mittelwert = finish['Produkt'].sum() / finish['count_finish'].sum()
            df_avg_placements_finish.loc[len(df_avg_placements_finish)] = [name, mittelwert]

    df_avg_placements_finish= df_avg_placements_finish.sort_values(by='avg_placement', ascending=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_avg_placements_start['driver_name'],
            y=df_avg_placements_start['avg_placement'],
            name='start',
            hovertemplate='Average starting position: %{y:.2f}<extra></extra>'
        )
    )

    fig.add_trace(
        go.Bar(
            x=df_avg_placements_finish['driver_name'],
            y=df_avg_placements_finish['avg_placement'],
            name='finish',
            hovertemplate='Average finishing position: %{y:.2f}<extra></extra>'
        )
    )

    fig.update_layout(
        template='plotly_dark',
        height=450,
        autosize=True,
        xaxis_title='Driver',
        yaxis_title='Position',
        title='Average placements of drivers in dry conditions since 2005 and atleast 20 races driven',
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            showgrid=False
        )
    )
    return fig


def create_driver_conditions_layout():
    layout = html.Div([
        html.Div([
            html.Button('Dry', id='dry-button', n_clicks=0),
            html.Button('Wet', id='wet-button', n_clicks=0),
        ],
        style={
            'marginBottom': '20px',
            'width': '100%',
            'textAlign': 'center'
        }),

        dcc.Store(id='last-clicked', data='dry-button'),

        dcc.Graph(
            id='graph',
            style={
                'width': '100%'
            },
            config={'responsive': True}
        )
    ], style={
        'min-height': '505px'
    })

    return layout


def create_grid_finish_figure(name, df):
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
            hovertemplate='Number of starts from position %{x}: %{y}<extra></extra>'
        )
    )

    fig.add_trace(
        go.Bar(
            x=finish_counts['grid_position'],
            y=finish_counts['count_finish'],
            name='Finish',
            hovertemplate='Number of finishes in position %{x}: %{y}<extra></extra>'
        )
    )

    fig.update_layout(
        template='plotly_dark',
        height=450,
        autosize=True,
        xaxis_title='Position',
        yaxis_title='Count',
        title=f'Amount of Times {name} has started and ended the race in a position from 1994 - 2024',
        title_font=dict(
        color='white'
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    return fig


def create_grid_finish_figure_layout():
    layout = html.Div(
        [
            html.Div(
                children=[
                    html.Label(
                        'Choose mininum races driven',
                        style={'color': 'white'},
                    ),
                    dcc.Slider(
                        id='driver-count-slider',
                        min= 0,
                        max= 400,
                        step= 10,
                        value= 130,
                        marks={
                            i: str(i) for i in range(0, 401, 10)
                        },
                        tooltip={
                            'placement': 'bottom',
                            'always_visible': True
                        },
                    ),
                ],
                style={
                    'width': '100%',
                    'margin': '0 auto',
                    'textAlign': 'center'
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
                            'color': 'black'
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
        style={
            'min-height': '620px'
        }
    ),
    return layout


def create_avg_all_drivers_figure(amount_of_races, df, df_race_completed):
    # Creates a figure for the average placements of drivers
    liste = ds.driver_list(amount_of_races, df)
    df_driver = pd.DataFrame({'driver_name': [], 'avg_placement': []})

    for name in liste:
        finish = ds.driver_finish_pos(name, df)
        finish['Produkt'] = finish.prod(axis=1)
        if finish['count_finish'].sum() != 0:
            mittelwert = finish['Produkt'].sum() / finish['count_finish'].sum()
            df_driver.loc[len(df_driver)] = [name, mittelwert]

    df_driver = df_driver.sort_values(by='avg_placement', ascending=True)

    df_driver_completed = pd.DataFrame({'driver_name': [], 'avg_placement': []})

    for name in liste:
        finish = ds.driver_finish_pos(name, df_race_completed)
        finish['Produkt'] = finish.prod(axis=1)
        if finish['count_finish'].sum() != 0:
            mittelwert = finish['Produkt'].sum() / finish['count_finish'].sum()
            df_driver_completed.loc[len(df_driver_completed)] = [name, mittelwert]

    df_driver_completed = df_driver_completed.sort_values(by='avg_placement', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_driver_completed['driver_name'],
        y=df_driver_completed['avg_placement'],
        name='Races completed',
        mode='markers',
        hovertemplate='Average placement: %{y:.2f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df_driver['driver_name'],
        y=df_driver['avg_placement'],
        name='All Races',
        mode='markers',
        hovertemplate='Average placement: %{y:.2f}<extra></extra>'
    ))

    fig.update_layout(
        template='plotly_dark',
        height=450,
        autosize=True,
        title=f'Average placement of drivers with at least {amount_of_races} races',
        xaxis=dict(
            showgrid=False,
            linecolor='white',
            title='Driver'
        ),
        yaxis=dict(
            tick0=0,
            dtick=2,
            range=[0, 20],
            showgrid=False,
            linecolor='white',
            title='Avg Placement'
        ),
        margin=dict(t=50, b=50, l=50, r=50),
    )

    return fig


def create_avg_all_drivers_figure_layout():
    layout = html.Div(
        [
            dcc.Slider(
                id='races-slider',
                min=0,
                max=400,
                step=10,
                value=130,
                marks={
                i: str(i) for i in range(0, 401, 10)
                },
            ),
            dcc.Graph(
                id='driver-placements',
                style={
                    'width': '100%',
                },
                config={'responsive': True},
            ),
        ],
        style={
            'position': 'relative',
            'min-height': '500px'
        }
    ),
    return layout
