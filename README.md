# TempoTrack

Personal Routine Assistant & Time Tracker

## 📌 Description

**TempoTrack** is a backend system with a REST API and a Telegram bot for managing personal schedules and time tracking.

The system helps users:

- structure their daily routines,
- track time spent on tasks,
- receive reminders and notifications via Telegram.

The project is built using **Clean Architecture** and **DDD principles**, with a strong focus on separation of concerns, testability, and long-term maintainability.

---

Key principles:

- Domain layer does not depend on frameworks
- Infrastructure details are isolated
- Business logic is tested independently from FastAPI and the database

---

## 🛠 Technologies (Stack)

- **Backend:** Python 3.11+, FastAPI
- **Telegram Bot:** Aiogram
- **Background tasks:** Celery + Redis
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.0 (async)
- **Auth:** JWT (access + refresh tokens), bcrypt, hashlib
- **Validation:** Pydantic
- **Testing:** pytest, pytest-asyncio
- **Logging:** loguru
- **Containerization:** Docker, Docker Compose

---

## ✅ Implemented Features

**👤 Authentication & Users**

- User registration
- User authentication (login)
- Password hashing and validation
- JWT-based authentication:
  - access token (short-lived)
  - refresh token (stored securely)

**📅 Schedules**

- Adding a new schedule
- Change of the main schedule
- Adding items to the schedule
- Validation of schedule items (time ranges, ownership)

**🤖 Telegram Bot**
Currently implemented:

- Account verification via Telegram:
  - One-time verification code generation
  - Secure code delivery via Telegram bot
  - Linking a Telegram account to a user profile
- Sending schedule notifications to users
  **Not implemented / intentionally omitted:**
- No keyboards
- No interactive schedule management via Telegram
- Bot is used strictly for verification and notifications

**🔔 Notifications**

- Background generation of schedule notifications
- Asynchronous notification processing via Celery
- Telegram delivery of notifications

**🧱 Architecture**

- Clean separation of:
  - domain
  - application (use cases)
  - infrastructure
  - interfaces (web and bot layers)
- Background tasks isolated from web layer
- Infrastructure **fully** containerized

---

## 🚀 Running the project (locally)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/1Laurenz1/TempoTrack.git
cd TempoTrack
```

---

### 2️⃣ Create .env file

Create a .env file (location depends on your setup, e.g. project root or config folder): recommended path: src\infrastructure\config\.env

```env
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DATABASE_NAME
DEV_DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DATABASE_NAME
TEST_DATABASE_URL=postgresql+asyncpg://postgres:test_db_passwd@localhost:5432/test_db

REDIS_HOST=redis
REDIS_PORT=6379
BOT_TOKEN=YOUR_BOT_TOKEN

SECRET_KEY = YOUR_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### **⚠️ Important**:

Generate a secure SECRET_KEY:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

### 3️⃣ Install dependencies (Poetry)

```bash
poetry install
```

---

### 4️⃣ Run the FastAPI application

You can run the backend in two ways: **via Makefile (recommended)** or **directly via Poetry**. Makefile ensures that all dependencies (like the database) are started automatically.

**Option 1: Using Makefile (recommended)**

```bash
# Start all necessary services (FastAPI app, telegram bot, database, redis, celery worker, celery beat)
make all

# Optional: view logs for specific services
make app-logs       # View FastAPI app logs
make bot-logs       # View Telegram bot logs
make storage-logs   # View database logs
make redis-logs     # View redis logs
make celery-logs    # View celery logs

# Stop all services when done
make drop-all
```

This approach is recommended because it automatically starts the main database and all services in the correct order.

The API will be available at:

- Swagger UI: http://localhost:8000/docs

- OpenAPI JSON: http://localhost:8000/openapi.json

**Option 2: Using Poetry directly**
If you prefer to run the app manually, you must ensure that the main database is already running:

```bash
# Start the main database separately
make storage

# Run the FastAPI application directly
poetry run uvicorn src.interfaces.web.main:create_app --factory --reload

# Check the API:
# Swagger UI: http://localhost:8000/docs
# OpenAPI JSON: http://localhost:8000/openapi.json
```

⚠️ Important: The application **requires the database to be running**. Use **make storage** to start the database container before running the app with Poetry.

**Notes**

- For development, make all is usually the fastest way to start everything in the correct order.

- You can follow logs in real-time using make <service>-logs.

- After finishing work, clean up resources using make drop-all to stop and remove all containers.

---

### 🐳 Docker & Docker Compose

The project uses Docker Compose to run infrastructure services (databases and app containers). The main compose files are located in the _docker_compose/_ directory:

```text
docker_compose/
├── app.yaml              # FastAPI application
├── bot.yaml              # Telegram bot
├── celery_worker.yaml    # Celery worker
├── celery_beat.yaml      # Celery beat
├── redis.yaml            # Redis database
├── storage.yaml          # Primary database
└── test_storage.yaml     # Test database (used by pytest)
```

### **⚠️ Important:**

- Tests **never touch the main database**.

- A separate PostgreSQL container is started for running tests.

- Always use the test database container (_test_storage.yaml_) when running tests locally.

---

### 🧪 Test Database

To run tests successfully, a **test database must be running.**

#### **Start the test database**

```bash
make test-storage
```

This will:

- Start a PostgreSQL container from _docker_compose/test_storage.yaml_

- Run in **detached mode**

- Be used only for tests

**View test database logs (optional)**

```bash
make test-storage-logs
```

**Stop and remove the test database**

```bash
make drop-test-storage
```

⚠️ **Destructive operation**: This will completely remove the test database container. Use only for testing and local development.

### 🧪 Running tests (with DB)

Typical workflow:

```bash
make test-storage   # Start test database
pytest              # Run tests
make drop-test-storage  # Stop and remove test database
```

Or manually:

```bash
docker compose -f docker_compose/test_storage.yaml up --build -d
pytest
docker compose -f docker_compose/test_storage.yaml down
```

Tests cover:

- authentication use cases
- password hashing and validation
- repository logic
- API endpoints

---

### 🤝 Contributing

The project is under active development.
Ideas, issues, and pull requests are welcome.

## 👤 Author

**1Laurenz1**

- GitHub: https://github.com/1Laurenz1
- Telegram: https://t.me/Laurenz5

### 📝 License

**MIT License**
