import pytest

from signalling.logic import (
    groups_intergreen_times,
    intergreen_time,
    intersect_traffic_streams,
)
from signalling.models import (
    GroupIntergreen,
    SignallingGroup,
    StreamIntersection,
    TrafficStream,
)


class TestModels:
    def test_intersection_inverts(self):
        ts1 = TrafficStream("ts1", 1, 1, 1, 1)
        ts1_dist = 1
        ts2 = TrafficStream("ts2", 2, 2, 2, 2)
        ts2_dist = 2
        si = StreamIntersection(ts1, ts1_dist, ts2, ts2_dist)
        assert si.inverted() == StreamIntersection(ts2, ts2_dist, ts1, ts1_dist)


class TestLogic:
    @pytest.fixture
    def stream_k(self):
        return TrafficStream("K1", 10, 14, 3, 10)

    @pytest.fixture
    def stream_p(self):
        return TrafficStream("P1", 1.4, 1, 0, 0)

    @pytest.fixture
    def groups(self, stream_k, stream_p):
        return [
            SignallingGroup(name="K", streams=set([stream_k])),
            SignallingGroup(name="P", streams=set([stream_p])),
        ]

    @pytest.fixture
    def stream_intersections(self, stream_k, stream_p):
        return set(
            StreamIntersection(stream_k, k, stream_p, p)
            for k, p in [(2, 0), (2, 6), (8, 0), (8, 6)]
        )

    @pytest.mark.parametrize(
        "evac_yellow_time, evac_time, arr_time, intergreen",
        [[0, 0, 0, 0], [3, 9.5, 0.1, 13], [0, 0, 12, 0]],
    )
    def test_intergreen_time(self, evac_yellow_time, evac_time, arr_time, intergreen):
        assert intergreen_time(evac_yellow_time, evac_time, arr_time) == intergreen

    def test_groups_intergreen_times(self, groups, stream_intersections):
        collision_points = intersect_traffic_streams(stream_intersections)
        intergreens = sorted(groups_intergreen_times(groups, collision_points))
        assert intergreens == [
            GroupIntergreen(groups[0], groups[1], 5),
            GroupIntergreen(groups[1], groups[0], 5),
        ]
