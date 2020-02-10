import base64
from collections import defaultdict

import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State

from stripes.models import ProgramStripes, SecondType
from stripes.render import SvgRenderer


def read_rows(rows):
    def format_row(row):
        data = [s.strip() for s in row["group_data"].split(",")]
        row_data = defaultdict(list)
        for s in data:
            sec_type, sec_range = s.split(" ")
            row_data[sec_type].append([int(x) for x in sec_range.split("-")])
        return [row["group_name"], row_data]

    return [format_row(row) for row in rows]


def format_svg(dwg):
    raw_content = dwg.tostring()
    content = str(base64.b64encode(raw_content.encode("utf-8")), "utf-8")
    return html.Div(html.Img(src="data:image/svg+xml;base64," + content))


def add_callbacks(app):
    @app.callback(
        Output("groups_table", "data"),
        [Input("add_group_button", "n_clicks")],
        [State("groups_table", "data"), State("groups_table", "columns")],
    )
    def add_group(n_clicks, rows, columns):
        if n_clicks > 0:
            rows.append({c["id"]: "" for c in columns})
        return rows

    @app.callback(
        Output("stripes", "children"),
        [Input("draw_program_stripes_button", "n_clicks")],
        [
            State("groups_table", "data"),
            State("program_stripes_green_lengths_input", "value"),
            State("program_stripes_annotations_input", "value"),
            State("program_stripes_left_offset_input", "value"),
            State("program_stripes_right_offset_input", "value"),
        ],
    )
    def render_program_stripes(
        n_clicks, rows, green_lengths, annotations, left_offset, right_offset
    ):
        if not n_clicks:
            return
        formatted_rows = read_rows(rows)
        formatted_annotations = [
            (int(x.split()[0]), " ".join(x.split()[1:]))
            for x in annotations.split(", ")
        ]
        annotate_greens = green_lengths == ["green_lengths"]
        renderers = [
            SvgRenderer(),
            SvgRenderer(
                annotate_greens=annotate_greens,
                left_offset=left_offset,
                right_offset=right_offset,
                annotations=formatted_annotations,
            ),
        ]
        return [
            format_svg(
                r.render_program(ProgramStripes.from_ranges_list(formatted_rows))
            )
            for r in renderers
        ]


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
                {
                    "group_name": "demo",
                    "group_data": "off 0-5, red 5-10, red_yellow 10-11, green 11-15, yellow 15-18, green_blinking 18-22, yellow_blinking 22-27",
                },
            ],
            editable=True,
            row_deletable=True,
        ),
        html.Div(
            [
                "Optional settings:",
                html.Ul(
                    [
                        html.Li(
                            html.Div(
                                dcc.Checklist(
                                    id="program_stripes_green_lengths_input",
                                    options=[
                                        {
                                            "label": "Show green lenghts",
                                            "value": "green_lengths",
                                        }
                                    ],
                                )
                            )
                        ),
                        html.Li(
                            [
                                html.Div("Ruler offset from left"),
                                html.Div(
                                    dcc.Input(
                                        id="program_stripes_left_offset_input",
                                        type="number",
                                        value=2,
                                    )
                                ),
                            ]
                        ),
                        html.Li(
                            [
                                html.Div("Ruler offset from right"),
                                html.Div(
                                    dcc.Input(
                                        id="program_stripes_right_offset_input",
                                        type="number",
                                        value=2,
                                    )
                                ),
                            ]
                        ),
                        html.Li(
                            [
                                html.Div("Annnotations"),
                                html.Div(
                                    dcc.Input(
                                        id="program_stripes_annotations_input",
                                        type="text",
                                        value="-2 Faza 1, 0 PF 1-2, 23 Faza 2",
                                        size="50",
                                    )
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
        html.Button("Draw program", id="draw_program_stripes_button", n_clicks=0),
        html.Div(id="stripes"),
    ]
)
