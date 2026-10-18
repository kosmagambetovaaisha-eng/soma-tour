"""Check SAMO setup against the «Исправить по всем турам» checklist."""

from dataclasses import dataclass

from .rooms import Room, placement_formula
from .tour import Tour

ROOMS = (Room.SNGL, Room.DBL, Room.TRPL)


@dataclass
class Issue:
    where: str
    what: str

    def __str__(self) -> str:
        return f"[{self.where}] {self.what}"


def check_tour(tour: Tour) -> list[Issue]:
    issues = []
    for hotel in (tour.makkah, tour.madinah):
        for room in ROOMS:
            if room not in hotel.formulas:
                issues.append(Issue(hotel.name, f"добавить формулу {room.value} = {placement_formula(room)}"))
            if room not in hotel.per_person_night:
                issues.append(Issue(hotel.name, f"нет цены на человека {room.value}"))
        if hotel.partner and hotel.partner != tour.receiving_party:
            issues.append(
                Issue(hotel.name, f"партнёр цены «{hotel.partner}» ≠ принимающая сторона «{tour.receiving_party}»")
            )
    for p in tour.flights.problems():
        issues.append(Issue("Авиа", p))
    for s in tour.services:
        for p in s.problems():
            issues.append(Issue("Услуги", p))
    if not any(s.name == "Виза" and s.included for s in tour.services):
        issues.append(Issue("Услуги", "виза не включена в пакет"))
    for name in tour.unpriced_addons:
        issues.append(Issue("Услуги", f"нет цены для «{name}»"))
    labels = {s.label() for s in tour.commission}
    if not tour.commission:
        issues.append(Issue("Комиссия", "нет записи «Комиссии туроператора»"))
    elif len(tour.commission) == 1 and tour.commission[0].start > tour.commission[0].end:
        issues.append(Issue("Комиссия", f"сезон {labels.pop()} надо разбить на две записи"))
    return [Issue(f"{tour.code} · {i.where}", i.what) for i in issues]


def check_all(tours: list[Tour]) -> list[Issue]:
    seen = set()
    out = []
    for t in tours:
        for i in check_tour(t):
            key = (i.where.split(" · ", 1)[1], i.what)
            if key not in seen:  # a shared hotel or flight is reported once
                seen.add(key)
                out.append(i)
    return out
