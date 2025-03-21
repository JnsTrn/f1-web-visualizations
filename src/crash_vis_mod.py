import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from plotly.subplots import make_subplots


def total_incidents_by_year(df):
    # Group by year and sum total retirements, crashes, and failures
    yearly_totals = (
        df.groupby('year')[
            ['Total_Retirements', 'Race Incident/Crash', 'Technical Failure']
        ]
        .sum()
        .reset_index()
    )

    # Rename columns for clarity in the legend
    column_mapping = {
        'Total_Retirements': 'Total Retirements',
        'Race Incident/Crash': 'Incidents/Crashes',
        'Technical Failure': 'Technical Failures',
    }
    yearly_totals = yearly_totals.rename(columns=column_mapping)

    fig = px.line(
        yearly_totals,
        x='year',
        y=list(column_mapping.values()),  # Use renamed columns
        title='Total Incidents by Year (1994 - 2024)',
        markers=True,
        labels={'value': 'Total Count', 'year': 'Year'},
        template='plotly_dark',
    )

    # Update traces for hover customization
    hover_templates = {
        'Total Retirements': '<b>Total Retirements:</b> %{y}<extra></extra>',
        'Incidents/Crashes': '<b>Incidents/Crashes:</b> %{y}<extra></extra>',
        'Technical Failures': '<b>Technical Failures:</b> %{y}<extra></extra>',
    }

    for trace in fig.data:
        trace_name = trace.name  # Get the trace name
        if trace_name in hover_templates:
            trace.hovertemplate = hover_templates[trace_name]

    # Update traces for better visibility
    fig.update_traces(line=dict(width=3), marker=dict(size=8))

    # Enable interactive legend
    fig.update_layout(
        yaxis=dict(rangemode='tozero'),
        legend=dict(
            title='Incident Type',
            itemclick='toggle',
            itemdoubleclick='toggleothers',
            font=dict(size=16),
            x=1,
            y=1,
        ),
    )

    return fig


def yearly_retirements_rate(df):
    # Sum up race incidents and technical failures per year
    yearly_breakdown = (
        df.groupby('year')[['Total_Retirements', 'Total']].sum().reset_index()
    )
    races_per_circuit = (
        df.groupby('year').size().reset_index(name='race_count')
    )
    yearly_breakdown = yearly_breakdown.merge(races_per_circuit, on='year')

    yearly_breakdown['yearly_retirements_per_car'] = (
        yearly_breakdown['Total_Retirements'] / yearly_breakdown['Total']
    ) * 100

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=yearly_breakdown['year'],
            y=yearly_breakdown['yearly_retirements_per_car'],
            mode='lines',
            fill='tonexty',
            line=dict(color='red'),
            hovertemplate='Retirement Rate: %{y:.2f}%<extra></extra>',
        )
    )

    fig.update_layout(
        title='Yearly Retirement Rate in Percent (1994 - 2024)',
        xaxis_title='Year',
        yaxis_title='Percentage of Retired Cars',
        template='plotly_dark',
    )

    return fig


def average_yearly_retirements(df):
    # Sum up race incidents and technical failures per year
    yearly_breakdown = (
        df.groupby('year')[['Total_Retirements', 'Total']].sum().reset_index()
    )
    races_per_circuit = (
        df.groupby('year').size().reset_index(name='race_count')
    )
    yearly_breakdown = yearly_breakdown.merge(races_per_circuit, on='year')

    yearly_breakdown['yearly_retirements_per_race'] = (
        yearly_breakdown['Total_Retirements'] / yearly_breakdown['race_count']
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=yearly_breakdown['year'],
            y=yearly_breakdown['yearly_retirements_per_race'],
            mode='lines',
            fill='tonexty',
            line=dict(color='blue'),
            hovertemplate='Retirements per Race: %{y:.2f}<extra></extra>',
        )
    )

    fig.update_layout(
        title='Yearly Average Retirements per Race (1994 - 2024)',
        xaxis_title='Year',
        yaxis_title='Retirements',
        template='plotly_dark',
    )

    return fig


def calculate_incidents(df, min_race_count):
    races_per_circuit = (
        df.groupby('circuit_id').size().reset_index(name='race_count')
    )
    track_incidents = (
        df.groupby('circuit_id')[
            [
                'Race Incident/Crash',
                'Technical Failure',
                'Total_Retirements',
                'Total',
            ]
        ]
        .sum()
        .reset_index()
    )
    track_incidents = track_incidents.merge(races_per_circuit, on='circuit_id')

    # Calculate incidents per race for each type
    track_incidents['crashes_per_race'] = (
        track_incidents['Race Incident/Crash'] / track_incidents['race_count']
    )
    track_incidents['failures_per_race'] = (
        track_incidents['Technical Failure'] / track_incidents['race_count']
    )
    track_incidents['retirements_per_race'] = (
        track_incidents['Total_Retirements'] / track_incidents['race_count']
    )

    # Calculate incident rate per total amount of cars that have driven on each
    # circuit for each type. It represents the maximum posibble amount of
    # retirements that could have happened on this track. Displayed as percent
    track_incidents['crashes_per_race_driver'] = (
        track_incidents['Race Incident/Crash'] / track_incidents['Total']
    ) * 100
    track_incidents['failures_per_race_driver'] = (
        track_incidents['Technical Failure'] / track_incidents['Total']
    ) * 100
    track_incidents['retirements_per_race_driver'] = (
        track_incidents['Total_Retirements'] / track_incidents['Total']
    ) * 100

    # Filter circuits with at least X races
    track_incidents = track_incidents[
        track_incidents['race_count'] >= min_race_count
    ]

    return track_incidents


def create_incidents_figure(df, start_year, end_year, min_race_count, type):
    # Filter the dataframe for the selected year range
    df_filtered = df[(df['year'] >= start_year) & (df['year'] <= end_year)]

    # Calculate incidents for the filtered dataframe
    track_incidents = calculate_incidents(df_filtered, min_race_count)

    # Return an empty figure if no data matches criteria
    if track_incidents.empty:
        fig = go.Figure()
        fig.update_layout(
            height=1000,
            annotations=[
                dict(
                    text='No circuits with enough races in selected period',
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=20),
                )
            ],
        )
        return fig

    # Set subplot titles based on the selected type
    if type == 'per_race':
        subplot_titles = [
            'Average Amount of Crashes per Race',
            'Average Amount of Technical Failures per Race',
            'Average Amount of Total Retirements per Race',
        ]
    else:  # per_race_driver
        subplot_titles = [
            'Average Rate of Crashes in Percent',
            'Average Rate of Technical Failures in Percent',
            'Average Rate of Total Retirements in Percent',
        ]

    fig = make_subplots(rows=1, cols=3, subplot_titles=subplot_titles)

    if type == 'per_race':
        # Sort by highest crash incidents per race
        track_incidents_sorted = track_incidents.sort_values(
            by='crashes_per_race', ascending=True
        )

        fig.add_trace(
            go.Bar(
                x=track_incidents_sorted['crashes_per_race'],
                y=track_incidents_sorted['circuit_id'],
                orientation='h',
                marker=dict(
                    color=track_incidents_sorted['crashes_per_race'],
                    colorscale='Reds',
                ),
                name='Crashes',
                hovertext=track_incidents_sorted.apply(
                    lambda row: (
                        f'Races: {row["race_count"]}<br>'
                        f'Crashes per Race: {row["crashes_per_race"]:.2f}'
                    ),
                    axis=1,
                ),
                hoverinfo='text',
            ),
            row=1,
            col=1,
        )

        # Sort by highest failures per race
        track_incidents_sorted = track_incidents.sort_values(
            by='failures_per_race', ascending=True
        )

        fig.add_trace(
            go.Bar(
                x=track_incidents_sorted['failures_per_race'],
                y=track_incidents_sorted['circuit_id'],
                orientation='h',
                marker=dict(
                    color=track_incidents_sorted['failures_per_race'],
                    colorscale='Blues',
                ),
                name='Failures',
                hovertext=track_incidents_sorted.apply(
                    lambda row: (
                        f'Races: {row["race_count"]}<br>'
                        f'Technical Failures per Race: '
                        f'{row["failures_per_race"]:.2f}'
                    ),
                    axis=1,
                ),
                hoverinfo='text',
            ),
            row=1,
            col=2,
        )

        # Sort by highest retirements per race
        track_incidents_sorted = track_incidents.sort_values(
            by='retirements_per_race', ascending=True
        )

        fig.add_trace(
            go.Bar(
                x=track_incidents_sorted['retirements_per_race'],
                y=track_incidents_sorted['circuit_id'],
                orientation='h',
                marker=dict(
                    color=track_incidents_sorted['retirements_per_race'],
                    colorscale='Greens',
                ),
                name='Retirements',
                hovertext=track_incidents_sorted.apply(
                    lambda row: (
                        f'Races: {row["race_count"]}<br>'
                        f'Total Retirements per Race: '
                        f'{row["retirements_per_race"]:.2f}'
                    ),
                    axis=1,
                ),
                hoverinfo='text',
            ),
            row=1,
            col=3,
        )

    # per_race_driver
    else:
        # Sort by highest crash incidents per total drivers
        track_incidents_sorted = track_incidents.sort_values(
            by='crashes_per_race_driver', ascending=True
        )

        fig.add_trace(
            go.Bar(
                x=track_incidents_sorted['crashes_per_race_driver'],
                y=track_incidents_sorted['circuit_id'],
                orientation='h',
                marker=dict(
                    color=track_incidents_sorted['crashes_per_race_driver'],
                    colorscale='Reds',
                ),
                name='Crashes',
                hovertext=track_incidents_sorted.apply(
                    lambda row: (
                        f'Races: {row["race_count"]}<br>'
                        f'Crash Rate: {row["crashes_per_race_driver"]:.2f}%'
                    ),
                    axis=1,
                ),
                hoverinfo='text',
            ),
            row=1,
            col=1,
        )

        # Sort by highest failures per total drivers
        track_incidents_sorted = track_incidents.sort_values(
            by='failures_per_race_driver', ascending=True
        )

        fig.add_trace(
            go.Bar(
                x=track_incidents_sorted['failures_per_race_driver'],
                y=track_incidents_sorted['circuit_id'],
                orientation='h',
                marker=dict(
                    color=track_incidents_sorted['failures_per_race_driver'],
                    colorscale='Blues',
                ),
                name='Failures',
                hovertext=track_incidents_sorted.apply(
                    lambda row: (
                        f'Races: {row["race_count"]}<br>'
                        f'Technical Failure Rate: '
                        f'{row["failures_per_race_driver"]:.2f}%'
                    ),
                    axis=1,
                ),
                hoverinfo='text',
            ),
            row=1,
            col=2,
        )

        # Sort by highest retirements per total drivers
        track_incidents_sorted = track_incidents.sort_values(
            by='retirements_per_race_driver', ascending=True
        )

        fig.add_trace(
            go.Bar(
                x=track_incidents_sorted['retirements_per_race_driver'],
                y=track_incidents_sorted['circuit_id'],
                orientation='h',
                marker=dict(
                    color=track_incidents_sorted[
                        'retirements_per_race_driver'
                    ],
                    colorscale='Greens',
                ),
                name='Retirements',
                hovertext=track_incidents_sorted.apply(
                    lambda row: (
                        f'Races: {row["race_count"]}<br>'
                        f'Total Retirements Rate: '
                        f'{row["retirements_per_race_driver"]:.2f}%'
                    ),
                    axis=1,
                ),
                hoverinfo='text',
            ),
            row=1,
            col=3,
        )

    fig.update_layout(
        height=1000,
        autosize=True,
        # Put the x-axis scale on top
        xaxis=dict(side='top'),
        xaxis2=dict(side='top'),
        xaxis3=dict(side='top'),
        margin=dict(t=100, b=20, l=50, r=30),
        title_text=f'Incidents by Circuit ({start_year} - {end_year})\n'
        f'(Minimum {min_race_count} races)',
        template='plotly_dark',
        showlegend=False,
        annotations=[
            # Adjust the positions of the subplot titles
            dict(
                x=0.135,
                y=1.02,
                text=subplot_titles[0],
                showarrow=False,
                font=dict(size=15),
                xref='paper',
                yref='paper',
            ),
            dict(
                x=0.49,
                y=1.02,
                text=subplot_titles[1],
                showarrow=False,
                font=dict(size=15),
                xref='paper',
                yref='paper',
            ),
            dict(
                x=0.85,
                y=1.02,
                text=subplot_titles[2],
                showarrow=False,
                font=dict(size=15),
                xref='paper',
                yref='paper',
            ),
        ],
    )

    return fig


def create_interactive_incidents_dashboard(df):
    all_years = sorted(df['year'].unique())
    min_year, max_year = all_years[0], all_years[-1]

    # Layout definition (No Dash instance created)
    layout = html.Div(
        [
            html.H3(
                'Interactive Incidents by Circuit Dashboard',
                className='text-center',
            ),
            dcc.Graph(
                id='incidents-graph',
                style={
                    'width': '100%',
                },
                config={'responsive': True},
            ),
            html.Div(
                [
                    html.Label(
                        'Years:',
                        style={
                            'font-size': '14px',
                            'color': '#ff5733',
                            'font-weight': 'bold',
                        },
                    ),
                    dcc.RangeSlider(
                        id='year-slider',
                        min=min_year,
                        max=max_year,
                        value=[min_year, max_year],
                        marks={
                            str(year): {
                                'label': str(year),
                                'style': {'color': '#d1d1d1'},
                            }
                            for year in all_years
                        },
                        step=1,
                    ),
                ],
                style={'width': '85%', 'margin': 'auto'},
            ),
            html.Div(
                [
                    html.Label(
                        'Minimum Number of Races:',
                        style={
                            'font-size': '14px',
                            'color': '#ff5733',
                            'font-weight': 'bold',
                        },
                    ),
                    dcc.Slider(
                        id='race-slider',
                        min=1,
                        max=30,
                        value=10,
                        marks={
                            i: {'label': str(i), 'style': {'color': '#d1d1d1'}}
                            for i in range(1, 31)
                        },
                        step=1,
                    ),
                ],
                style={'width': '85%', 'margin': 'auto'},
            ),
            html.Div(
                [
                    html.Label(
                        'Analysis Type:',
                        style={
                            'font-size': '14px',
                            'color': '#ff5733',
                            'font-weight': 'bold',
                        },
                    ),
                    dcc.Slider(
                        id='type-slider',
                        min=0,
                        max=1,
                        value=0,
                        marks={
                            0: {
                                'label': 'Per Race Basis',
                                'style': {
                                    'color': '#ff9e80',
                                    'font-size': '14px',
                                    'font-weight': 'bold',
                                },
                            },
                            1: {
                                'label': 'Percentage Basis',
                                'style': {
                                    'color': '#ff9e80',
                                    'font-size': '14px',
                                    'font-weight': 'bold',
                                },
                            },
                        },
                        step=1,
                    ),
                ],
                style={'width': '85%', 'margin': 'auto'},
            ),
        ]
    )

    return layout
