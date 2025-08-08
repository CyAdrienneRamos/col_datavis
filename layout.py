from dash import html, dcc

import config
from components import stores
from components import controls
from components import figures

# App Layout -----------------------------------------------------------------------------------------------------------
layout = html.Div([
    dcc.Store(id='primary-selection', data={
        'reg': config.DEFAULT_MAP_SELECTION['reg'],
        'prv': config.DEFAULT_MAP_SELECTION['prv'],
    }),
    dcc.Store(id='secondary-selection', data={
        'reg': config.DEFAULT_MAP_SELECTION['reg'],
        'prv': config.DEFAULT_MAP_SELECTION['prv'],
    }),

    # Header
    html.Div("Cost of Living Dashboard", style={
        'backgroundColor': '#1e1e2f',
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
