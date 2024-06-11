PYTHONPATH := /Users/niknekrasov/Study/SOA/TasksService/src:/Users/niknekrasov/Study/SOA/:/Users/niknekrasov/Study/SOA/common/proto

e2e_tests:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest tests_e2e.py

unit_tests:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest tests_unit.py

all_tests: unit_tests e2e_tests