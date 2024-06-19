PYTHONPATH := $(GITHUB_WORKSPACE):$(GITHUB_WORKSPACE)/common/tasks_proto

e2e_tests:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest tests_e2e.py -p no:warnings

unit_tests:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest tests_unit.py -p no:warnings

all_tests: unit_tests e2e_tests