import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State


def read_inlets_data(rows):
    return rows


def format_cartogram_image(dwg):
    return str(dwg)


def add_callbacks(app):
    @app.callback(
        Output("cartogram_image_container", "children"),
        [Input("draw_cartogram_button", "n_clicks")],
        [State("cartogram_inlets_table", "data"),],
    )
    def render_cartogram_image(n_clicks, inlets_table):
        if not n_clicks:
            return
        inlets_data = read_inlets_data(inlets_table)
        return format_cartogram_image(inlets_data)


layout = html.Div(
    [
        html.H1("Cartogram"),
        dt.DataTable(
            id="cartogram_inlets_table",
            columns=[
                {"name": x, "id": x} for x in ["inlet\\inlet", "1", "2", "3", "4"]
            ],
            data=[{"inlet\\inlet": x} for x in ["1", "2", "3", "4"]],
            editable=True,
        ),
        html.Button("Draw cartogram", id="draw_cartogram_button", n_clicks=0),
        html.Div(id="cartogram_image_container"),
    ]
)
