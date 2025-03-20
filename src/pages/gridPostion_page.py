import dash
from dash import html

dash.register_page(__name__, path="/page-1")

layout = html.Div([
    html.H1("Page 1", className="text-center text-light"),
    html.P("This is the content of Page 1.", className="text-light"),
    html.A("Back to Home", href="/", className="btn btn-primary")
], className="container bg-dark text-light")