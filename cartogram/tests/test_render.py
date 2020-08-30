from unittest import mock
from unittest.mock import call

from cartogram.models import TrafficVolumes, TrafficVolume
from cartogram.render import CartogramTemplate


class TestCartogramTemplate:
    def test_four_way(self):
        traffic_volumes = TrafficVolumes(
            [
                TrafficVolume("A", "A", 0),
                TrafficVolume("A", "B", 1),
                TrafficVolume("A", "C", 2),
                TrafficVolume("A", "D", 5),
                TrafficVolume("B", "A", 3),
                TrafficVolume("B", "B", 1),
                TrafficVolume("B", "C", 7),
                TrafficVolume("B", "D", 9),
                TrafficVolume("C", "A", 8),
                TrafficVolume("C", "B", 2),
                TrafficVolume("C", "C", 3),
                TrafficVolume("C", "D", 1),
                TrafficVolume("D", "A", 4),
                TrafficVolume("D", "B", 5),
                TrafficVolume("D", "C", 5),
                # TrafficVolume from D to D intentionally left missing
            ]
        )
        mocked_drawing = mock.MagicMock()
        CartogramTemplate(mocked_drawing).draw(traffic_volumes)
        assert mocked_drawing.method_calls == [
            call.text(0, 0, "A"),
            call.text(1, 0, "0"),
            call.text(2, 0, "A"),
            call.text(0, 0, "A"),
            call.text(1, 0, "1"),
            call.text(2, 0, "B"),
            call.text(0, 0, "B"),
            call.text(1, 0, "1"),
            call.text(2, 0, "B"),
            call.text(0, 0, "C"),
            call.text(1, 0, "1"),
            call.text(2, 0, "D"),
            call.text(0, 0, "A"),
            call.text(1, 0, "2"),
            call.text(2, 0, "C"),
            call.text(0, 0, "C"),
            call.text(1, 0, "2"),
            call.text(2, 0, "B"),
            call.text(0, 0, "B"),
            call.text(1, 0, "3"),
            call.text(2, 0, "A"),
            call.text(0, 0, "C"),
            call.text(1, 0, "3"),
            call.text(2, 0, "C"),
            call.text(0, 0, "D"),
            call.text(1, 0, "4"),
            call.text(2, 0, "A"),
            call.text(0, 0, "A"),
            call.text(1, 0, "5"),
            call.text(2, 0, "D"),
            call.text(0, 0, "D"),
            call.text(1, 0, "5"),
            call.text(2, 0, "B"),
            call.text(0, 0, "D"),
            call.text(1, 0, "5"),
            call.text(2, 0, "C"),
            call.text(0, 0, "B"),
            call.text(1, 0, "7"),
            call.text(2, 0, "C"),
            call.text(0, 0, "C"),
            call.text(1, 0, "8"),
            call.text(2, 0, "A"),
            call.text(0, 0, "B"),
            call.text(1, 0, "9"),
            call.text(2, 0, "D"),
        ]
