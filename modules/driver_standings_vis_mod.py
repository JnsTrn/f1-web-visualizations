import modules.driver_standings_mod as ds
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc, html


# Funktion, um das Diagramm basierend auf dem ausgewählten Fahrer zu erstellen
def create_grid_finish_figure(name, df):
    # Creates a bar chart for a specfic driver with his all time start/finish position
    grid_counts = ds.driver_grid_pos(name, df)
    grid_counts = grid_counts[grid_counts['grid_position'] != 0]  # Entfernen von Zeilen mit grid_pos == 0
    grid_counts.columns = ['grid_position', 'count_grid']

    finish_counts = ds.driver_finish_pos(name, df)
    finish_counts.columns = ['grid_position', 'count_finish']

    fig = go.Figure()
    fig.add_trace(go.Bar(x=grid_counts['grid_position'], y=grid_counts['count_grid'], name='grid', hovertemplate='Number from start position %{x}: %{y}<extra></extra>'))
    fig.add_trace(go.Bar(x=finish_counts['grid_position'], y=finish_counts['count_finish'], name='finish', hovertemplate='Number of finish positions %{x} %{y}<extra></extra>'))

    fig.update_layout(
        template='plotly_dark',
        #hoverlabel=dict(font=dict(color='white')),
        xaxis_title='Position', 
        yaxis_title='Count',  
        title=f'All time Start/Finish Position of {name}',
        title_font=dict(
        color='white'  
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    return fig


# Callback zum Abrufen der Liste von Strecken aus ds.circuit_list(number, df)
def get_circuit_options(number, df):
    circuit_list = ds.circuit_list(number=number, df=df)  # Beispielaufruf der Funktion mit number
    circuit_list = sorted(circuit_list)
    return [{'label': circuit.capitalize(), 'value': circuit} for circuit in circuit_list]


def update_dropdown_and_heatmap(slider_value, selected_circuit, df):
    # Multipliziere den Wert des Sliders mit 20
    number = slider_value * 20
    
    # Erhalte die Strecken-Liste basierend auf dem aktuellen Wert von "number"
    circuit_options = get_circuit_options(number, df)
    
    # Setze den Standardwert (erste Strecke aus der Liste) oder den ausgewählten Wert
    if selected_circuit is None or selected_circuit not in [option['value'] for option in circuit_options]:
        selected_circuit = circuit_options[0]['value'] if circuit_options else 'silverstone'
    
    # Filter für den gewählten Circuit
    circuit = df[df['circuit_id'] == selected_circuit]
    
    # Berechnung der Heatmap-Daten
    a = ds.get_all_standings(circuit,23)  # Verwende ds.get_all_standings, wenn verfügbar
    heatmap_data = a.pivot(index='finish_position', columns='grid_position', values='count')
    heatmap_data = heatmap_data.fillna(0)


    # Erstellen der Heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Reds_r',
        texttemplate='%{text}',
        hovertemplate='Start: %{x}<br>Finish: %{y}<br> count: %{z}<extra></extra>',
    ))

    # Layout der Heatmap
    fig.update_layout(
        template='plotly_dark',
        title=f'Start/finish position of circuit {selected_circuit.capitalize()}',
        height=600,
        xaxis=dict(
            tickmode='array',
            tickvals=a['grid_position'].unique(),
            showgrid=False,
            title='Start position',
            linecolor='white'
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=a['finish_position'].unique(),
            showgrid=False,
            title='Finish position',
            linecolor='white'
        )
    )
    
    return circuit_options, selected_circuit, fig



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
        name='Raced Completed', 
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
        title=f'Average placement of drivers with at Least {amount_of_races} races',
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


### Heatmap für alle driver 

def create_figure_all_time_standings(df):
    # Creates a heatmap of all time Start and finish position
    number = 22 

    df_heatmap = ds.get_all_standings(df, (number+1))
    df_heatmap = df_heatmap[df_heatmap['finish_position'] <= number]
    heatmap_data = df_heatmap.pivot(index='finish_position', columns='grid_position', values='count')
    heatmap_data = heatmap_data.fillna(0)

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,  
        y=heatmap_data.index,  
        colorscale='Reds_r',
        #text=heatmap_data.values,  # Werte in den Zellen anzeigen
        texttemplate='%{text}',  # Text direkt anzeigen
        #showscale=True  # Farbskala anzeigen (optional)
        hovertemplate='Start: %{x}<br>Finish: %{y}<br> count: %{z}<extra></extra>',
    ))
    fig.update_layout(
        template='plotly_dark',
        title= 'All time Start/finish Position',
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


### AVG Placement depending on Start Position

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

    fig.add_trace(go.Scatter(x=df_final['grid_position'], y=df_final['avg_placement'],  mode='lines+markers',name='race completed', marker=dict(color='blue'),
                            hovertemplate='Average placement: %{y:.2f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=df_final_all['grid_position'], y=df_final_all['avg_placement'], mode='lines+markers', name='all races ',  marker=dict(color='red'),
                            hovertemplate='Average placement: %{y:.2f}<extra></extra>'))
    
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
            title= 'Average placement',
            zeroline=False,
            
        ),     
    )

    return fig
