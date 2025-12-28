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
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.0 (async)
- **Auth:** JWT (access + refresh tokens), bcrypt, hashlib
- **Validation:** Pydantic
- **Testing:** pytest, pytest-asyncio
- **Logging:** loguru
- **Containerization:** Docker, Docker Compose

---

## ✅ Implemented Features

- User registration
- User authentication (login)
- Password hashing and validation
- Adding a new schedule
- Change of the main schedule
- Adding items to the schedule
- JWT-based authentication:
  - access token (short-lived)
  - refresh token (stored securely)
- Clean separation of:
  - domain
  - application (use cases)
  - infrastructure
  - web layer
- Unit and integration tests for auth logic

---

## 🚀 Running the project (locally)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/TempoTrack.git
cd TempoTrack
```

---

### 2️⃣ Create .env file

Create a .env file (location depends on your setup, e.g. project root or config folder): recommended path: src\infrastructure\config\.env

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5433/database_name
DEV_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/database_name
TEST_DATABASE_URL=postgresql+asyncpg://postgres:test_db_passwd@localhost:5432/test_db

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
```bash
poetry run uvicorn src.interfaces.web.main:create_app --factory --reload
```
The API will be available at:

- Swagger UI: http://localhost:8000/docs

- OpenAPI JSON: http://localhost:8000/openapi.json

---

### 🐳 Docker & Docker Compose

The project uses Docker Compose to run infrastructure services (databases and app containers).

```text
Main compose files
docker_compose/
├── app.yaml              # Main application (planned)
├── storage.yaml          # Primary database (planned)
└── test_storage.yaml     # Test database (used by pytest)
```

### **⚠️ Important:**
Tests **never touch the main database.**
A separate PostgreSQL container is started for running tests.

### 🧪 Test Database
To run tests successfully, a **test database must be running.**

#### **Start the test database**
```bash
make test-storage
```
What happens:

- PostgreSQL container from docker_compose/test_storage.yaml is started

- Runs in **detached mode**

- Used **only** for tests

#### **Stop and remove the test database**
```bash
make drop-test-storage
```
This completely removes the test database container.

⚠️ **Destructive operation**
Use only for testing and local development.


### 🧪 Running tests (with DB)

Typical workflow:
```bash
make test-storage
pytest
make drop-test-storage
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

### 🤖 Telegram Bot (planned)

The Telegram bot will:

- notify users about scheduled tasks,

- allow basic schedule management,

- integrate with the same backend via API.

**(Implementation in progress)**

---

### 🤝 Contributing

The project is under active development.
Ideas, issues, and pull requests are welcome.

### 📝 License

**MIT License**