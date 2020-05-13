from unittest.mock import MagicMock

import pytest

from stripes.models import GroupStripe, SecondType, ProgramStripes
from stripes.render import ColorTemplate, SvgRenderer


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


class TestRender:
    def test_color_template(self):
        template = ColorTemplate(
            MagicMock(),
            annotate_greens=True,
            left_offset=5,
            right_offset=5,
            annotations=[(-2, "Faza 1"), (0, "PF 1-2"), (23, "Faza 2")],
        )
        formatted_rows = [
            [
                "K1",
                {
                    "off": [[0, 5]],
                    "yellow": [[5, 10], [50, 53]],
                    "red": [[10, 30], [53, 60]],
                    "red_yellow": [[30, 31]],
                    "green": [[31, 50]],
                },
            ],
            [
                "P1",
                {
                    "off": [[0, 5]],
                    "yellow": [[5, 10], [50, 53]],
                    "red": [[10, 30], [53, 60]],
                    "red_yellow": [[30, 31]],
                    "green": [[31, 50]],
                },
            ],
        ]
        program_stripes = ProgramStripes.from_ranges_list(formatted_rows)
        template.render(program_stripes)
