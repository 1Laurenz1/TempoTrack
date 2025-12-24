DC = docker compose
TEST_STORAGE_FILE = docker_compose/test_storage.yaml


.PHONY: test-storage
test-storage:
	${DC} -f ${TEST_STORAGE_FILE} up --build -


.PHONY: drop-test-storage
drop-test-storage:
	${DC} -f ${TEST_STORAGE_FILE} down