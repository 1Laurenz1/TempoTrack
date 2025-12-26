DC = docker compose
TEST_STORAGE_FILE = docker_compose/test_storage.yaml
STORAGE_FILE = docker_compose/storage.yaml
APP_FILE = docker_compose/app.yaml


.PHONY: app
app:
	${DC} -f ${APP_FILE} up --build -d

.PHONY: drop-app
drop-app:
	${DC} -f ${APP_FILE} down


.PHONY: storage
storage:
	${DC} -f ${STORAGE_FILE} up --build -d

.PHONY: drop-storage
drop-storage:
	${DC} -f ${STORAGE_FILE} down


.PHONY: test-storage
test-storage:
	${DC} -f ${TEST_STORAGE_FILE} up --build -d


.PHONY: drop-test-storage
drop-test-storage:
	${DC} -f ${TEST_STORAGE_FILE} down


.PHONY: all
all:
# 	${DC} -f ${STORAGE_FILE} -f {APP_FILE} --build -d
	docker compose -f ${STORAGE_FILE} -f ${APP_FILE} up --build -d
	docker compose -f ${STORAGE_FILE} -f ${APP_FILE} up --build -d

.PHONY: drop-all
drop-all:
# 	${DC} -f ${STORAGE_FILE} -f {APP_FILE} down
	docker compose -f ${STORAGE_FILE} -f ${APP_FILE} down