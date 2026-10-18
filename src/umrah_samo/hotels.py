"""Hotels and their per-person nightly prices."""

from dataclasses import dataclass, field

from .rooms import Room, placement_formula


class PriceNotFound(Exception):
    """Same situation as SAMO's «Не найдена цена»."""


@dataclass
class Hotel:
    name: str
    city: str  # "Makkah" or "Madinah"
    partner: str = ""  # empty partner = universal price in SAMO
    # per-person price for one night, USD, by room type
    per_person_night: dict[Room, float] = field(default_factory=dict)
    # rooms that have a placement formula entered in SAMO
    formulas: set[Room] = field(default_factory=set)

    def room_night(self, room: Room) -> float:
        """Price of the whole room for one night, as SAMO computes it."""
        if room not in self.formulas:
            raise PriceNotFound(
                f"{self.name}: нет формулы размещения для {room.value} "
                f"(нужно {placement_formula(room)})"
            )
        if room not in self.per_person_night:
            raise PriceNotFound(f"{self.name}: нет цены на человека для {room.value}")
        return room.pax * self.per_person_night[room]

    def per_person(self, room: Room, nights: int) -> float:
        return self.room_night(room) / room.pax * nights
