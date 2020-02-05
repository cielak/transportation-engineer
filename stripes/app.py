import base64
from collections import defaultdict

import dash
import dash_table as dt
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table as dt

from stripes.models import ProgramStripes, SecondType
from stripes.render import SvgRenderer


def format_rows(rows):
    def format_row(row):
        data = [s.strip() for s in row["group_data"].split(",")]
        row_data = defaultdict(list)
        for s in data:
            sec_type, sec_range = s.split(" ")
            row_data[sec_type].append([int(x) for x in sec_range.split("-")])
        return [row["group_name"], row_data]

    return [format_row(row) for row in rows]


def add_callbacks(app):
    @app.callback(
        Output("groups_table", "data"),
        [Input("add_group_button", "n_clicks")],
        [State("groups_table", "data"), State("groups_table", "columns"),],
    )
    def add_group(n_clicks, rows, columns):
        if n_clicks > 0:
            rows.append({c["id"]: "" for c in columns})
        return rows

    @app.callback(
        Output("stripes", "children"),
        [Input("draw_stripes_button", "n_clicks")],
        [State("groups_table", "data"),],
    )
    def render_stripes(n_clicks, rows):
        if not n_clicks:
            return
        formatted_rows = format_rows(rows)
        renderer = SvgRenderer()
        raw_content = renderer.render_program(
            ProgramStripes.from_ranges_list(formatted_rows)
        )
        content = str(base64.b64encode(raw_content.encode("utf-8")), "utf-8")
        return html.Img(src="data:image/svg+xml;base64," + content)


layout = html.Div(
    [
        html.H1("Stripes"),
        html.Div(
            [
                html.Div("Available values:"),
                html.Ul([html.Li(t.name) for t in SecondType]),
            ]
        ),
        html.Button("Add group", id="add_group_button", n_clicks=0),
        dt.DataTable(
            id="groups_table",
            columns=[{"name": x, "id": x} for x in ["group_name", "group_data"]],
            data=[
                {"group_name": "K1", "group_data": "off 0-5, red 5-10, green 10-15"},
                {
                    "group_name": "P1",
                    "group_data": "off 0-2, red 2-10, yellow 10-11, green 11-15",
                },
            ],
            editable=True,
            row_deletable=True,
        ),
        html.Button("Draw program stripes", id="draw_stripes_button", n_clicks=0),
        html.Div(id="stripes"),
    ]
)
