import typing as t
from itertools import product
from math import ceil

from signalling.models import TrafficStream, CollisionPoint


def intergreen_time(
    evacuating_yellow_time: int, evacuation_time: float, arrival_time: float
) -> int:
    raw_intergreen_time = evacuating_yellow_time + evacuation_time - arrival_time
    return ceil(raw_intergreen_time) if raw_intergreen_time > 0 else 0


def intersect_traffic_streams(
    stream1: TrafficStream, stream2: TrafficStream
) -> t.Union[CollisionPoint, None]:
    raise NotImplementedError


def stream_intergreen_time(evacuating_stream, arriving_stream):
    collision_point = intersect_traffic_streams(evacuating_stream, arriving_stream)
    if not collision_point:
        return None
    return intergreen_time(
        evacuating_stream.evacuating_yellow_time,
        collision_point.evacuation_time,
        collision_point.arrival_time,
    )


def group_intergreen_time(evacuating_group, arriving_group):
    if evacuating_group == arriving_group:
        return None
    else:
        return max(
            stream_intergreen_time(evacuating_stream, arriving_stream)
            for evacuating_stream, arriving_stream in product(
                evacuating_group.streams, arriving_group.streams
            )
        )


def required_interphase_time(in_phase, out_phase):
    evacuating_groups = in_phase.green_groups.intersection(out_phase.red_groups)
    arriving_groups = in_phase.red_groups.intersection(out_phase.green_groups)
    return max(
        group_intergreen_time(evacuating, arriving)
        for (evacuating, arriving) in product(evacuating_groups, arriving_groups)
    )
