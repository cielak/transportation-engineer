import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html

from models import SignallingGroup, TrafficStream, StreamIntersection

app = dash.Dash(__name__)

server = app.server

app.title = "Transportation Engineer"
app.layout = html.Div(
    [
        html.H1("Signalling"),
        html.H2("Traffic streams"),
        html.Button("Add stream", id="add_stream_button", n_clicks=0),
        dt.DataTable(
            id="streams_table",
            columns=[{"name": x, "id": x} for x in TrafficStream._fields],
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
                for x in StreamIntersection._fields
            ],
            data=[],
            editable=True,
            row_deletable=True,
        ),
        html.H2("Signalling groups"),
        html.Button("Add group", id="add_group_button", n_clicks=0),
        html.Div(id="groups_table_", children=[]),
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
def add_collision_point(n_clicks, rows, columns):
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
    dash.dependencies.Output("groups_table_", "children"),
    [dash.dependencies.Input("add_group_button", "n_clicks")],
    [
        dash.dependencies.State("groups_table_", "children"),
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
                        id="group_streams", options=options, value=[], multi=True,
                    ),
                ]
            )
        )
    return groups_rows


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
