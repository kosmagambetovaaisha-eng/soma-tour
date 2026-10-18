from datetime import date

from umrah_samo.calculator import quote
from umrah_samo.checker import check_all
from umrah_samo.loader import load_tours
from umrah_samo.rooms import Room

START = date(2026, 11, 4)


def tour(data_dir):
    return load_tours(data_dir)[0]


def test_dbl_with_visa(data_dir):
    q = quote(tour(data_dir), Room.DBL, START)
    # 4×200 + 3×100 + 840 flight + 100 guide + 300 visa
    assert q.net == 2340
    assert q.total == 2457


def test_visa_can_be_removed(data_dir):
    assert quote(tour(data_dir), Room.DBL, START, with_visa=False).net == 2040


def test_my_seat_only_when_chosen(data_dir):
    assert quote(tour(data_dir), Room.DBL, START, addons=("My Seat",)).net == 2365


def test_clean_setup_has_no_issues(data_dir):
    assert check_all(load_tours(data_dir)) == []


def test_bundled_data_shows_open_work():
    issues = [str(i) for i in check_all(load_tours())]
    assert any("Swissotel Makkah" in i and "SNGL" in i for i in issues)
    assert any("DV495" in i for i in issues)
    assert any("My Seat" in i for i in issues)
