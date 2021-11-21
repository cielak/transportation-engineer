import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from stripes.app.formatters import format_svg
from stripes.models import ProgramStripes
from stripes.render import ColorTemplate, SvgRenderer

DEFAULT_CYCLE_LENGTH = 50  # seconds


def generate_single_group_program_ranges(
    cycle_length, group_name, group_type, group_start_on_green, group_slider_positions
):
    return [
        group_name,
        {
            "red": [
                [0, group_slider_positions[0]],
                [group_slider_positions[1], cycle_length],
            ],
            "green": [[group_slider_positions[0], group_slider_positions[1]]],
        }
        if not group_start_on_green
        else {
            "green": [
                [0, group_slider_positions[0]],
                [group_slider_positions[1], cycle_length],
            ],
            "red": [[group_slider_positions[0], group_slider_positions[1]]],
        },
    ]


class GroupElement(html.Div):
    def __init__(self, id: str, cycle_length: int):
        super(GroupElement, self).__init__(
            [
                # TODO: "Group name",
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
        [
            Input("add_group_button", "n_clicks"),
            Input("cycle_length", "value"),
        ],
        [State("group_sliders", "children")],
    )
    def update_group_elements(add_group_n_clicks, cycle_length, group_elements):
        def add_group(group_elements, id_number):
            group_elements.append(GroupElement(f"group-{id_number}", cycle_length))
            return group_elements

        def set_cycle_length(group_elements, cycle_length):
            def set_slider_length(slider, max):
                slider["props"]["max"] = max
                slider["props"]["marks"] = {i: str(i) for i in range(cycle_length)}

            sliders = [
                element["props"]["children"][3]["props"]["children"]
                for element in group_elements
            ]
            for slider in sliders:
                set_slider_length(slider, cycle_length)
            return group_elements

        triggered_input = dash.callback_context.triggered[0]["prop_id"]
        if triggered_input == "add_group_button.n_clicks" and add_group_n_clicks > 0:
            return add_group(group_elements, id_number=add_group_n_clicks)
        elif triggered_input == "cycle_length.value":
            return set_cycle_length(group_elements, int(cycle_length))
        else:
            return group_elements

    @app.callback(
        Output("slider_stripes", "children"),
        [Input("draw_program_stripes_button", "n_clicks")],
        [State("group_sliders", "children"), State("cycle_length", "value")],
    )
    def render_program_stripes(n_clicks, group_elements, cycle_length):
        cycle_length = int(cycle_length)
        # TODO: render on slider drag (with sliders 'drag_value')
        program_group_signal_ranges = []
        for signalling_group_input in group_elements:
            group_name = signalling_group_input["props"]["children"][0]["props"][
                "value"
            ]
            group_type = signalling_group_input["props"]["children"][1]["props"][
                "value"
            ]
            group_start_on_green = bool(
                signalling_group_input["props"]["children"][2]["props"]["value"]
            )
            group_slider_positions = signalling_group_input["props"]["children"][3][
                "props"
            ]["children"]["props"]["value"]

            program_group_signal_ranges.append(
                generate_single_group_program_ranges(
                    cycle_length,
                    group_name,
                    group_type,
                    group_start_on_green,
                    group_slider_positions,
                )
            )
        template = ColorTemplate(SvgRenderer())
        return format_svg(
            template.render(
                ProgramStripes.from_ranges_list(program_group_signal_ranges)
            )
        )


layout = html.Div(
    [
        html.H1("Stripes"),
        "Program cycle length [s]",
        dcc.Input(
            id="cycle_length", value=DEFAULT_CYCLE_LENGTH, type="number", min=8, step=1
        ),
        html.Div(),
        html.Button("Add group", id="add_group_button", n_clicks=0),
        html.Div(
            children=[GroupElement("group-0", DEFAULT_CYCLE_LENGTH)], id="group_sliders"
        ),
        html.Button("Draw program", id="draw_program_stripes_button", n_clicks=0),
        html.Div(id="slider_stripes"),
    ]
)
