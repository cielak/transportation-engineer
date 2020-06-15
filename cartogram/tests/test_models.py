from cartogram.models import TrafficVolume, TrafficVolumes


class TestModels:
    def test_traffic_matrix(self):
        traffic_volumes = [
            TrafficVolume("A", "B", 1),
            TrafficVolume("A", "C", 2),
            TrafficVolume("A", "D", 5),
            TrafficVolume("B", "A", 3),
            TrafficVolume("B", "C", 7),
            TrafficVolume("B", "D", 9),
            TrafficVolume("C", "A", 8),
            TrafficVolume("C", "B", 2),
            TrafficVolume("C", "D", 1),
            TrafficVolume("D", "A", 4),
            TrafficVolume("D", "B", 5),
            TrafficVolume("D", "C", 5),
        ]
        traffic_matrix = TrafficVolumes(traffic_volumes)
        assert traffic_matrix.sorted_relations == [
            TrafficVolume("A", "B", 1),
            TrafficVolume("C", "D", 1),
            TrafficVolume("A", "C", 2),
            TrafficVolume("C", "B", 2),
            TrafficVolume("B", "A", 3),
            TrafficVolume("D", "A", 4),
            TrafficVolume("A", "D", 5),
            TrafficVolume("D", "B", 5),
            TrafficVolume("D", "C", 5),
            TrafficVolume("B", "C", 7),
            TrafficVolume("C", "A", 8),
            TrafficVolume("B", "D", 9),
        ]
