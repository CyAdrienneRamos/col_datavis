from dash import html, dcc

import config
from components import stores
from components import controls
from components import figures

layout = html.Div(className='layout',children=[
    stores.primary_selection,
    stores.secondary_selection,
    figures.fig_map,
    figures.fig_hist,
    figures.fig_line,
    
    html.Div(className='controls-container', children=[
        html.Div(className='dropdown-container', children=[
            controls.primary_dropdown,
            controls.secondary_dropdown
        ]),
        html.Div(className='location-controls', children=[
            controls.level_radio,
            controls.compare_checklist
        ])
    ]),
    
    html.Div(className='details-container', children=[
            html.Div(className='category-controls', children=[
                controls.category_radio
            ]),
            html.Div(className='category-details')
        ]),
    
    html.Div(id='header', children=[
        "Cost of Living Dashboard"
        ]),
    html.Div(id='footer', children=[
        "2025 Cost of Living Project"
    ])
])

'''
# App Layout -----------------------------------------------------------------------------------------------------------
layout = html.Div([
    # Header
    html.Div("Cost of Living Dashboard", style={
        'backgroundColor': '#1e1e2f',
        'height': '40vh',
        'color': 'white',
        'padding': '20px',
        'fontSize': '24px',
        'textAlign': 'left'
    }),

    # Main Content: 3 Columns
    html.Div([

        # Column 1: Map
        html.Div([
            dcc.Graph(id='fig-map', figure={})
        ], style={
            'width': '33%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'backgroundColor': '#0f0f2f',
            'height': '100%',
            'overflow': 'hidden'
        }),

        # Column 2: Histogram + Line
        html.Div([
            dcc.Graph(id='fig-hist', figure={}, style={'height': '40vh'}),
            dcc.Graph(id='fig-line', figure={}, style={'height': '40vh'})
        ], style={
            'width': '34%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'backgroundColor': '#f2f2f2'
        }),

        # Column 3: Controls
        html.Div([
            controls.primary_dropdown,
            controls.compare_checklist,
            controls.secondary_dropdown,
            controls.level_radio,
            controls.category_radio
        ], style={
            'width': '33%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'backgroundColor': '#e0e0e0',
            'height': '100%'
        })

    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'flex-start',
        'overflow': 'hidden',
        'backgroundColor': "#96c7ab"
    }),

    # Footer
    html.Div("© 2025 Cost of Living Project", style={
        'backgroundColor': '#1e1e2f',
        'color': 'white',
        'textAlign': 'center',
        'padding': '10px'
    })

], style={
    'display': 'flex',
    'flexDirection': 'column',
    'height': '100vh'
})
'''