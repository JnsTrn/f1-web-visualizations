import dash

from dash import html

import dash_bootstrap_components as dbc


####### Initialize the Dash app #######

style_sheet = [dbc.themes.LUX]
app = dash.Dash(
    __name__,
    external_stylesheets=style_sheet,
    use_pages=True,
)
app.title = 'DSP 2025 - Team 897'
server = app.server


########## Create Bootstrap Components ##########

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Home', href='/')),
        dbc.NavItem(
            dbc.NavLink('Grid Position Analysis', href='/grid-position')
        ),
        dbc.NavItem(dbc.NavLink('Retirement Analysis', href='/retirements')),
        dbc.NavItem(dbc.NavLink('Pit Stop Analysis', href='/pit-stops')),
        dbc.NavItem(dbc.NavLink('About the Data', href='/about-data')),
        dbc.NavItem(html.Img(
            src=dash.get_asset_url('red_f1_car_clipped_small.png'),
            style={'height': '40px'},
        )),
    ],
    brand='DSP 2025 - Team 897',
    brand_href='/',
    dark=True,
    fluid=True,
)

# Structure AI generated
imprint_section = html.Footer(
    [
        dbc.Container(
            [
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.P(
                                    [
                                        '',
                                        html.A(
                                            'Christian-Albrechts-Universität zu Kiel',
                                            href='https://www.uni-kiel.de/en/imprint',
                                            target='_blank',
                                            className='text-center text-light',
                                        ),
                                    ],
                                    className='text-center text-light',
                                ),
                                html.P(
                                    'Christian-Albrechts-Platz 4',
                                    className='text-center text-light',
                                ),
                                html.P(
                                    '24118 Kiel, Germany',
                                    className='text-center text-light',
                                ),
                                html.P(
                                    [
                                        'Telephone: ',
                                        html.A(
                                            '+49 (0431) 880-00',
                                            href='tel:+4943188000',
                                            className='text-light',
                                        ),
                                    ],
                                    className='text-center text-light',
                                ),
                                html.P(
                                    [
                                        'E-Mail: ',
                                        html.A(
                                            'mail@uni-kiel.de',
                                            href='mailto:mail@uni-kiel.de',
                                            className='text-light',
                                        ),
                                    ],
                                    className='text-center text-light',
                                ),
                            ],
                            width=12,
                        )
                    ],
                    justify='center',
                ),
            ],
            fluid=True,
            className='text-light',
        )
    ]
)


########## Set up the layout ##########

#Structure AI generated
app.layout = dbc.Container(
    [navbar, html.Br(), dash.page_container, html.Br(), imprint_section],
    fluid=True,
    className='bg-dark text-light', style={'backgroundColor': 'black'}
)


############# Run the app #############

if __name__ == '__main__':
    app.run(debug=False)
