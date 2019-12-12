import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html

from signalling.models import (
    SignallingGroup,
    TrafficStream,
    StreamIntersection,
    CollisionPoint,
)
from signalling.logic import intersect_traffic_streams

app = dash.Dash(__name__)

app.title = "Transportation Engineer"
app.layout = html.Div(
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
        html.H2("Signalling groups"),
        html.Button("Add group", id="add_group_button", n_clicks=0),
        html.Div(id="groups_table", children=[]),
    ]
)


@app.callback(
    dash.dependencies.Output("streams_table", "data"),
    [dash.dependencies.Input("add_stream_button", "n_clicks")],
    [
        dash.dependencies.State("streams_table", "data"),
        dash.dependencies.State("streams_table", "columns"),
    ],
)
def add_stream(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c["id"]: "" for c in columns})
    return rows


@app.callback(
    dash.dependencies.Output("stream_intersections_table", "data"),
    [dash.dependencies.Input("add_stream_intersection_button", "n_clicks")],
    [
        dash.dependencies.State("stream_intersections_table", "data"),
        dash.dependencies.State("stream_intersections_table", "columns"),
    ],
)
def add_stream_intersection(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c["id"]: "" for c in columns})
    return rows


@app.callback(
    dash.dependencies.Output("stream_intersections_table", "dropdown"),
    [dash.dependencies.Input("streams_table", "data_timestamp")],
    [dash.dependencies.State("streams_table", "data")],
)
def set_available_streams_for_stream_intersections(timestamp, rows):
    vals = [x["stream_id"] for x in rows]
    options = {"options": [{"label": i, "value": i} for i in vals]}
    dropdown = {"arriving_stream": options, "evacuating_stream": options}
    return dropdown


@app.callback(
    dash.dependencies.Output("stream_collisions_table", "data"),
    [
        dash.dependencies.Input("streams_table", "data_timestamp"),
        dash.dependencies.Input("stream_intersections_table", "data_timestamp"),
    ],
    [
        dash.dependencies.State("streams_table", "data"),
        dash.dependencies.State("stream_intersections_table", "data"),
    ],
)
def set_stream_intersections_data(_1, _2, streams_data, intersections_data):
    streams = set(TrafficStream(**x) for x in streams_data)
    if not all(
        all([cell != "" for cell in row.values()]) for row in intersections_data
    ) or not all(all([cell != "" for cell in row.values()]) for row in streams_data):
        return []
    updated_intersections_data = intersections_data.copy()
    for s in updated_intersections_data:
        e_id = s["evacuating_stream"]
        a_id = s["arriving_stream"]
        e_stream = [x for x in streams if x.stream_id == e_id][0]
        a_stream = [x for x in streams if x.stream_id == a_id][0]
        s["evacuating_stream"] = e_stream
        s["arriving_stream"] = a_stream
    intersections = set(StreamIntersection(**x) for x in updated_intersections_data)
    return sorted(
        [pt._asdict() for pt in intersect_traffic_streams(intersections)],
        key=lambda x: (x["evacuating_stream"], x["arriving_stream"]),
    )


@app.callback(
    dash.dependencies.Output("groups_table", "children"),
    [dash.dependencies.Input("add_group_button", "n_clicks")],
    [
        dash.dependencies.State("groups_table", "children"),
        dash.dependencies.State("streams_table", "data"),
    ],
)
def add_group(n_clicks, groups_rows, streams_rows):
    if n_clicks > 0:
        vals = [x["stream_id"] for x in streams_rows]
        options = [{"label": i, "value": i} for i in vals]
        groups_rows.append(
            html.Div(
                children=[
                    dcc.Input(id="group_id"),
                    dcc.Dropdown(
                        id="group_streams", options=options, value=[], multi=True
                    ),
                ]
            )
        )
    return groups_rows


# TODO: allow group removal
