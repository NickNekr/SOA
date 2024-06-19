PYTHONPATH := $(GITHUB_WORKSPACE):$(GITHUB_WORKSPACE)/common/statistics_proto:$(GITHUB_WORKSPACE)/common/tasks_proto

grpc: 
	PYTHONPATH=$(PYTHONPATH) poetry run pytest test_create_task.py --asyncio-mode=auto -p no:warnings -sss -v

kafka: 
	PYTHONPATH=$(PYTHONPATH) poetry run pytest test_send_like.py --asyncio-mode=auto -p no:warnings -sss -v

e2e_tests: grpc kafka 