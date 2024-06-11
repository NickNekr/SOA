PYTHONPATH := /Users/niknekrasov/Study/SOA/Statistics/src:/Users/niknekrasov/Study/SOA/

e2e_tests:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest tests_e2e.py --asyncio-mode=auto

unit_tests:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest tests_unit.py

all_tests: unit_tests e2e_tests