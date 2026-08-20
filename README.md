# Flask ToDo App

A multi-user ToDo web application built with Flask using a layered MVC-style architecture.

The application supports authenticated users, per-user Todo ownership, completion tracking, filtering and sorting, theme switching, and a service layer that keeps business logic separate from Flask request handling.

## Features

- User registration and login
- Session-based authentication
- Versioned REST API with Bearer token authentication
- Per-user Todo ownership
- Add, edit, delete, filter, and sort Todos
- Mark Todos as complete or reopen them
- Completion timestamps
- Light and dark themes
- Custom error handling
- Versioned PostgreSQL schema migrations with Flask-Migrate / Alembic
- 56 automated pytest tests running against PostgreSQL
- Per-user weekly completion statistics
- Cumulative completion rates

## Tech Stack

- **Python 3.12**
- **Flask** — routing, sessions, controllers, and application setup
- **Flask-SQLAlchemy / SQLAlchemy 2.0** — ORM and database access
- **PostgreSQL 16** — application and test database
- **Psycopg 3** — PostgreSQL driver
- **Flask-Migrate / Alembic** — database schema migrations
- **Docker** — local PostgreSQL environment
- **Jinja2** — server-rendered HTML templates
- **HTML/CSS** — user interface
- **pytest** — automated tests
- **uv** — dependency and environment management

## Project Structure

```text
.
├── app/
│   ├── controllers/       # Flask routes and request handling
│   ├── middlewares/       # Authentication and error handling
│   ├── migrations/        # Alembic migration environment and revisions
│   ├── models/            # SQLAlchemy database models
│   ├── services/          # Business logic and database operations
│   ├── static/            # CSS and static assets
│   ├── templates/         # Jinja2 templates
│   ├── app.py             # Flask application factory and entry point
│   └── config.py          # Application configuration
│
├── tests/                 # pytest test suite
├── .env.example           # Environment variable template
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock                # Locked dependency versions
└── README.md
```

### Architecture

The application separates responsibilities across several layers:

- **Models** define persisted data and relationships.
- **Services** contain business logic and database operations.
- **Controllers** handle Flask requests, sessions, redirects, and templates.
- **Templates** render the user interface.
- **Middleware** handles cross-cutting concerns such as authentication and error handling.
- **Alembic migrations** version and apply persistent database schema changes.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/georges1138/flask-todo-service.git
cd flask-todo-service
```

### 2. Install dependencies

This project uses `uv` for dependency and environment management:

```bash
uv sync
```

### 3. Start PostgreSQL

The local development setup uses PostgreSQL 16 in Docker.

Create and start the container:

```powershell
docker run -d --name todo-pg `
  -e POSTGRES_USER=todo `
  -e POSTGRES_PASSWORD=devpass `
  -e POSTGRES_DB=todo `
  -p 5432:5432 `
  -v todo-pg-data:/var/lib/postgresql/data `
  postgres:16
```

If the container already exists but is stopped:

```powershell
docker start todo-pg
```

Create a separate database for the test suite:

```powershell
docker exec -it todo-pg psql -U todo -d todo -c "CREATE DATABASE todo_test;"
```

The development and test databases are intentionally separate:

```text
todo       # development application data
todo_test  # disposable pytest data
```

### 4. Configure environment variables

The application requires `SECRET_KEY` and `DATABASE_URL`. The test suite requires its own `TEST_DATABASE_URL`.

Generate a random application secret:

```bash
uv run python -c "import secrets; print(secrets.token_hex(32))"
```

**PowerShell:**

```powershell
$env:SECRET_KEY = "paste-your-generated-secret-here"
$env:DATABASE_URL = "postgresql+psycopg://todo:devpass@localhost:5432/todo"
$env:TEST_DATABASE_URL = "postgresql+psycopg://todo:devpass@localhost:5432/todo_test"
```

**Linux/macOS:**

```bash
export SECRET_KEY="paste-your-generated-secret-here"
export DATABASE_URL="postgresql+psycopg://todo:devpass@localhost:5432/todo"
export TEST_DATABASE_URL="postgresql+psycopg://todo:devpass@localhost:5432/todo_test"
```

The application reads configuration from the process environment and fails loudly when required application configuration is missing.

### 5. Apply database migrations

Persistent schema changes are managed by Flask-Migrate / Alembic rather than `db.create_all()`.

From inside the `app/` directory:

```bash
cd app
uv run flask --app app db upgrade
```

This applies all migration revisions needed to bring the development PostgreSQL database to the current schema.

### 6. Run the application

From inside `app/`:

```bash
uv run python app.py
```

Then open:

```text
http://localhost:3000
```

## Running Tests

Tests run against the separate PostgreSQL `todo_test` database, not the development `todo` database.

Before running the suite, make sure:

1. the `todo-pg` Docker container is running,
2. the `todo_test` database exists, and
3. `TEST_DATABASE_URL` points to `todo_test`.

From the repository root:

```powershell
$env:TEST_DATABASE_URL = "postgresql+psycopg://todo:devpass@localhost:5432/todo_test"
uv run pytest
```

For verbose output:

```powershell
uv run pytest -v
```

The current suite contains **56 tests** covering Todo ownership and CRUD behavior, completion-state rules, user registration and authentication, API token authentication, Todo API CRUD and authorization behavior, JSON error handling, and PostgreSQL-backed reporting behavior including weekly bucketing, cumulative completion rates, per-user window partitions, and scoped reporting.

The test fixture creates and drops its schema in `todo_test`, so **do not point `TEST_DATABASE_URL` at the development `todo` database**.

## REST API

The application exposes a versioned JSON API alongside the server-rendered HTML interface.

Base URL:

```text
http://localhost:3000/api/v1
```

### Authentication

- API routes use Bearer token authentication rather than the browser session used by the server-rendered HTML interface.
- A client obtains an API token by sending its username, password, and a token name to `POST /api/v1/tokens`.
- The raw API token is returned only when the token is created, so clients should store it securely at that time.
- Only a SHA-256 hash of the token is stored in PostgreSQL; the raw token is not persisted by the application.


### Create an API token

Send valid user credentials and a descriptive name for the token:

```http
POST /api/v1/tokens
```

Required JSON fields:

- `username` — the username of an existing registered user.
- `password` — the password for that user account.
- `name` — a descriptive label that identifies the client or purpose of the token.

Example request:

```bash
curl -X POST http://localhost:3000/api/v1/tokens \
  -H "Content-Type: application/json" \
  -d '{
    "username": "exampleuser",
    "password": "example-password-not-real",
    "name": "local-development"
  }'
```

A successful request returns `201 Created` and a JSON response containing:

```json
{
  "token": "<raw-token-returned-once>",
  "token_id": 1,
  "name": "local-development"
}
```

The client must store the raw `token` value securely when it is returned because the application does not persist or display the raw token again.


### Using the token

Protected API routes expect the token in the HTTP `Authorization` header:

```http
Authorization: Bearer <token>
```

The Bearer token identifies the API user whose account and permissions apply to the request.

Example:

```bash
curl http://localhost:3000/api/v1/todos \
  -H "Authorization: Bearer <raw-token>"
```

If the `Authorization` header is missing or malformed, or the token is invalid or expired, the API returns `401 Unauthorized`.


### Todo endpoints

All Todo endpoints require Bearer token authentication.

| Method | Endpoint | Purpose | Success |
|---|---|---|---|
| `GET` | `/api/v1/todos` | List Todos belonging to the authenticated user. | `200 OK` |
| `GET` | `/api/v1/todos/<todo_id>` | Retrieve one Todo belonging to the authenticated user. | `200 OK` |
| `POST` | `/api/v1/todos` | Create a new Todo for the authenticated user. | `201 Created` |
| `PUT` | `/api/v1/todos/<todo_id>` | Replace the title and description of an existing Todo belonging to the authenticated user. | `200 OK` |
| `DELETE` | `/api/v1/todos/<todo_id>` | Delete an existing Todo belonging to the authenticated user. | `204 No Content` |
| `PATCH` | `/api/v1/todos/<todo_id>/completion` | Toggle an existing Todo belonging to the authenticated user between complete and incomplete. | `200 OK` |


### API authorization

For API requests, the authenticated user's identity is resolved from the Bearer token in the `Authorization` header rather than from a browser session.

Every Todo lookup, update, deletion, and completion change is scoped to the user identified by that token. A client can therefore access or modify only Todos belonging to the authenticated API user.

If a Todo ID belongs to another user, the API returns `404 Not Found`, the same response used when the Todo ID does not exist for the authenticated user.

Returning `404 Not Found` instead of `403 Forbidden` avoids revealing whether a Todo with that ID exists under another user's account. A `403 Forbidden` response could disclose the existence of another user's Todo even though the requesting user is not authorized to access it.

## Database Migrations

The project uses Flask-Migrate, backed by Alembic, to version PostgreSQL schema changes.

Typical workflow:

```bash
cd app
uv run flask --app app db migrate -m "Describe the schema change"
uv run flask --app app db upgrade
```

Generated migration files live in `app/migrations/versions/` and should be reviewed before they are applied.

## Design Decisions

**User ownership is passed into the service layer explicitly.** The server-rendered HTML controllers read `user_id` from the Flask session, while API controllers resolve the user from the Bearer token and use `g.user_id`. Both paths then pass the authenticated user ID into the same ownership-aware service layer rather than allowing services to depend directly on session or request authentication state. This keeps business logic easier to test, reusable across both interfaces, and less tightly coupled to Flask.

**`SECRET_KEY` and database configuration have no silent runtime fallback.** Missing configuration fails loudly instead of allowing the application to start with an insecure secret or an unintended database.

**Development and test databases are isolated.** The application uses the `todo` PostgreSQL database, while pytest uses `todo_test`. This prevents destructive test cleanup from touching development data and ensures tests run against the same database engine as the application.

**Todo completion stores both `completed` and `completed_at`.** The explicit Boolean keeps service and template logic easy to read, while the timestamp supports reporting. `TodoService.toggle_complete()` owns the invariant so reopening a Todo also clears its completion timestamp.

**Weekly counts can be produced with `GROUP BY`, but cumulative completion statistics need each weekly row to retain its own values while also carrying running totals across earlier weeks for the same user.** A window function handles that ordered, per-user accumulation without collapsing the result set.

## Security

`POST /api/v1/tokens` requires valid user credentials. Invalid credentials return a generic `401 Unauthorized` response without revealing whether the username or password was incorrect. Issued API tokens are stored only as hashes rather than as raw token values. The token-creation endpoint does **not** currently implement rate limiting, so high-volume credential attempts remain a known production-hardening gap; a production deployment should add a shared-backend rate limiter, such as Redis.

- Passwords are stored as hashes rather than plaintext.
- Todo operations are scoped to the authenticated user.
- Browser routes are protected by session authentication middleware, while `/api/` routes bypass session authentication and use Bearer token authentication.
- Session configuration requires an externally supplied secret key.
- Unauthorized Todo update, delete, and completion operations are rejected by the service layer.
