import typing as t


class TrafficStream(t.NamedTuple):
    evacuation_velocity: int
    arrival_velocity: int
    evacuation_yellow_time: int
    vehicle_length: int


class CollisionPoint(t.NamedTuple):
    evacuation_time: float
    arrival_time: float


class SignallingGroup(t.NamedTuple):
    name: str
    streams: t.Set[TrafficStream]


class SignallingPhase(t.NamedTuple):
    green_groups: set
    red_groups: set


class PhaseTransition(t.NamedTuple):
    in_phase: SignallingPhase
    out_phase: SignallingPhase


class SignallingProgram(t.NamedTuple):
    groups: t.Set[SignallingGroup]
    phases: t.Set[SignallingPhase]
    phase_transitions: t.Set[PhaseTransition]
