.PHONY: install test check price

install:
	pip install -e ".[dev]"

test:
	pytest -q

check:
	python -m umrah_samo check

price:
	python -m umrah_samo price 13 --room DBL --date 04.11.2026
