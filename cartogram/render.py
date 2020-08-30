from cartogram.models import TrafficVolumes, TrafficVolume


class DrawingInterface:
    def text(self, pox_x, pos_y, text: str):
        raise NotImplementedError


class CartogramTemplate:
    def __init__(self, drawing: DrawingInterface):
        self.dwg = drawing

    def draw_relation(self, relation: TrafficVolume):
        self.dwg.text(0, 0, relation.in_name)
        self.dwg.text(1, 0, str(relation.value))
        self.dwg.text(2, 0, relation.out_name)

    def draw(self, traffic_volumes: TrafficVolumes):
        for relation in traffic_volumes.sorted_relations:
            self.draw_relation(relation)
