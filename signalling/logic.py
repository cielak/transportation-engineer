import typing as t
from math import ceil


class CollisionElement:
    @property
    def evacuation_time(self) -> float:
        raise NotImplementedError

    @property
    def arrival_time(self) -> float:
        raise NotImplementedError

    @property
    def evacuation_yellow_time(self) -> int:
        raise NotImplementedError


class IntergreenElement:
    pass


class CollisionPair:
    a = CollisionElement
    b = CollisionElement

    @property
    def elements(self) -> t.Tuple[t.Type[CollisionElement], t.Type[CollisionElement]]:
        return self.a, self.b

    @property
    def inverted_elements(
        self
    ) -> t.Tuple[t.Type[CollisionElement], t.Type[CollisionElement]]:
        return self.b, self.a


class IntergreenPair:
    evacuating = IntergreenElement
    arriving = IntergreenElement
    intergreen_time = int

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
        for evacuating, arriving in [
            collision_pair.elements,
            collision_pair.inverted_elements,
        ]:
            yield IntergreenPair(
                evacuating,
                arriving,
                intergreen_time(
                    evacuating.evacuation_yellow_time,
                    evacuating.evacuation_time,
                    arriving.arrival_time,
                ),
            )
