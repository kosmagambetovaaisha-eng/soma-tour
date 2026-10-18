import pytest

from umrah_samo.hotels import Hotel, PriceNotFound
from umrah_samo.rooms import Room, placement_formula


def test_formula_text():
    assert placement_formula(Room.SNGL) == "1*A"
    assert placement_formula(Room.DBL) == "2*B"
    assert placement_formula(Room.TRPL) == "3*C"


def test_room_price_needs_formula():
    h = Hotel("H", "Makkah", per_person_night={Room.DBL: 200})
    with pytest.raises(PriceNotFound, match="2\\*B"):
        h.room_night(Room.DBL)
    h.formulas.add(Room.DBL)
    assert h.room_night(Room.DBL) == 400
    assert h.per_person(Room.DBL, 4) == 800
