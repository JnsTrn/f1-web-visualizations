import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div([
    html.H1("Page 3", className="text-center text-light"),
    html.P("This is the content of Page 3.", className="text-light"),
    html.A("Back to Home", href="/", className="btn btn-danger")
], className="container bg-dark text-light")

    # html.H2(
    #     "Welcome to DSP 2025! These are our research questions:",
    #     className="text-center text-light"
    # ),
    # html.Br(),
    # dbc.Row([
    #     dbc.Col([
    #         dcc.Graph(figure=fig_CraWeath)
    #     ])
    # ]),
    # dbc.Row([
    #     dbc.Col(dbc.Button("Page 1", href="/page-1", color="primary", size="lg", className="w-100"), width=4),
    #     dbc.Col(dbc.Button("Page 2", href="/page-2", color="success", size="lg", className="w-100"), width=4),
    #     dbc.Col(dbc.Button("Page 3", href="/page-3", color="danger", size="lg", className="w-100"), width=4),
    # ], className="text-center"),
    # html.Br(),