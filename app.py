import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from signalling.app.setup import add_callbacks as add_signalling_callbacks
from signalling.app.setup import layout as signalling_layout
from stripes.app import add_callbacks as add_stripes_callbacks
from stripes.app import layout as stripes_layout

app = dash.Dash(__name__)
server = app.server

app.title = "Transportation Engineer"

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

app.config.suppress_callback_exceptions = True

index_layout = html.Div(
    [
        # represents the URL bar, doesn't render anything
        dcc.Location(id="url", refresh=False),
        dcc.Link("Transportation Engineer", href="/"),
        html.Br(),
        dcc.Link("signalling", href="/signalling"),
        html.Br(),
        dcc.Link("stripes", href="/stripes"),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/signalling":
        return signalling_layout
    elif pathname == "/stripes":
        return stripes_layout
    else:
        return index_layout


add_signalling_callbacks(app)
add_stripes_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
