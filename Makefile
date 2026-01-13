DC = docker compose
TEST_STORAGE_FILE = docker_compose/test_storage.yaml
STORAGE_FILE = docker_compose/storage.yaml
APP_FILE = docker_compose/app.yaml
BOT_FILE = docker_compose/bot.yaml
REDIS_FILE = docker_compose/redis.yaml
CELERY_WORKER_FILE = docker_compose/celery_worker.yaml
CELERY_BEAT_FILE = docker_compose/celery_beat.yaml

# ------------------------
# App
# ------------------------
.PHONY: app
app:
	${DC} -f ${APP_FILE} up --build -d

.PHONY: drop-app
drop-app:
	${DC} -f ${APP_FILE} down

.PHONY: app-logs
app-logs:
	${DC} -f ${APP_FILE} logs -f

# ------------------------
# Storage
# ------------------------
.PHONY: storage
storage:
	${DC} -f ${STORAGE_FILE} up --build -d

.PHONY: drop-storage
drop-storage:
	${DC} -f ${STORAGE_FILE} down

.PHONY: storage-logs
storage-logs:
	${DC} -f ${STORAGE_FILE} logs -f

# ------------------------
# Test Storage
# ------------------------
.PHONY: test-storage
test-storage:
	${DC} -f ${TEST_STORAGE_FILE} up --build -d

.PHONY: drop-test-storage
drop-test-storage:
	${DC} -f ${TEST_STORAGE_FILE} down

.PHONY: test-storage-logs
test-storage-logs:
	${DC} -f ${TEST_STORAGE_FILE} logs -f

# ------------------------
# Redis
# ------------------------
.PHONY: redis
redis:
	${DC} -f ${REDIS_FILE} up --build -d

.PHONY: drop-redis
drop-redis:
	${DC} -f ${REDIS_FILE} down

.PHONY: redis-logs
redis-logs:
	${DC} -f ${REDIS_FILE} logs -f

# ------------------------
# Bot
# ------------------------
.PHONY: bot
bot:
	${DC} -f ${BOT_FILE} up --build -d

.PHONY: drop-bot
drop-bot:
	${DC} -f ${BOT_FILE} down

.PHONY: bot-logs
bot-logs:
	${DC} -f ${BOT_FILE} logs -f

# ------------------------
# Celery
# ------------------------
.PHONY: celery
celery:
	${DC} -f ${CELERY_WORKER_FILE} -f ${CELERY_BEAT_FILE} up --build -d

.PHONY: drop-celery
drop-celery:
	${DC} -f ${CELERY_WORKER_FILE} -f ${CELERY_BEAT_FILE} down

.PHONY: celery-logs
celery-logs:
	${DC} -f ${CELERY_WORKER_FILE} -f ${CELERY_BEAT_FILE} logs -f

# ------------------------
# All services
# ------------------------
.PHONY: all
all:
	${DC} -f ${STORAGE_FILE} -f ${REDIS_FILE} -f ${APP_FILE} -f ${BOT_FILE} -f ${CELERY_WORKER_FILE} -f ${CELERY_BEAT_FILE} up --build -d

.PHONY: drop-all
drop-all:
	${DC} -f ${STORAGE_FILE} -f ${REDIS_FILE} -f ${APP_FILE} -f ${BOT_FILE} -f ${CELERY_WORKER_FILE} -f ${CELERY_BEAT_FILE} down

.PHONY: all-logs
all-logs:
	${DC} -f ${STORAGE_FILE} -f ${REDIS_FILE} -f ${APP_FILE} -f ${BOT_FILE} -f ${CELERY_WORKER_FILE} -f ${CELERY_BEAT_FILE} logs -f

# ------------------------
# Restart everything
# ------------------------
.PHONY: restart-all
restart-all: drop-all all