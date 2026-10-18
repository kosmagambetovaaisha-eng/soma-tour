"""Package services: visa and optional add-ons."""

from dataclasses import dataclass


@dataclass
class Service:
    name: str
    price: float  # USD per person
    included: bool = False  # «Включена в пакет»
    removable: bool = True  # «Доступна для удаления»
    default: bool = False  # «Выбрана по умолчанию»
    offered: bool = False  # «Предлагаемая»
    required: bool = False  # «Необходима»

    def problems(self) -> list[str]:
        out = []
        if self.included and self.required and self.removable:
            out.append(f"{self.name}: «Необходима» не даст удалить услугу")
        return out


def visa(price: float = 300.0) -> Service:
    """Visa is in the package and selected by default, but can be removed."""
    return Service("Виза", price, included=True, removable=True, default=True)


def addon(name: str, price: float) -> Service:
    """An optional extra the agent can add, like train, kit or My Seat."""
    return Service(name, price, offered=True)
