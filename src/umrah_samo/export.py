"""Price list for B2B agents: one row per tour, room and check-in date."""

import csv
from datetime import date
from pathlib import Path

from .calculator import quote
from .hotels import PriceNotFound
from .rooms import Room
from .tour import Tour

COLUMNS = ["tour_code", "tour", "check_in", "room", "net", "commission_percent", "total", "with_visa"]


def price_rows(tours: list[Tour], dates: list[date], rooms=(Room.SNGL, Room.DBL, Room.TRPL)):
    for tour in tours:
        for d in dates:
            for room in rooms:
                try:
                    q = quote(tour, room, d)
                except PriceNotFound:
                    continue
                yield {
                    "tour_code": tour.code,
                    "tour": tour.name,
                    "check_in": d.strftime("%d.%m.%Y"),
                    "room": room.value,
                    "net": f"{q.net:.2f}",
                    "commission_percent": f"{q.commission_percent:g}",
                    "total": f"{q.total:.2f}",
                    "with_visa": "да",
                }


def write_csv(path: Path, rows) -> int:
    n = 0
    with open(path, "w", newline="", encoding="utf-8-sig") as f:  # BOM so Excel reads Cyrillic
        w = csv.DictWriter(f, fieldnames=COLUMNS, delimiter=";")
        w.writeheader()
        for r in rows:
            w.writerow(r)
            n += 1
    return n
