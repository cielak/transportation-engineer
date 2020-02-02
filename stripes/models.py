from enum import Enum
import typing as t


# SecondType = Enum(
#    "SecondType", "off red red_yellow green yellow green_blinking yellow_blinking"
# )


class SecondType(Enum):
    off = "off"
    red = "red"
    red_yellow = "red_yellow"
    green = "green"
    yellow = "yellow"
    green_blinking = "green_blinking"
    yellow_blinking = "yellow_blinking"


class SecondsRange(t.NamedTuple):
    type: SecondType
    start: int
    stop: int


class GroupStripe(t.NamedTuple):
    name: str
    seconds: t.List[SecondType]

    @classmethod
    def from_ranges(cls, name, ranges: t.List[SecondsRange]):
        sorted_ranges = sorted(ranges, key=lambda x: x.start)
        seconds = []
        for r in sorted_ranges:
            seconds.extend([r.type for _ in range(r.stop - r.start)])
        return cls(name, seconds)

    @classmethod
    def from_ranges_dict(cls, name, data: dict):
        ranges = []
        for type_name, ranges_list in data.items():
            type = SecondType(type_name)
            for raw_range in ranges_list:
                ranges.append(SecondsRange(type, *raw_range))
        return cls.from_ranges(name, ranges)


class ProgramStripes(t.NamedTuple):
    groups: t.List[GroupStripe]
