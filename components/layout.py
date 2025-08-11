from dash import html, dcc, dash_table

from components import stores
from components import controls
from components import figures

from utils.data_loader import region_list

layout = html.Div(id='layout',children=[
    stores.primary_selection,
    stores.secondary_selection,
    
    figures.fig_map,
    figures.fig_hist,
    figures.fig_line,
    
    html.Div(id='display-panel', children=[
        html.Div(id='location-controls', children=[
            html.Div([
                controls.primary_dropdown,
                controls.secondary_dropdown
            ]),
            html.Div(id='location-config', children=[
                controls.level_radio,
                controls.compare_checklist
            ])
        ], style={'gridArea': 'location-controls'}),
        
        html.Div(id='category-details', children=[
            html.Div(id='category-controls', children=[
                controls.category_radio,
                html.Div(id='category-label', children=[
                    'Cost of Living'
                ], style={
                    'fontSize':'2.5vh',
                    'marginTop':'1vh',
                })
            ], style={'gridArea': 'category-controls'}),
            
            html.Div(id='category-info-left', style={'gridArea': 'category-info-left'}),
            
            html.Div(id='category-info-right', style={'gridArea': 'category-info-right'}),
        ], style={
            'fontSize':'1.8vh',
        }),
    ]),
    
    dash_table.DataTable(id='price-table',
        style_table={
            'maxHeight': '42vh',   # Table height limit
            'overflowY': 'auto',    # Vertical scroll if too tall
            'overflowX': 'auto',    # Horizontal scroll if too wide
            'width': '28vw',
            'borderRadius': '5px',
            'border': '1px solid #022B50'},
        style_header={
            'backgroundColor': '#022B50',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'fontFamily': 'Quicksand',
            'fontSize': '1.8vh'
        },
        style_cell={
            'textAlign': 'center',
            'padding': '8px',
            'whiteSpace': 'normal',
            'fontFamily': 'Quicksand',
            'fontSize': '1.5vh',
            'border': '1px solid #022B50'
        },
    ),
    
    html.Div(id='header', children=[
        'Cost of Living Dashboard'
        ]),
    html.Div(id='footer', children=[
        '2025 Cost of Living Project'
    ])
])