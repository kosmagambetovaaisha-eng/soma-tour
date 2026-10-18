from datetime import date

import pytest

from umrah_samo.commission import commission_for, split_over_new_year
from umrah_samo.currency import sar_to_usd


def test_season_over_new_year_is_two_records():
    seasons = split_over_new_year((1, 10), (31, 3), 5)
    assert [s.label() for s in seasons] == ["01.10–31.12", "01.01–31.03"]
    assert commission_for(seasons, date(2026, 11, 4)) == 5
    assert commission_for(seasons, date(2027, 2, 10)) == 5


def test_no_season_raises():
    seasons = split_over_new_year((1, 10), (31, 3), 5)
    with pytest.raises(LookupError):
        commission_for(seasons, date(2027, 6, 1))


def test_sar_rate_includes_cash_fee():
    assert round(sar_to_usd(3825), 2) == 1000
