import crash_vis_mod as cvm
import dash
import dash_bootstrap_components as dbc  # for dark theme
import pandas as pd
import plots as plt
from dash import dcc, html

####### Initialize the Dash app #######

# bootstrap increases the default size of the text in html.h1 and .h3
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

############## Load Data ##############


DATA_PATH = 'data/'

df = pd.read_csv(
    DATA_PATH + 'f1_1994_2024_categorized_by_race_status.csv',
    parse_dates=['date'],
)

df_CraWeath = pd.read_csv(DATA_PATH + 'crashes_and_weather.csv')


# ############ Define Graphs ############

plt.init_figs()
fig_CraWeath = plt.create_fig_CraWeath(df_CraWeath)
fig_total_incidents = cvm.total_incidents_by_year(df)
fig_retirements_rate = cvm.yearly_retirements_rate(df)
fig_retirements_race = cvm.average_yearly_retirements(df)
incidents_layout, register_incidents_callbacks = (
    cvm.create_interactive_incidents_dashboard(df)
)

########## Set up the layout ##########

app.layout = html.Div(
    [
        html.H1('Testing Server', style={'fontSize': '32px'}),
        html.Div(children='Hello from testing server.'),
        html.Div(
            [
                html.H3('Total Incidents by Year', style={'fontSize': '22px'}),
                dcc.Graph(figure=fig_total_incidents),
            ]
        ),
        html.Div(
            [
                html.H3('Retirement Rate by Year', style={'fontSize': '22px'}),
                dcc.Graph(figure=fig_retirements_rate),
            ]
        ),
        html.Div(
            [
                html.H3(
                    'Average Retirements per Race by Year',
                    style={'fontSize': '22px'},
                ),
                dcc.Graph(figure=fig_retirements_race),
            ]
        ),
        html.Div(
            [
                html.H3('Crash Rate by Weather', style={'fontSize': '22px'}),
                dcc.Graph(figure=fig_CraWeath),
            ]
        ),
        # Include the interactive incidents dashboard
        incidents_layout,
    ]
)

# Register the incidents callback functions
register_incidents_callbacks(app)


############# Run the app #############

if __name__ == '__main__':
    app.run(debug=True)
