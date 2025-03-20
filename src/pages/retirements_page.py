import dash
from dash import html

dash.register_page(__name__, path="/retirements")

layout = html.Div([
    html.H1("Page 2", className="text-center text-light"),
    html.P("This is the content of Page 2.", className="text-light"),
    html.A("Back to Home", href="/", className="btn btn-success")
], className="container bg-dark text-light")