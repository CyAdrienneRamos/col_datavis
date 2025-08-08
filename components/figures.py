import plotly.express as px
from dash import Input, Output, State

from data_loader import dfs
from app_instance import app
from config import MAP_LEVEL_SETTINGS as lvlset

# Figures --------------------------------------------------------------------------------------------------------------

# Column 1
# Choropleth Map
@app.callback(
    Output('fig-map', 'figure'),
    Input('level-radio', 'value'),
)

def update_map(level):
    # Choose level (region/province)
    if level == 'reg':
        group_field = 'region'
    else:
        group_field = 'province'

    fig = px.choropleth(
        dfs[level]['idv'],
        geojson=lvlset[level]['geojson'],
        locations=lvlset[level]['grouper'],
        featureidkey=lvlset[level]['feature'],
        color='col',
        color_continuous_scale='Viridis'
    )

    fig.update_layout(
        geo=dict(
            projection=dict(
                type='mercator',       
                scale=20 
            ),
            visible=False,
            center={
                'lat': 12.8797,
                'lon': 121.7740
            }
        ),
        margin={'r':20, 't':30, 'l':20, 'b':30})
    return fig

# Column 2
# Histogram
@app.callback(
    Output('fig-hist', 'figure'),
    
    Input('category-radio', 'value'),
    Input('primary-dropdown', 'value'),
    Input('level-radio', 'value')
)

def update_hist(category, primary_loc, level):
    targets = {
        'COL': 'col',
        'FOD': 'food',
        'HNU': 'housing',
        'TRN': 'transport'
    }
    
    titles = {
        'COL': f'Cost of Living Distribution',
        'FOD': f'Food Expense Distribution',
        'HNU': f'Housing and Utilities Expense Distribution',
        'TRN': f'Transportation Expense Distribution',
    }
    
    dff = dfs[level]['bin'][
        (dfs[level]['bin'][lvlset[level]['grouper']] == primary_loc) &
        (dfs[level]['bin']['variable'] == targets[category])
    ]
    
    fig = px.bar(
        dff,
        x='bin_label',
        y='count',
        color=lvlset[level]['grouper'],
        labels={
            'bin_label': 'Spending Range',
            'count': 'Number of Families'
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
        bargap=0.2
    )
    return fig


# Column 2
# Line Graph
@app.callback(
    Output('fig-line', 'figure'),
    
    Input('primary-dropdown', 'value'),
    Input('secondary-dropdown', 'value'),
    Input('category-radio', 'value'),
    Input('compare-checklist', 'value'),
    State('level-radio', 'value')
)

def update_line(primary_loc, secondary_loc, category, compare, level):
    targets = {
        'COL': 'col',
        'FOD': 'food',
        'HNU': 'housing',
        'TRN': 'transport'
    }
    
    titles = {
        'COL': f'Median Cost of Living by Family Size',
        'FOD': f'Median Food Expense by Family Size',
        'HNU': f'Median Housing and Utilities Expense by Family Size',
        'TRN': f'Median Transportation Expense by Family Size',
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
        y=targets[category],
        markers=True,
        color=lvlset[level]['grouper'],
        labels={
            "family_size": "Family Size",
            targets[category]: f"Median {targets[category].title()}"
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
        )
    )
    return fig