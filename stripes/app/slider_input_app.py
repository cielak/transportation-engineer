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
                dcc.Input(id=f"{id}-name", value=id),
                dcc.Dropdown(
                    id=f"{id}-type",
                    options=[
                        {"label": "K", "value": "K"},
                        {"label": "P", "value": "P"},
                    ],
                    value="K",
                ),
                dcc.Checklist(
                    id=id + "-inverted",
                    options=[{"label": "start on green", "value": "inverted"}],
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
                        className="default-signalling-slider",
                    ),
                ),
            ],
            id=id,
        )


def add_callbacks(app):

    for i in range(100):

        @app.callback(
            Output(f"group-{i}-range", "className"),
            [Input(f"group-{i}-inverted", "value")],
        )
        def invert_slider_marking(inverted):
            invert_slider = inverted == ["inverted"]
            default_marking_style_class = "default-signalling-slider"
            inverted_marking_style_class = "inverted-signalling-slider"
            slider_style_class = (
                default_marking_style_class
                if not invert_slider
                else inverted_marking_style_class
            )
            return slider_style_class

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
        Output("slider_stripes", "children"),
        [Input("draw_program_stripes_button", "n_clicks")],
        [State("group_sliders", "children")],
    )
    def render_program_stripes(n_clicks, group_elements):
        # TODO: render on slider drag (with sliders 'drag_value')
        formatted_rows = []
        for signalling_group_input in group_elements:
            group_id = signalling_group_input["props"]["id"]
            group_name = signalling_group_input["props"]["children"][0]["props"][
                "value"
            ]
            group_type = signalling_group_input["props"]["children"][1]["props"][
                "value"
            ]
            group_start_on_green = bool(
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
                    }
                    if group_start_on_green
                    else {
                        "green": [
                            [0, group_slider_positions[0]],
                            [group_slider_positions[1], DEFAULT_CYCLE_LENGTH],
                        ],
                        "red": [[group_slider_positions[0], group_slider_positions[1]]],
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
        html.Div(id="slider_stripes"),
    ]
)
