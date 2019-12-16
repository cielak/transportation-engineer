import typing as t

from signalling.models import (
    TrafficStream,
    StreamIntersection,
    CollisionPoint,
    SignallingGroup,
)


def read_traffic_streams(streams_data):
    return set(TrafficStream(**x) for x in streams_data)


def read_stream_intersections(intersections_data, streams):
    updated_intersections_data = intersections_data.copy()
    for s in updated_intersections_data:
        e_id = s["evacuating_stream"]
        a_id = s["arriving_stream"]
        e_stream = [x for x in streams if x.stream_id == e_id][0]
        a_stream = [x for x in streams if x.stream_id == a_id][0]
        s["evacuating_stream"] = e_stream
        s["arriving_stream"] = a_stream
    return set(StreamIntersection(**x) for x in updated_intersections_data)


def return_collision_point(collision_point: CollisionPoint) -> dict:
    return {
        **collision_point._asdict(),
        **{
            "evacuating_stream": collision_point.evacuating_stream.stream_id,
            "arriving_stream": collision_point.arriving_stream.stream_id,
        },
    }


def read_collision_points(collisions_rows) -> t.Set[CollisionPoint]:
    return set(CollisionPoint(**c) for c in collisions_rows)


def read_signalling_groups(
    signalling_groups_rows, traffic_streams_rows
) -> t.List[SignallingGroup]:
    streams = read_traffic_streams(traffic_streams_rows)
    return [
        SignallingGroup(
            name=g["props"]["children"][0]["props"]["value"],
            streams=set(
                s
                for s in streams
                if s.stream_id in g["props"]["children"][1]["props"]["value"]
            ),
        )
        for g in signalling_groups_rows
    ]
