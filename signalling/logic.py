import typing as t
from itertools import product
from math import ceil


class TrafficStream:
    evacuation_velocity = int
    arrival_velocity = int
    evacuation_yellow_time = int
    vehicle_length = int

    def intersects(self, other_stream):
        raise NotImplementedError


class CollisionPoint:
    @property
    def evacuation_time(self) -> float:
        raise NotImplementedError

    @property
    def arrival_time(self) -> float:
        raise NotImplementedError

    @property
    def evacuation_yellow_time(self) -> int:
        raise NotImplementedError


class SignallingGroup:
    name = str


class SignallingPhase:
    green_groups = set
    red_groups = set

    @property
    def saturation_level(self):
        raise NotImplementedError


class PhaseTransition:
    in_phase = SignallingPhase
    out_phase = SignallingPhase

    @property
    def minimal_duration(self):
        return interphase_min_time(self.in_phase, self.out_phase)


class SignallingProgram:
    groups = t.Set[SignallingGroup]
    phases = t.Set[SignallingPhase]
    phase_transitions = t.Set[PhaseTransition]


def intergreen_time(
    evacuating_yellow_time: int, evacuation_time: float, arrival_time: float
) -> int:
    intergreen_time = evacuating_yellow_time + evacuation_time - arrival_time
    return ceil(intergreen_time) if intergreen_time > 0 else 0


def stream_intergreen_time(evacuating_stream, arriving_stream):
    collision_point = evacuating_stream.intersects(arriving_stream)
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


def interphase_min_time(in_phase, out_phase):
    evacuating_groups = in_phase.green_groups.intersection(out_phase.red_groups)
    arriving_groups = in_phase.red_groups.intersection(out_phase.green_groups)
    return max(
        group_intergreen_time(evacuating, arriving)
        for (evacuating, arriving) in product(evacuating_groups, arriving_groups)
    )
