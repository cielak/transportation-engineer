import pytest
from dash import dcc, html

from stripes.app.slider_input_app import (
    DEFAULT_CYCLE_LENGTH,
    GroupElement,
    read_single_group,
)


@pytest.fixture
def dafault_first_group_id():
    return "group-0"


@pytest.fixture
def default_group_element() -> dict:
    return html.Div(
        children=[
            dcc.Input(id="group-0-name", value="group-0"),
            dcc.Dropdown(
                id="group-0-type",
                options=[{"label": "K", "value": "K"}, {"label": "P", "value": "P"}],
                value="K",
            ),
            dcc.Checklist(
                id="group-0-inverted",
                options=[{"label": "start on green", "value": "inverted"}],
                value=[],
            ),
            html.Div(
                dcc.RangeSlider(
                    id="group-0-range",
                    className="default-signalling-slider",
                    marks={
                        0: "0",
                        1: "1",
                        2: "2",
                        3: "3",
                        4: "4",
                        5: "5",
                        6: "6",
                        7: "7",
                        8: "8",
                        9: "9",
                        10: "10",
                        11: "11",
                        12: "12",
                        13: "13",
                        14: "14",
                        15: "15",
                        16: "16",
                        17: "17",
                        18: "18",
                        19: "19",
                        20: "20",
                        21: "21",
                        22: "22",
                        23: "23",
                        24: "24",
                        25: "25",
                        26: "26",
                        27: "27",
                        28: "28",
                        29: "29",
                        30: "30",
                        31: "31",
                        32: "32",
                        33: "33",
                        34: "34",
                        35: "35",
                        36: "36",
                        37: "37",
                        38: "38",
                        39: "39",
                        40: "40",
                        41: "41",
                        42: "42",
                        43: "43",
                        44: "44",
                        45: "45",
                        46: "46",
                        47: "47",
                        48: "48",
                        49: "49",
                    },
                    max=50,
                    min=0,
                    step=1,
                    value=[1, 25],
                )
            ),
        ],
        id="group-0",
    )


def test_program_has_50_seconds_by_default():
    assert DEFAULT_CYCLE_LENGTH == 50


def test_group_element_layout(dafault_first_group_id, default_group_element):
    group_element = GroupElement(dafault_first_group_id, DEFAULT_CYCLE_LENGTH)
    assert str(group_element) == str(default_group_element)
