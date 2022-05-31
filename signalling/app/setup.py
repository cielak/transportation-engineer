import dash
from dash import dash_table as dt
from dash import html

from signalling.app.callbacks import add_callbacks
from signalling.models import CollisionPoint, StreamIntersection, TrafficStream

layout = html.Div(
    [
        html.H1("Signalling"),
        html.H2("Traffic streams"),
        html.Button("Add stream", id="add_stream_button", n_clicks=0),
        dt.DataTable(
            id="streams_table",
            columns=[
                {"name": x, "id": x, "type": "numeric"}
                if not "_id" in x
                else {"name": x, "id": x}
                for x in TrafficStream._fields
            ],
            data=[],
            editable=True,
            row_deletable=True,
        ),
        html.H2("Stream intersections"),
        html.Button(
            "Add stream intersection", id="add_stream_intersection_button", n_clicks=0
        ),
        dt.DataTable(
            id="stream_intersections_table",
            columns=[
                {"name": x, "id": x, "presentation": "dropdown"}
                if "_stream" in x  # TODO: check field type
                else {"name": x, "id": x, "type": "numeric"}
                for x in StreamIntersection._fields
            ],
            data=[],
            editable=True,
            row_deletable=True,
        ),
        html.H2("Streams Collisions"),
        html.Div(
            "Automatically generated from traffic streams and stream intersections"
        ),
        dt.DataTable(
            id="stream_collisions_table",
            columns=[
                {"name": x, "id": x, "presentation": "dropdown"}
                for x in CollisionPoint._fields
            ],
            data=[],
        ),
        html.Div(id="stream_collisions_matrix", children=[]),
        html.H2("Signalling groups"),
        html.Button("Add group", id="add_group_button", n_clicks=0),
        html.Div(id="groups_table", children=[]),
        html.Button(
            "Refresh groups intergreen times",
            id="refresh_groups_intergreen_matrix_button",
            n_clicks=0,
        ),
        html.Div(id="groups_intergreen_matrix", children=[]),
    ]
)


# TODO: allow group removal
