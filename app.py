import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from signalling.app.setup import add_callbacks as add_signalling_callbacks
from signalling.app.setup import layout as signalling_layout
from stripes.app.slider_input_app import add_callbacks as add_stripes_slider_callbacks
from stripes.app.slider_input_app import layout as stripes_slider_layout
from stripes.app.string_input_app import add_callbacks as add_stripes_text_callbacks
from stripes.app.string_input_app import layout as stripes_text_layout

app = dash.Dash(__name__)
server = app.server

app.title = "Transportation Engineer"

app.layout = html.Div([dcc.Location(id="url"), html.Div(id="page-content")])

app.config.suppress_callback_exceptions = True

index_layout = html.Div(
    [
        # represents the URL bar, doesn't render anything
        dcc.Location(id="url", refresh=False),
        dcc.Link("Transportation Engineer", href="/"),
        html.Br(),
        dcc.Link("signalling", href="/signalling"),
        html.Br(),
        dcc.Link("stripes (basic)", href="/stripes-slider"),
        html.Br(),
        dcc.Link("stripes (advanced)", href="/stripes-text"),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return index_layout
    elif pathname == "/signalling":
        return signalling_layout
    elif pathname == "/stripes-slider":
        return stripes_slider_layout
    elif pathname == "/stripes-text":
        return stripes_text_layout
    else:
        return index_layout


add_signalling_callbacks(app)
add_stripes_slider_callbacks(app)
add_stripes_text_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
