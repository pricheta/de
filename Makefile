.PHONY: lint

CODE := common.py fifo_reader.py main.py window.py widgets

lint:
	mypy $(CODE)
