"""Load hotels, flights and tours from the JSON files in data/."""

import json
from importlib import resources
from pathlib import Path

from .commission import split_over_new_year
from .flights import Flight, FlightPair, TicketType
from .hotels import Hotel
from .rooms import Room
from .services import addon, visa
from .tour import Tour


def _read(name: str, data_dir: Path | None) -> dict:
    if data_dir:
        return json.loads((Path(data_dir) / name).read_text(encoding="utf-8"))
    return json.loads(resources.files("umrah_samo.data").joinpath(name).read_text(encoding="utf-8"))


def load_hotels(data_dir: Path | None = None) -> dict[str, Hotel]:
    out = {}
    for h in _read("hotels.json", data_dir)["hotels"]:
        out[h["name"]] = Hotel(
            name=h["name"],
            city=h["city"],
            partner=h.get("partner", ""),
            per_person_night={Room(k): float(v) for k, v in h["per_person_night"].items()},
            formulas={Room(r) for r in h["formulas"]},
        )
    return out


def load_flights(data_dir: Path | None = None) -> tuple[dict[str, Flight], list[FlightPair]]:
    raw = _read("flights.json", data_dir)
    flights = {
        f["number"]: Flight(f["number"], f["route"], TicketType(f["ticket_type"]), f["returns"])
        for f in raw["flights"]
    }
    pairs = [FlightPair(flights[p["outbound"]], flights[p["inbound"]], p["adult"]) for p in raw["pairs"]]
    return flights, pairs


def load_tours(data_dir: Path | None = None) -> list[Tour]:
    hotels = load_hotels(data_dir)
    _, pairs = load_flights(data_dir)
    raw = _read("tours.json", data_dir)
    d = raw["defaults"]
    tours = []
    for t in raw["tours"]:
        c = {**d, **t}
        out_no, in_no = c["flights"]
        pair = next(p for p in pairs if p.outbound.number == out_no and p.inbound.number == in_no)
        services = [visa(c["visa"])]
        unpriced = []
        for name, price in c["addons"].items():
            if price is None:
                unpriced.append(name)
            else:
                services.append(addon(name, price))
        cm = c["commission"]
        tours.append(
            Tour(
                code=c["code"],
                name=c["name"],
                receiving_party=c["receiving_party"],
                makkah=hotels[c["makkah"]],
                makkah_nights=c["makkah_nights"],
                madinah=hotels[c["madinah"]],
                madinah_nights=c["madinah_nights"],
                flights=pair,
                guide=c["guide"],
                services=services,
                commission=split_over_new_year(tuple(cm["start"]), tuple(cm["end"]), cm["percent"]),
                product_price=c.get("product_price", {}),
                unpriced_addons=unpriced,
            )
        )
    return tours
