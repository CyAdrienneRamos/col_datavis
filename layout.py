from dash import html, dcc

from components import stores
from components import controls
from components import figures

layout = html.Div(id='layout',children=[
    stores.primary_selection,
    stores.secondary_selection,
    figures.fig_map,
    figures.fig_hist,
    figures.fig_line,
    
    html.Div(id='controls-container', children=[
        html.Div(id='dropdown-container', children=[
            controls.primary_dropdown,
            controls.secondary_dropdown
        ]),
        html.Div(id='location-controls', children=[
            controls.level_radio,
            controls.compare_checklist
        ])
    ]),
    
    html.Div(id='details-container', children=[
        html.Div(id='category-controls', children=[
            controls.category_radio
        ]),
        html.Div(id='category-details')
    ]),
    
    html.Div(id='header', children=[
        "Cost of Living Dashboard"
        ]),
    html.Div(id='footer', children=[
        "2025 Cost of Living Project"
    ])
])