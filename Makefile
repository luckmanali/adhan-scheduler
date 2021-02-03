SHELL := /bin/bash
########################################################################################################################
## adhan-scheduler
########################################################################################################################
activate = poetry run

list:
	@grep '^[^#[:space:]].*:' Makefile

install:
	poetry install

lint:
	$(activate) pylint --output-format=parseable --rcfile=pylint.rc adhan_scheduler/* tests/*

test:
	$(activate) pytest -v
