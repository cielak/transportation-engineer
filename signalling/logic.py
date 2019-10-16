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


class IntergreenPair:
    def __init__(self, evacuating, arriving, intergreen_time):
        raise NotImplementedError


def intergreen_time(
    evacuating_yellow_time: int, evacuation_time: float, arrival_time: float
) -> int:
    intergreen_time = evacuating_yellow_time + evacuation_time - arrival_time
    return ceil(intergreen_time) if intergreen_time > 0 else 0


def all_intergreen_pairs(
    collision_pairs: t.Iterable[CollisionPair]
) -> t.Iterable[IntergreenPair]:
    for collision_pair in collision_pairs:
        for evacuating, arriving in [collision_pair, collision_pair.inverted()]:
            yield IntergreenPair(
                evacuating,
                arriving,
                intergreen_time(
                    evacuating.yellow_time,
                    evacuating.time_evacuation,
                    arriving.time_arrival,
                ),
            )
