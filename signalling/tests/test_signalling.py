import pytest

from signalling.logic import intergreen_time, groups_intergreen_times
from signalling.models import TrafficStream, StreamIntersection


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
    def groups(self):
        return set()

    @pytest.fixture
    def collisions(self):
        return set()
    
    @pytest.mark.parametrize(
        "evac_yellow_time, evac_time, arr_time, intergreen",
        [[0, 0, 0, 0], [3, 9.5, 0.1, 13], [0, 0, 12, 0]],
    )
    def test_intergreen_time(self, evac_yellow_time, evac_time, arr_time, intergreen):
        assert intergreen_time(evac_yellow_time, evac_time, arr_time) == intergreen

    def test_groups_intergreen_times(self, groups, collisions):
        intergreens = groups_intergreen_times(groups, collisions)
        assert intergreens == []
