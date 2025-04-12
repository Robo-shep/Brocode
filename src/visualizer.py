import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# Example data
data = {
    "Platform": ["Reddit", "Hacker News", "Quora"],
    "Sentiment": ["Positive", "Neutral", "Negative"]
}
df = pd.DataFrame(data)

fig = px.bar(df, x="Platform", y="Sentiment")

app.layout = html.Div([
    html.H1('Market Research Bot Visualization'),
    dcc.Graph(id='sentiment-graph', figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)
