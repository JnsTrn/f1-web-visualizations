import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

####### Initialize the Dash app #######

dash.register_page(__name__, path="/")


############## Load Data ##############
############ Create Graphs ############

########## Set up the layout ##########

layout = dbc.Container([
    html.H4(
        "Welcome to our Project! We want to answer these questions:",
        className="text-center text-light"
    ),
    html.Br(),
    html.A(
        html.H1("How does the starting grid position influence the finishing position of drivers in the seasons from 1994 - 2024?", className='text-center page-header'),
    href='/gridPosition'),
    html.P("The starting grid position is an important factor in determining the finishing position of drivers in Formula and could be a key factor in determening the outcome of the race. We will analyze the data from the seasons 1994 - 2024 to determine the relationship between the starting grid position and the finishing position of drivers."),
    html.Br(),
    html.A(
    html.H1("How has the total number of crashes and retirements evolved in the seasons from 1994 - 2024?", className='text-center page-header'),
    href='/retirements'),
    html.P("Crashes and retirements are a common occurence in Formula 1. We will analyze the data from the seasons 1994 - 2024 to determine how the total number of crashes and retirements has evolved over the years."),
    html.Br(),
    html.A(
    html.H1("How does the number and the average duration of pitstops for a driver in a race relate to his finishing position?", className='text-center page-header'),
    href='/pitstops'),
    html.P("Pitstops are an important part of Formula 1. We will analyze the data from the seasons 2005 - 2024 to determine how the number and the average duration of pitstops for a driver has evolved over the years and how it relates to his finishing position."),
    html.Br(),
])
