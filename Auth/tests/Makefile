PYTHONPATH := $(GITHUB_WORKSPACE)/Auth/src:$(GITHUB_WORKSPACE):$(GITHUB_WORKSPACE)/Auth

unit_tests:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest tests_unit.py --asyncio-mode=auto -p no:warnings

all_tests: unit_tests 