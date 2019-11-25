import typing as t


class StreamIntersection(t.NamedTuple):
    evacuating_stream: "TrafficStream"
    evacuation_distance: float
    arriving_stream: "TrafficStream"
    arrival_distance: float

    def inverted(self):
        return StreamIntersection(
            self.arriving_stream,
            self.arrival_distance,
            self.evacuating_stream,
            self.evacuation_distance,
        )


class TrafficStream(t.NamedTuple):
    stream_id: str
    evacuation_velocity: int
    arrival_velocity: int
    evacuating_yellow_time: int
    vehicle_length: int


class CollisionPoint(t.NamedTuple):
    evacuating_stream: TrafficStream
    evacuation_time: float
    arriving_stream: TrafficStream
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
