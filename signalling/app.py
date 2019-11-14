import os

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

server = app.server

app.title = "Transportation Engineer"
app.layout = html.Div([
    html.H2('Signalling'),
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)

