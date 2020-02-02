import pytest
from unittest.mock import patch

from stripes.models import SecondType, GroupStripe


class TestModels:
    def test_group_stipe(self):
        gs = GroupStripe.from_ranges_dict(
            "K1",
            {
                "off": [(10, 15), (20, 25)],
                "red": [(0, 10)],
                "green": [(16, 17), (25, 30)],
            },
        )
        assert (
            gs.seconds
            == [SecondType.red] * 10
            + [SecondType.off] * 5
            + [SecondType.green] * 1
            + [SecondType.off] * 5
            + [SecondType.green] * 5
        )
