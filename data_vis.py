import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import json

app = dash.Dash(__name__)

df = px.data.gapminder().query("year == 2007")
fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country",
                 log_x=True, size_max=60)

with open("data\Regions.json", "r") as f:
    geojson_regions = json.load(f)
with open("data\Provinces.json", "r") as f:
    geojson_provinces = json.load(f)

app.layout = html.Div([

    # 🔹 Header
    html.Div("Cost of Living Dashboard", style={
        'backgroundColor': '#1e1e2f',
        'color': 'white',
        'padding': '20px',
        'fontSize': '24px',
        'textAlign': 'center'
    }),

    # 🔹 Main Content (3 Columns)
    html.Div([

        # Left Column: Choropleth Map
        html.Div([
            dcc.Graph(figure=fig)
        ], style={
            'width': '33%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'backgroundColor': '#0f0f2f'
        }),

        # Middle Column: Graphs
        html.Div([
            dcc.Graph(figure=fig),
            dcc.Graph(figure=fig),
        ], style={
            'width': '34%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'backgroundColor': '#f2f2f2'
        }),

        # Right Column: Region Info + Buttons
        html.Div([
            html.H2(id='region-title', style={'color': '#d33'}),
            html.Div(id='summary-stats', children=[
                html.P("Mean:"),
                html.P("Median:"),
                html.P("Q1:"),
                html.P("Q3:")
            ]),
            html.Button("FOOD", id='btn-food', style={'margin': '5px'}),
            html.Button("RENT", id='btn-rent', style={'margin': '5px'}),
            html.Button("UTILITIES", id='btn-utilities', style={'margin': '5px'}),
            html.Button("TRANSPORT", id='btn-transport', style={'margin': '5px'}),
            html.Div(id='info-panel')  # placeholder for expanding section
        ], style={
            'width': '33%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'backgroundColor': '#e0e0e0'
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

if __name__ == "__main__":
    app.run(debug=True)
