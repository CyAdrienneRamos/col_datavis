import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, dcc

from data_loader import dfs
from app_instance import app
from config import MAP_LEVEL_SETTINGS as lvlset

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

VARIABLE_EXPANSION = {
    'col': 'Cost of Living',
    'food': 'Food Expense',
    'housing': 'Housing and Utilities Expense',
    'transport': 'Transportation Expense',
}

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
        color_continuous_scale='Viridis',
        labels={
            'region_name': 'Location',
            'col': 'Median Cost of Living'
        }
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
    
    locations = [primary_loc]
    if compare != []:
        locations.append(secondary_loc)
    
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
            "family_size": "Family Size",
            category: f"Median {category.title()}"
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