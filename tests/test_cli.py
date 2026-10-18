from umrah_samo.cli import main


def test_price_prints_product_difference(data_dir, capsys):
    assert main(["--data", str(data_dir), "price", "X"]) == 0
    out = capsys.readouterr().out
    assert "2457.00" in out
    assert "разница +57.00" in out


def test_export_writes_rows(data_dir, tmp_path, capsys):
    out = tmp_path / "price.csv"
    assert main(["--data", str(data_dir), "export", str(out), "--date", "04.11.2026", "--date", "11.11.2026"]) == 0
    lines = out.read_text(encoding="utf-8-sig").splitlines()
    assert lines[0].startswith("tour_code;")
    assert len(lines) == 1 + 2 * 3


def test_check_fails_on_bundled_data(capsys):
    assert main(["check"]) == 1
