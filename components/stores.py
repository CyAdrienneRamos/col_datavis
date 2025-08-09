from dash import html, dcc, Input, Output, no_update, State, ctx

from data_loader import region_list, province_list
from app_instance import app
import config

primary_selection = dcc.Store(id='primary-selection', data={
    'reg': config.DEFAULT_MAP_SELECTION['reg'],
    'prv': config.DEFAULT_MAP_SELECTION['prv'],
})

@app.callback(
    Output('primary-dropdown', 'options'),
    Input('level-radio', 'value')
)

def update_primary_options(level):
    return region_list if level == 'reg' else province_list

@app.callback(
    Output('primary-selection', 'data'),
    Output('primary-dropdown', 'value'),
    
    Input('primary-dropdown', 'options'),
    Input('fig-map', 'clickData'),
    
    State('compare-checklist', 'value'),
    State('primary-selection', 'data'),
    State('level-radio', 'value')
)

def update_primary_dropdown(options, clickData, compare, current, level):
    if ctx.triggered_id == 'fig-map':
        if compare != []:
            return no_update
        if clickData == None:
            return no_update
        loc = clickData['points'][0]['location']
        current[level] = loc
        return current, loc
    else:
        return no_update, current[level]

secondary_selection = dcc.Store(id='secondary-selection', data={
    'reg': config.DEFAULT_MAP_SELECTION['reg'],
    'prv': config.DEFAULT_MAP_SELECTION['prv'],
})

@app.callback(
    Output('secondary-dropdown', 'options'),
    Input('level-radio', 'value')
)

def update_secondary_options(level):
    return region_list if level == 'reg' else province_list

@app.callback(
    Output('secondary-selection', 'data'),
    Output('secondary-dropdown', 'value'),
    
    Input('secondary-dropdown', 'options'),
    Input('fig-map', 'clickData'),
    
    State('compare-checklist', 'value'),
    State('secondary-selection', 'data'),
    State('level-radio', 'value')
)

def update_secondary_dropdown(options, clickData, compare, current, level):
    if ctx.triggered_id == 'fig-map':
        if compare == []:
            return no_update
        if clickData == None:
            return no_update
        loc = clickData['points'][0]['location']
        current[level] = loc
        return current, loc
    else:
        return no_update, current[level]