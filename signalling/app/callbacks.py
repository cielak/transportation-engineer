from collections import OrderedDict

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt

from signalling.app import formatters, validators
from signalling.logic import intersect_traffic_streams, collision_intergreen_time


def add_callbacks(app):
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
        dash.dependencies.Output("stream_collisions_matrix", "children"),
        [
            dash.dependencies.Input("streams_table", "data_timestamp"),
            dash.dependencies.Input("stream_intersections_table", "data_timestamp"),
        ],
        [
            dash.dependencies.State("streams_table", "data"),
            dash.dependencies.State("stream_intersections_table", "data"),
        ],
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
        columns = [{"name": "evac\\arr", "id": "evac\\arr"}]
        data = OrderedDict()
        for s in streams:
            columns.append({"name": s.stream_id, "id": s.stream_id})
            data[s.stream_id] = {"evac\\arr": s.stream_id}
        for c in collisions:
            data[c.evacuating_stream.stream_id].update(
                {c.arriving_stream.stream_id: collision_intergreen_time(c)}
            )
        return [dt.DataTable(columns=columns, data=list(data.values()))]

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
