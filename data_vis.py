import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
from enum import Enum

# Load JSON and CSV Files
df_prices = pd.read_csv('data/price_filtered.csv')


dfs = {
    'reg': {                                          # Region Dataframes
        'fam': pd.read_csv('data/region_fam.csv'),    # Grouped by family
        'idv': pd.read_csv('data/region_idv.csv'),    # Adjusted for individuals
        'bin': pd.read_csv('data/region_bin.csv'),    # Pre-binned for histogram
    },

    'prv': {                                          # Province Dataframes
        'fam': pd.read_csv('data/province_fam.csv'),  # Grouped by family
        'idv': pd.read_csv('data/province_idv.csv'),  # Adjusted for individuals
        'bin': pd.read_csv('data/province_bin.csv'),  # Pre-binned for histogram
    }
}

with open('data\Regions.json', 'r') as f:
    geojson_reg = json.load(f)
with open('data\Provinces.json', 'r') as f:
    geojson_prv = json.load(f)

reg_list = dfs['reg']['idv']['region_name'].tolist()
prv_list = dfs['prv']['idv']['province_name'].tolist()


# Main App
app = dash.Dash(__name__)

# Data
target_variable = 'food'
map_level = 'prv'
sel = {
    'reg': {

        'feature': 'properties.REGION',
        'geojson': geojson_reg,
        'grouper': 'region_name',
    },

    'prv': {
        'feature': 'properties.NAME_1',
        'geojson': geojson_prv,
        'grouper': 'province_name',
    }
}

map_selection = {
    'reg': "National Capital Region",
    'prv': "Metropolitan Manila"
}

# Controllers

rad_cat = dcc.RadioItems(
    id='region-radio',
    options=[
        {'label': html.Span('COL', className='radio-button'), 'value': 'COL'},
        {'label': html.Span('FOD', className='radio-button'), 'value': 'FOD'},
        {'label': html.Span('HNU', className='radio-button'), 'value': 'HNU'},
        {'label': html.Span('TRN', className='radio-button'), 'value': 'TRN'}
    ],
    value='COL',
    labelStyle={'display': 'inline-block'}
)

drp_prm = dcc.Dropdown(
    id='drp_prm',
    options=reg_list,
    value = reg_list[0]
)

drp_sec = dcc.Dropdown(
    id='drp_sec',
    options=reg_list,
    value = reg_list[0]
)

rad_lvl = dcc.RadioItems(
    id='rad_lvl',
    options=[
        {'label': 'Region', 'value': 'reg'},
        {'label': 'Province', 'value': 'prv'}
    ],
    value = 'reg',
    labelStyle={'display': 'inline-block'}
)

chk_cmp = dcc.Checklist(
    id='chk_cmp',
    options=[
        {'label': 'Enable Comparison', 'value': 'compare'}
    ],
    value = [],
)

# Create Histogram



@app.callback(
    Output('fig_hst', 'figure'),
    Input('rad_lvl', 'value')
)

def update_figures(map_level):

    filtered_df = dfs[map_level]['bin'][
        (dfs[map_level]['bin'][sel[map_level]['grouper']] == map_selection[map_level]) &
        (dfs[map_level]['bin']["variable"] == target_variable)
    ].copy()

    hist_fig = px.bar(
        filtered_df,
        x="bin_label",
        y="count",
        color=sel[map_level]['grouper'],
        labels={
            "bin_label": "Spending Range",
            "count": "Number of Families"
        },
        title="Food Spending Distribution in National Capital Region"
    )
    return hist_fig

# Create Line Graph
filtered_df = dfs[map_level]['fam'][
    (dfs[map_level]['fam'][sel[map_level]['grouper']] == map_selection[map_level]) &
    (dfs[map_level]['fam']['family_size'] <= 10)
].copy()

line_fig = px.line(
    filtered_df,
    x="family_size",
    y=target_variable,
    markers=True,
    color=sel[map_level]['grouper'],
    labels={
        "family_size": "Family Size",
        target_variable: f"Average {target_variable.title()}"
    },
    title=f"Growth of {target_variable.title()} by Family Size (≤10)"
)

map_fig = px.choropleth(
    dfs[map_level]['idv'],
    geojson=sel[map_level]['geojson'],
    locations=sel[map_level]['grouper'],
    featureidkey=sel[map_level]['feature'],
    color="col",
    color_continuous_scale="Viridis",
)

map_fig.update_layout(
    geo=dict(
        projection=dict(
            type="mercator",       
            scale=20 
        ),
        visible=False,
        center={
            "lat": 12.8797,
            "lon": 121.7740
        }
    ),
    margin=dict(l=20, r=20, t=30, b=30)
)

col_mid = html.Div(
    id='col_mid',
    children=[
    dcc.Graph(id='fig_hst'),
    dcc.Graph(figure=line_fig),
    ], 
    style={
        'width': '34%',
        'display': 'inline-block',
        'verticalAlign': 'top',
        'backgroundColor': '#f2f2f2'
    }
)

app.layout = html.Div([

    # 🔹 Header
    html.Div("Cost of Living Dashboard", style={
        'backgroundColor': '#1e1e2f',
        'color': 'white',
        'padding': '20px',
        'fontSize': '24px',
        'textAlign': 'left'
    }),

    # 🔹 Main Content (3 Columns)
    html.Div([

        # Left Column: Choropleth Map
        html.Div([
            dcc.Graph(figure=map_fig)
        ], style={
            'width': '33%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'backgroundColor': '#0f0f2f',
            'height': '100%', 
            'overflow': 'hidden',
        }),

        # Middle Column: Graphs
        col_mid,

        # Right Column: Region Info + Buttons
        html.Div([
            drp_prm,
            html.H3("REGION", id='region-title', style={'color': '#d33'}),
            drp_sec,

            rad_cat,
            rad_lvl,
            chk_cmp,
            html.Div(id='info-panel')  # placeholder for expanding section
            
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
    }),  # makes the 3 columns sit side-by-side

    # 🔹 Footer
    html.Div("© 2025 Cost of Living Project", style={
        'backgroundColor': '#1e1e2f',
        'color': 'white',
        'textAlign': 'center',
        'padding': '10px',
    })

], style={
    'display': 'flex',
    'flexDirection': 'column',
    'height': '100vh',
})

"""
@app.callback(
    Output()
)

def update_histogram():
    pass
"""

if __name__ == "__main__":
    app.run(debug=True)
