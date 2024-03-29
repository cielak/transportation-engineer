from dash import dash_table as dt
from dash import dcc, html
from dash.dependencies import Input, Output, State

from stripes.app.formatters import format_svg, read_rows
from stripes.models import ProgramStripes, SecondType
from stripes.render import ColorTemplate, SvgRenderer


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
        formatted_annotations = (
            [
                (int(x.split()[0]), " ".join(x.split()[1:]))
                for x in annotations.split(", ")
            ]
            if annotations
            else None
        )
        annotate_greens = green_lengths == ["green_lengths"]
        template = ColorTemplate(
            SvgRenderer(),
            annotate_greens=annotate_greens,
            left_offset=left_offset,
            right_offset=right_offset,
            annotations=formatted_annotations,
        )
        return format_svg(
            template.render(ProgramStripes.from_ranges_list(formatted_rows))
        )


layout = html.Div(
    [
        html.H1("Stripes"),
        html.Div(
            [
                html.Div("Available values:"),
                html.Ul([html.Li(t.name) for t in SecondType]),
                html.Div(
                    "Example input: || K1 | off 0-5, yellow 5-10, red 10-30, red_yellow 30-31, green 31-50, yellow 50-53, red 53-60 ||"
                ),
            ]
        ),
        html.Button("Add group", id="add_group_button", n_clicks=0),
        dt.DataTable(
            id="groups_table",
            columns=[{"name": x, "id": x} for x in ["group_name", "group_data"]],
            data=[{"group_name": "", "group_data": ""} for _ in range(2)],
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
                                    value=["green_lengths"],
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
                                        value=0,
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
                                        value=0,
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
                                        placeholder="0 Phase 1, 5 Phase shift, 10, Phase 2",
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
