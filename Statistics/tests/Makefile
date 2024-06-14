PYTHONPATH := $(GITHUB_WORKSPACE)/Statistics/src:$(GITHUB_WORKSPACE):$(GITHUB_WORKSPACE)/common/statistics_proto

e2e_tests:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest tests_e2e.py --asyncio-mode=auto -p no:warnings

unit_tests:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest tests_unit.py -p no:warnings

broker_tests:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest tests_message_broker.py --asyncio-mode=auto -p no:warnings

all_tests: unit_tests e2e_tests broker_tests