"""Tour operator commission seasons.

SAMO stores a season as dd.mm without a year, so a season that crosses New
Year has to be entered as two records: 01.10–31.12 and 01.01–31.03.
"""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Season:
    start: tuple[int, int]  # (day, month)
    end: tuple[int, int]
    percent: float

    def contains(self, d: date) -> bool:
        key = (d.month, d.day)
        return (self.start[1], self.start[0]) <= key <= (self.end[1], self.end[0])

    def label(self) -> str:
        return f"{self.start[0]:02d}.{self.start[1]:02d}–{self.end[0]:02d}.{self.end[1]:02d}"


def split_over_new_year(start: tuple[int, int], end: tuple[int, int], percent: float) -> list[Season]:
    """Return the records to enter in SAMO for one commercial season."""
    if (start[1], start[0]) <= (end[1], end[0]):
        return [Season(start, end, percent)]
    return [Season(start, (31, 12), percent), Season((1, 1), end, percent)]


def commission_for(seasons: list[Season], d: date) -> float:
    for s in seasons:
        if s.contains(d):
            return s.percent
    raise LookupError(f"Нет комиссии туроператора на {d:%d.%m.%Y}")
