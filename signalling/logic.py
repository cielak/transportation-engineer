import typing as t
from math import ceil


class SignallingGroup:
    name = str


class CollisionElement:
    @property
    def evacuation_time(self) -> float:
        raise NotImplementedError

    @property
    def arrival_time(self) -> float:
        raise NotImplementedError

    @property
    def evacuation_yellow_time(self) -> int:
        raise NotImplementedError


class IntergreenElement:
    pass


class CollisionPair:
    a = CollisionElement
    b = CollisionElement

    @property
    def elements(self) -> t.Tuple[t.Type[CollisionElement], t.Type[CollisionElement]]:
        return self.a, self.b

    @property
    def inverted_elements(
        self
    ) -> t.Tuple[t.Type[CollisionElement], t.Type[CollisionElement]]:
        return self.b, self.a


class IntergreenPair:
    evacuating = IntergreenElement
    arriving = IntergreenElement
    intergreen_time = int

    def __init__(self, evacuating, arriving, intergreen_time):
        raise NotImplementedError


def intergreen_time(
    evacuating_yellow_time: int, evacuation_time: float, arrival_time: float
) -> int:
    intergreen_time = evacuating_yellow_time + evacuation_time - arrival_time
    return ceil(intergreen_time) if intergreen_time > 0 else 0


def stream_intergreen_time(evacuating_stream, arriving_stream):
    collision_point = evacuating_stream.intercests(arriving_stream)
    if not collision_point:
        return None
    return intergree_time(
        evacuating_stream.evacuating_yellow_time,
        collision_point.evacuating_time,
        collision_point.arriving_time,
    )


def group_intergreen_time(evacuating_group, arriving_group):
    if evacuating_group == arriving_group:
        return None
    else:
        stream_intergreen_times = []
        for evacuating_stream in evacuating_group.streams:
            for arriving_stream in arriving_group.streams:
                stream_intergreen_times.append(
                    stream_intergreen_time(evacuating_stream, arriving_stream)
                )
        return max(stream_intergreen_times)


def intergreen_times(signalling_groups):
    for group in signalling_groups:
        for other_group in signalling_groups:
            yield IntergreenPair(
                group, other_group, group_intergreen_time(group, other_group)
            )


def interphase_min_time(in_phase, out_phase):
    evacuating_groups = intersection(in_phase.green_groups, out_phase.red_groups)
    arriving_groups = intersection(in_phase.red_groupa, out_phase.green_groups)
    return max(
        group_intergreen_time(evacuating, incoming)
        for (evacuating, arriving) in permutation(evacuating_groups, arriving_groups)
    )
