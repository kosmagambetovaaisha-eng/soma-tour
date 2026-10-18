"""Command line: umrah-samo price | check | export."""

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

from .calculator import quote
from .checker import check_all
from .hotels import PriceNotFound
from .loader import load_tours
from .rooms import Room


def _date(s: str) -> date:
    return datetime.strptime(s, "%d.%m.%Y").date()


def cmd_price(args) -> int:
    tours = {t.code: t for t in load_tours(args.data)}
    tour = tours[args.tour]
    try:
        q = quote(tour, Room(args.room), args.date, with_visa=not args.no_visa, addons=tuple(args.addon))
    except PriceNotFound as e:
        print(f"Не найдена цена: {e}", file=sys.stderr)
        return 1
    print(f"{tour.name}, {q.room.value}, заезд {q.start:%d.%m.%Y}")
    for name, value in q.lines:
        print(f"  {name:<32} {value:>10.2f}")
    print(f"  {'Нетто':<32} {q.net:>10.2f}")
    print(f"  {f'Итого (+{q.commission_percent:g} %)':<32} {q.total:>10.2f}")
    target = tour.product_price.get(q.room.value)
    if target:
        print(f"  {'PRODUCT':<32} {target:>10.2f}  разница {q.total - target:+.2f}")
    return 0


def cmd_check(args) -> int:
    issues = check_all(load_tours(args.data))
    for i in issues:
        print(i)
    print(f"\nВсего: {len(issues)}")
    return 1 if issues else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="umrah-samo")
    ap.add_argument("--data", type=Path, help="папка с hotels.json, flights.json, tours.json")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("price", help="цена тура на человека")
    p.add_argument("tour")
    p.add_argument("--room", default="DBL", choices=[r.value for r in Room])
    p.add_argument("--date", type=_date, default=date(2026, 11, 4), help="дд.мм.гггг")
    p.add_argument("--no-visa", action="store_true")
    p.add_argument("--addon", action="append", default=[])
    p.set_defaults(func=cmd_price)

    c = sub.add_parser("check", help="что ещё исправить в САМО")
    c.set_defaults(func=cmd_check)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
