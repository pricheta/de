.PHONY: lint, format, check

CODE := common.py fifo_reader.py main.py window.py widgets

lint:
	mypy $(CODE)

format:
	black $(CODE)

check: format lint
