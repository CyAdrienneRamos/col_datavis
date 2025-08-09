import plotly.express as px
from dash import Input, Output, State, dcc

from data_loader import dfs
from app_instance import app
from config import MAP_LEVEL_SETTINGS as lvlset

# Column 1
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
        }
    )

    fig.update_layout(
        margin={'r': 20, 't': 0, 'l': 20, 'b': 50},
        autosize=True,
        coloraxis_colorbar_x=0.5,
        coloraxis_colorbar_yanchor='top',
        coloraxis_colorbar_y=0.1,
        coloraxis_colorbar_title='Median Cost of Living per Person',
        coloraxis_colorbar_title_side='top',
        coloraxis_colorbar_orientation='h',
        
    )
    return fig

# Column 2
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
    titles = {
        'col': f'Cost of Living Distribution',
        'food': f'Food Expense Distribution',
        'housing': f'Housing and Utilities Expense Distribution',
        'transport': f'Transportation Expense Distribution',
    }
    
    if compare == []:
        dff = dfs[level]['bin'][
            (dfs[level]['bin'][lvlset[level]['grouper']] == primary_loc) &
            (dfs[level]['bin']['variable'] == category)
        ]
    else:
        dff = dfs[level]['bin'][
            (dfs[level]['bin'][lvlset[level]['grouper']].isin([primary_loc, secondary_loc])) &
            (dfs[level]['bin']['variable'] == category)
        ]

    
    fig = px.bar(
        dff,
        x='bin_label',
        y='percent',
        color=lvlset[level]['grouper'],
        labels={
            'bin_label': 'Spending Range',
            'count': 'Percent of Families'
        },
        title=titles[category],
        barmode='group',
    )
    
    fig.update_layout(
        legend=dict(
            orientation="h",         # horizontal legend
            yanchor="top",           # anchor the legend's y position
            y=-0.3,                  # move below the plot
            xanchor="center",        # anchor the legend's x position
            x=0.5                    # center the legend
        ),
        bargap=0.2,
        autosize=True,
    )
    return fig


# Column 2
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
    titles = {
        'col': f'Median Cost of Living by Family Size',
        'food': f'Median Food Expense by Family Size',
        'housing': f'Median Housing and Utilities Expense by Family Size',
        'transport': f'Median Transportation Expense by Family Size',
    }
    
    if compare == []:
        dff = dfs[level]['fam'][
            (dfs[level]['fam'][lvlset[level]['grouper']] == primary_loc) &
            (dfs[level]['fam']['family_size'].mod(1) == 0) &
            (dfs[level]['fam']['family_size'] <= 10)
        ]
    else:
        dff = dfs[level]['fam'][
            (dfs[level]['fam'][lvlset[level]['grouper']].isin([primary_loc, secondary_loc])) &
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
            "family_size": "Family Size",
            category: f"Median {category.title()}"
        },
        title=titles[category]
    )
    fig.update_layout(
        legend=dict(
            orientation="h",         # horizontal legend
            yanchor="top",           # anchor the legend's y position
            y=-0.3,                  # move below the plot
            xanchor="center",        # anchor the legend's x position
            x=0.5                    # center the legend
        ),
        autosize=True
    )
    return fig