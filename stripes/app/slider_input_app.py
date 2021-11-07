import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from stripes.app.formatters import format_svg
from stripes.models import ProgramStripes
from stripes.render import ColorTemplate, SvgRenderer

DEFAULT_CYCLE_LENGTH = 50  # seconds


class GroupElement(html.Div):
    def __init__(self, id: str, cycle_length: int):
        super(GroupElement, self).__init__(
            [
                dcc.Input(id=id + "-name"),
                dcc.Dropdown(
                    id=id + "-type",
                    options=[
                        {"label": "K", "value": "K"},
                        {"label": "P", "value": "P"},
                    ],
                ),
                dcc.Checklist(
                    id=id + "-inverted",
                    options=[
                        {"label": "inverted (marks non-green)", "value": "inverted"}
                    ],
                    value=[],
                ),
                html.Div(
                    dcc.RangeSlider(
                        min=0,
                        max=cycle_length,
                        step=1,
                        marks={i: str(i) for i in range(cycle_length)},
                        id=id + "-range",
                        value=[1, int(cycle_length / 2)],
                    ),
                ),
            ],
            id=id,
        )


def add_callbacks(app):
    @app.callback(
        Output("group_sliders", "children"),
        [Input("add_group_button", "n_clicks")],
        [State("group_sliders", "children")],
    )
    def add_group(n_clicks, group_elements):
        if n_clicks > 0:
            group_elements.append(
                GroupElement(f"group-{n_clicks}", DEFAULT_CYCLE_LENGTH)
            )
        return group_elements

    @app.callback(
        Output("slider-stripes", "children"),
        [Input("draw_program_stripes_button", "n_clicks")],
        [State("group_sliders", "children")],
    )
    def render_program_stripes(n_clicks, group_elements):
        # TODO: render on slider drag (with sliders 'drag_value')
        formatted_rows = []
        if n_clicks > 0:
            for signalling_group_input in group_elements:
                group_id = signalling_group_input["props"]["id"]
                group_name = signalling_group_input["props"]["children"][0]["props"][
                    "value"
                ]
                group_type = signalling_group_input["props"]["children"][1]["props"][
                    "value"
                ]
                group_green_inverted = bool(
                    signalling_group_input["props"]["children"][1]["props"]["value"]
                )
                group_slider_positions = signalling_group_input["props"]["children"][3][
                    "props"
                ]["children"]["props"]["value"]

                formatted_rows.append(
                    [
                        group_name,
                        {
                            "red": [
                                [0, group_slider_positions[0]],
                                [group_slider_positions[1], DEFAULT_CYCLE_LENGTH],
                            ],
                            "green": [
                                [group_slider_positions[0], group_slider_positions[1]]
                            ],
                        },
                    ]
                )
        template = ColorTemplate(SvgRenderer())
        return format_svg(
            template.render(ProgramStripes.from_ranges_list(formatted_rows))
        )


layout = html.Div(
    [
        html.H1("Stripes"),
        html.Button("Add group", id="add_group_button", n_clicks=0),
        html.Div(
            children=[GroupElement("group-0", DEFAULT_CYCLE_LENGTH)], id="group_sliders"
        ),
        html.Button("Draw program", id="draw_program_stripes_button", n_clicks=0),
        html.Div(id="slider-stripes"),
    ]
)
