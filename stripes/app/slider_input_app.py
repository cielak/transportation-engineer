import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from stripes.app.formatters import format_svg
from stripes.models import ProgramStripes
from stripes.render import ColorTemplate, SvgRenderer


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
                    ),
                ),
            ],
            id=id,
        )


def add_callbacks(app):
    pass


layout = html.Div(
    [
        html.H1("Stripes"),
        html.Button("Add group", id="add_group_button", n_clicks=0),
        html.Div(GroupElement("group-0", 50), id="groups_table"),
        html.Button("Draw program", id="draw_program_stripes_button", n_clicks=0),
        html.Div(id="stripes"),
    ]
)
