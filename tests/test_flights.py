from umrah_samo.flights import Flight, FlightPair, TicketType


def test_oneway_price_is_flagged():
    out = Flight("DV495", "ALA-JED", TicketType.ONEWAY, ["DV498"])
    back = Flight("DV498", "MED-ALA", TicketType.ALL)
    assert FlightPair(out, back, 840).problems() == ["DV495: тип билета «В одну сторону», нужно «Все»"]


def test_return_must_be_linked():
    out = Flight("DV495", "ALA-JED", TicketType.ALL, ["DV496"])
    back = Flight("DV498", "MED-ALA", TicketType.ROUNDTRIP)
    assert "не указан обратным рейсом" in FlightPair(out, back, 840).problems()[0]
