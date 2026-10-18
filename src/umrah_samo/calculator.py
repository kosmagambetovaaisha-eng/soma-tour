"""Per-person tour price, computed the way SAMO builds the order."""

from dataclasses import dataclass, field
from datetime import date

from .commission import commission_for
from .rooms import Room
from .tour import Tour


@dataclass
class Quote:
    tour: str
    room: Room
    start: date
    lines: list[tuple[str, float]] = field(default_factory=list)
    commission_percent: float = 0.0

    @property
    def net(self) -> float:
        return round(sum(v for _, v in self.lines), 2)

    @property
    def total(self) -> float:
        return round(self.net * (1 + self.commission_percent / 100), 2)


def quote(
    tour: Tour,
    room: Room,
    start: date,
    with_visa: bool = True,
    addons: tuple[str, ...] = (),
) -> Quote:
    q = Quote(tour.code, room, start)
    q.lines.append((tour.makkah.name, tour.makkah.per_person(room, tour.makkah_nights)))
    q.lines.append((tour.madinah.name, tour.madinah.per_person(room, tour.madinah_nights)))
    q.lines.append((f"{tour.flights.outbound.number}/{tour.flights.inbound.number}", tour.flights.adult))
    q.lines.append(("Гид", tour.guide))
    for s in tour.services:
        if s.included and (s.default or not s.removable):
            if s.name == "Виза" and not with_visa and s.removable:
                continue
            q.lines.append((s.name, s.price))
        elif s.offered and s.name in addons:
            q.lines.append((s.name, s.price))
    q.lines = [(n, round(v, 2)) for n, v in q.lines]
    if tour.commission:
        q.commission_percent = commission_for(tour.commission, start)
    return q
