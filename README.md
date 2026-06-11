# Clustra

Multi-tenant task management API built with FastAPI, PostgreSQL, async SQLAlchemy, Alembic, and RBAC.

Clustra is in active development. The backend is being built around strict tenant isolation and clear service boundaries.

## What It Is

Clustra models work across this hierarchy:

```text
Organization -> Team -> Project -> Task
```

The goal is to support collaborative task management where users only access data through the organizations, teams, and projects they belong to.

## Core Ideas

- Organization, team, project, and task hierarchy
- Role-based access control
- Async FastAPI backend
- PostgreSQL-ready SQLAlchemy models
- Alembic migrations
- Service-layer business logic
- Router-layer HTTP handling
- Integration tests with async clients

## Role Model

Current roles are designed around collaboration boundaries:

- Organization Owner
- Admin
- Team Lead
- Contributor
- Viewer

## Architecture

The backend follows a consistent split:

```text
app/
  models/      SQLAlchemy models
  schemas/     Pydantic request and response schemas
  routers/     FastAPI route handlers
  services/    business logic
  utils/       permissions, activity logging, normalization
  database.py  async database session setup
  main.py      FastAPI application entrypoint
tests/         async integration tests
alembic/       database migrations
```

Routers handle HTTP concerns and delegate to services. Services own business rules and database operations.

## Tenant Isolation

Tenant isolation is a first-class design rule. Access checks happen before tenant-scoped data is read or modified.

Current service methods use membership and role checks before returning organization-scoped data.

## Current Status

Clustra is not a finished product yet. Active work includes:

- Organization dashboard views
- Frontend pages for auth and organization flows
- More permission checks across teams, projects, and tasks
- Broader integration test coverage
- CI/CD cleanup before production deployment

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

Run migrations:

```bash
alembic upgrade head
```

## Project Direction

Clustra is being built as a production-shaped backend project, not a quick demo. The focus is correctness, readable service boundaries, and tenant isolation by design.
