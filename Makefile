.PHONY: lint, format, check, install

CODE := code

lint:
	mypy $(CODE)

format:
	ruff check --select F401 --fix $(CODE)
	black $(CODE)

check: format lint

install:
	rm -rf /home/pricheta/.local/bin/pricheta_de/*
	cp -r * /home/pricheta/.local/bin/pricheta_de/
