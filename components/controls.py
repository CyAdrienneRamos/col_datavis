from dash import html, dcc, Input, Output, no_update, State, ctx

from data_loader import region_list, province_list
from app_instance import app
import config

# For switching between tabs
category_radio = dcc.RadioItems(
    id='category-radio',
    options=[
        {'label': html.Span('Cost of Living', className='radio-button'), 'value': 'col'},
        {'label': html.Span('Transportation', className='radio-button'), 'value': 'transport'},
        {'label': html.Span('Housing and Utilities', className='radio-button'), 'value': 'housing'},
        {'label': html.Span('Food', className='radio-button'), 'value': 'food'},
    ],
    value=config.DEFAULT_CATEGORY,
    labelStyle={'display': 'inline-block'}
)
"""
@app.callback(
    Output('category-radio', 'labelStyle'),
    Input('category-radio', 'value'),
    State('category-radio', 'options'),
)
def update_styles(selected, options):
    new_styles = []
    for option in options:
        base_style = {'display': 'inline-block', 'padding': '10px 20px', 'border': '1px solid #ccc', 'border-radius': '5px', 'margin': '5px', 'cursor': 'pointer'}
        if option['value'] == selected:
            base_style.update({'backgroundColor': '#4285f4', 'color': 'white', 'border-color': '#4285f4'})
        new_styles.append(base_style)
    return new_styles
"""

# For selecting primary location
primary_dropdown = dcc.Dropdown(
    id='primary-dropdown',
    options=region_list,
    value=region_list[0]
)

# For selecting secondary location if enabled
secondary_dropdown = dcc.Dropdown(
    id='secondary-dropdown',
    options=region_list,
    value=region_list[0]
)

# For selecting map level
level_radio = dcc.RadioItems(
    id='level-radio',
    options=[
        {'label': 'Region', 'value': 'reg'},
        {'label': 'Province', 'value': 'prv'}
    ],
    value='reg',
    labelStyle={'display': 'inline-block'}
)

# For toggling comparison mode
compare_checklist = dcc.Checklist(
    id='compare-checklist',
    options=[{'label': 'Enable Comparison', 'value': 'compare'}],
    value=[]
)