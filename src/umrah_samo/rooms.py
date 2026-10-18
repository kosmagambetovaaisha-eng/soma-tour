"""Room types and the per-person placement formula.

SAMO stores hotel prices per person (A=SNGL, B=DBL, C=TRPL in the top table of
«Размещения на человека»). A room accommodation is priced only when the lower
table has a formula that turns per-person prices into a room price, e.g.
DBL room = 2 × DBL per person. Without that formula SAMO says «Не найдена цена».
"""

from enum import Enum


class Room(str, Enum):
    SNGL = "SNGL"
    DBL = "DBL"
    TRPL = "TRPL"
    QUAD = "QUAD"

    @property
    def pax(self) -> int:
        return {"SNGL": 1, "DBL": 2, "TRPL": 3, "QUAD": 4}[self.value]


# Letters SAMO uses in the top table of «Размещения на человека».
PER_PERSON_LETTER = {Room.SNGL: "A", Room.DBL: "B", Room.TRPL: "C", Room.QUAD: "D"}


def placement_formula(room: Room) -> str:
    """Formula text to type into «Ввод формулы размещения на человека»."""
    return f"{room.pax}*{PER_PERSON_LETTER[room]}"
