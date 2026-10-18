"""A переездной Umrah tour: Makkah nights, then Madinah nights."""

from dataclasses import dataclass, field

from .commission import Season
from .flights import FlightPair
from .hotels import Hotel
from .services import Service


@dataclass
class Tour:
    code: str
    name: str
    receiving_party: str  # «Принимающая сторона»
    makkah: Hotel
    makkah_nights: int
    madinah: Hotel
    madinah_nights: int
    flights: FlightPair
    guide: float  # USD per person
    services: list[Service] = field(default_factory=list)
    commission: list[Season] = field(default_factory=list)
    product_price: dict[str, float] = field(default_factory=dict)  # PRODUCT, by room

    @property
    def nights(self) -> int:
        return self.makkah_nights + self.madinah_nights
