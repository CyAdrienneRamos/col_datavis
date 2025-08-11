import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html

from utils.data_loader import dfs, PRV_TO_REG
from app_instance import app
from config import MAP_LEVEL_SETTINGS as lvlset
from config import VARIABLE_EXPANSION, MAP_COLOR_PALETTE

MAP_COLORBAR_LAYOUT = dict(
    xanchor='center',
    x=0.5,
    yanchor='top',
    y=0.1,
    title_text='Median Cost of Living per Person',
    title_side='top',
    orientation='h',
)

GRAPH_LEGEND_LAYOUT = dict(
    xanchor='center',
    x=0.5,
    yanchor='bottom',
    y=1.0,
    title_text = '',
    orientation='h',
)
GRAPH_TITLE_LAYOUT = dict(
    x=0.5,
    yanchor='bottom',
    y=0.94,
)

PLOTLY_FONT = dict(
    family='Quicksand, sans-serif',
    size=12,
    color='black'
)

def get_figline_title(category):
    return f'Median {VARIABLE_EXPANSION[category]} by Family Size'

def get_fighist_title(category):
    return f'Median {VARIABLE_EXPANSION[category]} Distribution'

# Choropleth Map
fig_map = dcc.Graph(id='fig-map', figure={}, className='graph-figure')

@app.callback(
    Output('fig-map', 'figure'),
    Input('level-radio', 'value'),
)
def update_map(level):
    
    fig = px.choropleth(
        dfs[level]['idv'],
        geojson=lvlset[level]['geojson'],
        locations=lvlset[level]['grouper'],
        featureidkey=lvlset[level]['feature'],
        color='col',
        color_continuous_scale=MAP_COLOR_PALETTE,
        labels={
            'region_name': 'Location',
            'col': 'Median Cost of Living'
        },
    )
    
    fig.update_geos(
        projection=dict(
            type='mercator',
            scale=23
        ),
        visible=False,
        center={
            'lat': 11.4797,
            'lon': 121.7740
        },
    )

    fig.update_layout(
        coloraxis_colorbar = MAP_COLORBAR_LAYOUT,
        font=PLOTLY_FONT,
        margin={'r': 20, 't': 0, 'l': 20, 'b': 50},
        autosize=True,
    )
    return fig

# Histogram
fig_hist = dcc.Graph(id='fig-hist', figure={}, className='graph-figure')

@app.callback(
    Output('fig-hist', 'figure'),
    
    Input('primary-dropdown', 'value'),
    Input('secondary-dropdown', 'value'),
    Input('category-radio', 'value'),
    Input('compare-checklist', 'value'),
    Input('level-radio', 'value')
)

def update_hist(primary_loc, secondary_loc, category, compare, level):
    title = get_fighist_title(category)
    
    locations = [primary_loc, secondary_loc] if compare else [primary_loc]
    
    dff = dfs[level]['bin'][
        (dfs[level]['bin'][lvlset[level]['grouper']].isin(locations)) &
        (dfs[level]['bin']['variable'] == category)
    ]
    
    fig = px.bar(
        dff,
        x='bin_label',
        y='percent',
        color=lvlset[level]['grouper'],
        labels={
            'region_name': 'Location',
            'bin_label': 'Spending Range (₱)',
            'percent': 'Percent of Families'
        },
        barmode='group',
    )
    
    fig.update_layout(
        legend=GRAPH_LEGEND_LAYOUT,
        title=GRAPH_TITLE_LAYOUT,
        font=PLOTLY_FONT,
        autosize=True,
        title_text=title,
        bargap=0.2,
    )
    return fig


# Line Graph
fig_line = dcc.Graph(id='fig-line', figure={}, className='graph-figure')

@app.callback(
    Output('fig-line', 'figure'),
    
    Input('primary-dropdown', 'value'),
    Input('secondary-dropdown', 'value'),
    Input('category-radio', 'value'),
    Input('compare-checklist', 'value'),
    State('level-radio', 'value')
)

def update_line(primary_loc, secondary_loc, category, compare, level):
    title = get_figline_title(category)
    
    locations = [primary_loc]
    if compare != []:
        locations.append(secondary_loc)
        
    dff = dfs[level]['fam'][
        (dfs[level]['fam'][lvlset[level]['grouper']].isin(locations)) &
        (dfs[level]['fam']['family_size'].mod(1) == 0) &
        (dfs[level]['fam']['family_size'] <= 10)
    ]
    
    fig = px.line(
        dff,
        x='family_size',
        y=category,
        markers=True,
        color=lvlset[level]['grouper'],
        labels={
            'region_name': 'Location',
            'family_size': 'Family Size',
            category: f'Median {category.title()}'
        }
    )
    fig.update_layout(
        legend=GRAPH_LEGEND_LAYOUT,
        title=GRAPH_TITLE_LAYOUT,
        font=PLOTLY_FONT,
        autosize=True,
        title_text=title,
    )
    
    return fig

@app.callback(
    Output('price-table', 'data'),
    Output('price-table', 'columns'),
    
    Input('primary-dropdown', 'value'),
    Input('secondary-dropdown', 'value'),
    Input('compare-checklist', 'value'),
    State('level-radio', 'value')
)
def update_table(primary_loc, secondary_loc, compare, level):
    df = dfs['pri']
    
    primary_prv = ''
    secondary_prv = ''
    
    # Map province → region if needed
    if level == 'prv':
        primary_prv = f' ({primary_loc})'
        secondary_prv = f' ({secondary_loc})'
        
        primary_loc = PRV_TO_REG.get(primary_loc, primary_loc)
        if compare:
            secondary_loc = PRV_TO_REG.get(secondary_loc, secondary_loc)

    # Single location
    if not compare:
        filtered_df = df[df['region'] == primary_loc].drop(columns=['region'])
        filtered_df = filtered_df.T.reset_index()
        filtered_df.columns = ['Product', f'{primary_loc}{primary_prv} Price']
    else:
        # Two locations
        filtered_df = df[df['region'].isin([primary_loc, secondary_loc])]
        filtered_df = filtered_df.set_index('region').T.reset_index()
        filtered_df.rename(columns={'index': 'Product', primary_loc: f'{primary_loc}{primary_prv} Price', secondary_loc: f'{secondary_loc}{secondary_prv} Price'}, inplace=True)

    columns = [{'name': col, 'id': col} for col in filtered_df.columns]
    data = filtered_df.to_dict('records')
    return data, columns

@app.callback(
    Output('category-info-left', 'children'),
    Input('primary-dropdown', 'value'),
    State('level-radio', 'value'),
    Input('category-radio', 'value'),
)

def update_info_left(loc, level, category):
    per_family = dfs[level]['fam'][
        (dfs[level]['fam'][lvlset[level]['grouper']] == loc) &
        (dfs[level]['fam']['family_size'] == 4)
    ][category].iloc[0]
    per_person = dfs[level]['idv'][
        dfs[level]['idv'][lvlset[level]['grouper']] == loc
    ][category].iloc[0]
    
    children = [
        html.Div(loc),
        html.Br(),
        html.Div(f'For a Family of Four: ₱{per_family}'),
        html.Div(f'Per Person: ₱{per_person}'),
    ]
    return children

@app.callback(
    Output('category-info-right', 'children'),
    Input('secondary-dropdown', 'value'),
    State('level-radio', 'value'),
    Input('category-radio', 'value'),
    Input('compare-checklist', 'value'),
    Input('primary-dropdown', 'value'),
)

def update_info_right(loc, level, category, compare, ploc):
    if not compare or (loc == ploc):
        return []
    
    per_family = dfs[level]['fam'][
        (dfs[level]['fam'][lvlset[level]['grouper']] == loc) &
        (dfs[level]['fam']['family_size'] == 4)
    ][category].iloc[0]
    per_person = dfs[level]['idv'][
        dfs[level]['idv'][lvlset[level]['grouper']] == loc
    ][category].iloc[0]
    
    children = [
        html.Div(loc),
        html.Br(),
        html.Div(f'For a Family of Four: ₱{per_family}'),
        html.Div(f'Per Person: ₱{per_person}'),
    ]
    return children

@app.callback(
    Output('category-label', 'children'),
    Input('category-radio', 'value'),
)

def update_category_label(category):
    return [VARIABLE_EXPANSION[category]]