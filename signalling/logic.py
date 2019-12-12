import typing as t
from itertools import product
from math import ceil

from signalling.models import (
    TrafficStream,
    CollisionPoint,
    SignallingPhase,
    SignallingGroup,
    StreamIntersection,
)


def intergreen_time(
    evacuating_yellow_time: int, evacuation_time: float, arrival_time: float
) -> int:
    raw_intergreen_time = evacuating_yellow_time + evacuation_time - arrival_time
    return ceil(raw_intergreen_time) if raw_intergreen_time > 0 else 0


def evacuation_time(stream_intersection: StreamIntersection) -> float:
    return (
        stream_intersection.evacuation_distance
        + stream_intersection.evacuating_stream.vehicle_length
    ) / stream_intersection.evacuating_stream.evacuation_velocity


def arrival_time(stream_intersection: StreamIntersection) -> float:
    return (
        stream_intersection.arrival_distance
        / stream_intersection.arriving_stream.arrival_velocity
    )


def intersect_traffic_streams(
    stream_intersections: t.Set[StreamIntersection],
) -> t.Union[CollisionPoint, None]:
    return [
        CollisionPoint(
            evacuating_stream=intersection.evacuating_stream,
            evacuation_time=evacuation_time(intersection),
            arriving_stream=intersection.arriving_stream,
            arrival_time=arrival_time(intersection),
        )
        for intersection in (
            list(stream_intersections) + [s.inverted() for s in stream_intersections]
        )
    ]


def stream_intergreen_time(
    evacuating_stream: TrafficStream, arriving_stream: TrafficStream
) -> t.Union[int, None]:
    collision_point = intersect_traffic_streams(evacuating_stream, arriving_stream)
    if not collision_point:
        return None
    return intergreen_time(
        evacuating_stream.evacuating_yellow_time,
        collision_point.evacuation_time,
        collision_point.arrival_time,
    )


def group_intergreen_time(
    evacuating_group: SignallingGroup, arriving_group: SignallingGroup
) -> t.Union[int, None]:
    if evacuating_group == arriving_group:
        return None
    else:
        return max(
            stream_intergreen_time(evacuating_stream, arriving_stream)
            for evacuating_stream, arriving_stream in product(
                evacuating_group.streams, arriving_group.streams
            )
        )


def required_interphase_time(
    in_phase: SignallingPhase, out_phase: SignallingPhase
) -> int:
    evacuating_groups = in_phase.green_groups.intersection(out_phase.red_groups)
    arriving_groups = in_phase.red_groups.intersection(out_phase.green_groups)
    return max(
        group_intergreen_time(evacuating, arriving)
        for (evacuating, arriving) in product(evacuating_groups, arriving_groups)
    )
