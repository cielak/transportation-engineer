import pytest

from stripes.models import GroupStripe, SecondType


class TestModels:
    def test_group_stripe(self):
        gs = GroupStripe.from_ranges_dict(
            "K1",
            {
                "off": [(10, 15), (17, 25)],
                "red": [(0, 10)],
                "green": [(15, 17), (25, 30)],
            },
        )
        assert len(gs.seconds) == 30
        assert (
            gs.seconds
            == [SecondType.red] * 10
            + [SecondType.off] * 5
            + [SecondType.green] * 2
            + [SecondType.off] * 8
            + [SecondType.green] * 5
        )

    @pytest.mark.parametrize("red_start, red_stop", [[0, 9], [1, 10]])
    def test_group_stripe_invalid(self, red_start, red_stop):
        with pytest.raises(ValueError):
            GroupStripe.from_ranges_dict(
                "T1", {"red": [(red_start, red_stop)], "green": [(10, 20)]}
            )
