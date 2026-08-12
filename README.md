# Flask ToDo App

A multi-user ToDo web application built with Flask using a layered MVC-style architecture.

The application supports authenticated users, per-user Todo ownership, completion tracking, filtering and sorting, theme switching, and a service layer that keeps business logic separate from Flask request handling.

## Features

- User registration and login
- Session-based authentication
- Per-user Todo ownership
- Add, edit, delete, filter, and sort Todos
- Mark Todos as complete or reopen them
- Completion timestamps
- Light and dark themes
- Custom error handling
- Versioned PostgreSQL schema migrations with Flask-Migrate / Alembic
- 15 automated pytest tests running against PostgreSQL

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
git clone https://github.com/georges1138/ToDo_List_app_with_Flask-MVC_Architecture.git
cd ToDo_List_app_with_Flask-MVC_Architecture
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

The current suite contains **15 tests** covering Todo ownership, CRUD behavior, completion-state rules, user registration, and authentication behavior.

The test fixture creates and drops its schema in `todo_test`, so **do not point `TEST_DATABASE_URL` at the development `todo` database**.

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

**User ownership is passed into the service layer explicitly.** Controllers read `user_id` from the Flask session and pass it to services rather than allowing the service layer to depend directly on Flask session state. This keeps business logic easier to test and less tightly coupled to Flask.

**`SECRET_KEY` and database configuration have no silent runtime fallback.** Missing configuration fails loudly instead of allowing the application to start with an insecure secret or an unintended database.

**Development and test databases are isolated.** The application uses the `todo` PostgreSQL database, while pytest uses `todo_test`. This prevents destructive test cleanup from touching development data and ensures tests run against the same database engine as the application.

**Todo completion stores both `completed` and `completed_at`.** The explicit Boolean keeps service and template logic easy to read, while the timestamp supports reporting. `TodoService.toggle_complete()` owns the invariant so reopening a Todo also clears its completion timestamp.

## Security

- Passwords are stored as hashes rather than plaintext.
- Todo operations are scoped to the authenticated user.
- Authentication middleware protects application routes by default, with explicit exemptions for authentication and static routes.
- Session configuration requires an externally supplied secret key.
- Unauthorized Todo update, delete, and completion operations are rejected by the service layer.
