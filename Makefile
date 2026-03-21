.PHONY: lint, format, check

CODE := common.py fifo_reader.py main.py window.py widgets

lint:
	mypy $(CODE)

format:
	ruff check --select F401 --fix $(CODE)
	black $(CODE)

check: format lint
