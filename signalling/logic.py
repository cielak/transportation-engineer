import typing as t
from math import ceil


class CollisionElement:
    @property
    def evacuation_time(self):
        raise NotImplementedError

    @property
    def arrival_time(self):
        raise NotImplementedError


class UnorderedPair:
    def inverted(self):
        raise NotImplementedError


class CollisionPair(CollisionElement, UnorderedPair):
    pass


class IntergreenPair(UnorderedPair):
    pass


def _intergreen_time(x: float, y: float) -> float:
    pass


def _standardized_intergreen_time(x: float, y: float) -> int:
    intergreen_time = _intergreen_time(x, y)
    return ceil(intergreen_time) if intergreen_time > 0 else 0


def all_intergreen_pairs(collision_pairs: t.Iterable[CollisionPair]) -> t.Iterable[IntergreenPair]:
    ret = []
    for collision_pair in collision_pairs:
        for evacuating, arriving in [collision_pair, collision_pair.inverted()]:
            ret.append(evacuating.yellow_time + evacuating.time_evacuation - arriving.time_arrival)
    return ret
