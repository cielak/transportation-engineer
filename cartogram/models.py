import typing as t
from dataclasses import dataclass


@dataclass
class TrafficVolume:
    in_name: str
    out_name: str
    value: int


@dataclass
class TrafficVolumes:
    volumes: t.Iterable[TrafficVolume]

    @property
    def sorted_relations(self):
        return sorted(self.volumes, key=lambda x: (x.value, x.in_name, x.out_name))
