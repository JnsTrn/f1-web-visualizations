from dash import dcc, html


def create_pitstop_layout(unique_circuits):
    layout = html.Div(
        style={
            'backgroundColor': 'black',
            'color': 'white',
            'padding': '20px',
        },
        children=[
            html.H1('F1 Pitstop Analyse', style={'textAlign': 'center'}),
            # Dropdown für Rennstrecke
            html.Label('Wähle eine Rennstrecke:', style={'fontSize': '20px'}),
            dcc.Dropdown(
                id='circuit-pitstops-dropdown',
                options=[
                    {'label': circuit, 'value': circuit}
                    for circuit in unique_circuits
                ],
                value=unique_circuits[0],  # Standardwert
                clearable=False,
                style={'backgroundColor': 'white', 'color': 'black'},
            ),
            # Dropdown für Jahr (abhängig von Rennstrecke)
            html.Label(
                'Wähle ein Jahr:',
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
            html.H1('F1 Pitstop Analyse', style={'textAlign': 'center'}),
            html.Label('Fahrer auswählen:', style={'fontSize': '20px'}),
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
