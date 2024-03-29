from collections import OrderedDict

import dash
from dash import dash_table as dt
from dash import dcc, html
from dash.dependencies import Input, Output, State

from signalling.app import formatters, validators
from signalling.logic import (
    collision_intergreen_time,
    groups_intergreen_times,
    intersect_traffic_streams,
)

HEADER = "evac\\arr"
EMPTY = "X"


def add_callbacks(app):
    @app.callback(
        Output("streams_table", "data"),
        [Input("add_stream_button", "n_clicks")],
        [State("streams_table", "data"), State("streams_table", "columns")],
    )
    def add_stream(n_clicks, rows, columns):
        if n_clicks > 0:
            rows.append({c["id"]: "" for c in columns})
        return rows

    @app.callback(
        Output("stream_intersections_table", "data"),
        [Input("add_stream_intersection_button", "n_clicks")],
        [
            State("stream_intersections_table", "data"),
            State("stream_intersections_table", "columns"),
        ],
    )
    def add_stream_intersection(n_clicks, rows, columns):
        if n_clicks > 0:
            rows.append({c["id"]: "" for c in columns})
        return rows

    @app.callback(
        Output("groups_table", "children"),
        [Input("add_group_button", "n_clicks")],
        [State("groups_table", "children"), State("streams_table", "data")],
    )
    def add_group(n_clicks, groups_rows, streams_rows):
        if n_clicks > 0:
            vals = [x["stream_id"] for x in streams_rows]
            options = [{"label": i, "value": i} for i in vals]
            groups_rows.append(
                html.Div(
                    children=[
                        html.Button(
                            "x",
                            id="remove_group_{}_button".format(n_clicks),
                            n_clicks=0,
                        ),
                        dcc.Input(id="group_id"),
                        dcc.Dropdown(
                            id="group_streams", options=options, value=[], multi=True
                        ),
                    ]
                )
            )
        return groups_rows

    @app.callback(
        Output("stream_intersections_table", "dropdown"),
        [Input("streams_table", "data_timestamp")],
        [State("streams_table", "data")],
    )
    def set_available_streams_for_stream_intersections(timestamp, rows):
        vals = [x["stream_id"] for x in rows]
        options = {"options": [{"label": i, "value": i} for i in vals]}
        dropdown = {"arriving_stream": options, "evacuating_stream": options}
        return dropdown

    @app.callback(
        Output("stream_collisions_table", "data"),
        [
            Input("streams_table", "data_timestamp"),
            Input("stream_intersections_table", "data_timestamp"),
        ],
        [State("streams_table", "data"), State("stream_intersections_table", "data")],
    )
    def set_collisions_data(_1, _2, streams_data, intersections_data):
        if not all(
            (
                validators.all_cells(streams_data),
                validators.all_cells(intersections_data),
            )
        ):
            raise dash.exceptions.PreventUpdate
        streams = formatters.read_traffic_streams(streams_data)
        intersections = formatters.read_stream_intersections(
            intersections_data, streams
        )
        collisions = intersect_traffic_streams(intersections)
        collisions_data = sorted(
            [formatters.return_collision_point(pt) for pt in collisions],
            key=lambda x: (x["evacuating_stream"], x["arriving_stream"]),
        )
        return collisions_data

    @app.callback(
        Output("stream_collisions_matrix", "children"),
        [
            Input("streams_table", "data_timestamp"),
            Input("stream_intersections_table", "data_timestamp"),
        ],
        [State("streams_table", "data"), State("stream_intersections_table", "data")],
    )
    def set_collisions_matrix(_1, _2, streams_data, intersections_data):
        if not all(
            (
                validators.all_cells(streams_data),
                validators.all_cells(intersections_data),
            )
        ):
            raise dash.exceptions.PreventUpdate
        streams = sorted(
            formatters.read_traffic_streams(streams_data), key=lambda x: x.stream_id
        )
        intersections = formatters.read_stream_intersections(
            intersections_data, streams
        )
        collisions = intersect_traffic_streams(intersections)
        columns = [{"name": HEADER, "id": HEADER}]
        data = OrderedDict()
        for stream in streams:
            columns.append({"name": stream.stream_id, "id": stream.stream_id})
            data[stream] = {HEADER: stream.stream_id, stream.stream_id: EMPTY}
        for collision in collisions:
            data[collision.evacuating_stream].update(
                {
                    collision.arriving_stream.stream_id: collision_intergreen_time(
                        collision
                    )
                }
            )
        return [dt.DataTable(columns=columns, data=list(data.values()))]

    @app.callback(
        Output("groups_intergreen_matrix", "children"),
        [
            Input("refresh_groups_intergreen_matrix_button", "n_clicks"),
            Input("stream_collisions_table", "data"),
        ],
        [State("groups_table", "children"), State("streams_table", "data")],
    )
    def set_groups_intergreen_matrix(_, collisions_rows, groups_rows, streams_rows):
        streams = formatters.read_traffic_streams(streams_rows)
        collisions = formatters.read_collision_points(collisions_rows, streams)
        groups = sorted(
            formatters.read_signalling_groups(groups_rows, streams_rows),
            key=lambda x: x.name,
        )
        intergreens = groups_intergreen_times(groups, collisions)
        columns = [{"name": HEADER, "id": HEADER}]
        data = OrderedDict()
        for group in groups:
            columns.append({"name": group.name, "id": group.name})
            data[group.name] = {HEADER: group.name, group.name: EMPTY}
            for i in intergreens:
                if i.arriving_group.name == group.name:
                    data[group.name].update(
                        {i.evacuating_group.name: i.intergreen_time}
                    )
        return [dt.DataTable(columns=columns, data=list(data.values()))]
