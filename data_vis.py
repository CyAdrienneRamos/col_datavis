import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = px.data.gapminder().query("year == 2007")
fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country",
                 log_x=True, size_max=60)

app.layout = html.Div([
    html.H1("Gapminder Data Visualization"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
