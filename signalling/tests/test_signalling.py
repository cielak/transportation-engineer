import pytest

from signalling.logic import intergreen_time


class TestLogic:
    @pytest.mark.parametrize(
        "evac_yellow_time, evac_time, arr_time, intergreen",
        [[0, 0, 0, 0], [3, 10, 0, 13]],
    )
    def test_intergreen_time(self, evac_yellow_time, evac_time, arr_time, intergreen):
        assert intergreen_time(evac_yellow_time, evac_time, arr_time) == intergreen
