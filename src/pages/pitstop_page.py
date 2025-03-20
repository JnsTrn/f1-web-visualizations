import dash
from dash import html

dash.register_page(__name__, path="/page-3")

layout = html.Div([
    html.H1("Page 3", className="text-center text-light"),
    html.P("This is the content of Page 3.", className="text-light"),
    html.A("Back to Home", href="/", className="btn btn-danger")
], className="container bg-dark text-light")