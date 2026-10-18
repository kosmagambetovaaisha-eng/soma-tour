"""Flights and ticket types.

A flight price that takes part in a package must have ticket type «Все» or
«Туда-обратно». A price set to «В одну сторону» is ignored in package pricing.
"""

from dataclasses import dataclass, field
from enum import Enum


class TicketType(str, Enum):
    ALL = "Все"
    ROUNDTRIP = "Туда-обратно"
    ONEWAY = "В одну сторону"

    @property
    def usable_in_package(self) -> bool:
        return self is not TicketType.ONEWAY


@dataclass
class Flight:
    number: str
    route: str
    ticket_type: TicketType
    returns: list[str] = field(default_factory=list)  # allowed return flights


@dataclass
class FlightPair:
    outbound: Flight
    inbound: Flight
    adult: float  # roundtrip price per adult, USD

    def problems(self) -> list[str]:
        out = []
        for f in (self.outbound, self.inbound):
            if not f.ticket_type.usable_in_package:
                out.append(f"{f.number}: тип билета «{f.ticket_type.value}», нужно «Все»")
        if self.inbound.number not in self.outbound.returns:
            out.append(
                f"{self.inbound.number} не указан обратным рейсом для {self.outbound.number}"
            )
        return out
