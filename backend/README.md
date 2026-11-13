# Portfolio Backend

FastAPI backend for the personal portfolio website. Serves the REST API, admin panel, and static frontend.

## Features

- Public REST API for profile, skills, experience, projects, and education
- Contact form endpoint with optional SMTP email notifications
- SQLAdmin panel at `/admin` for content management
- JWT auth endpoints for programmatic admin access
- SQLite by default; PostgreSQL via `DATABASE_URL`

## Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
# source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS / Linux

alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload --port 8000
```

## URLs

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Portfolio site |
| http://localhost:8000/docs | OpenAPI docs |
| http://localhost:8000/admin | Admin panel |
| http://localhost:8000/api/health | Health check |

Default admin credentials (change in `.env`): `admin` / `changeme`

## Environment

See `.env.example` for all options. SMTP settings are optional; contact messages are always stored in the database.

## Docker

From the project root:

```bash
docker compose up --build
```

This starts PostgreSQL and the FastAPI backend on port 8000.

## Render

Production deploy uses the root `render.yaml` Blueprint (Docker web service + Postgres). See the project root README **Deploy on Render** section.
