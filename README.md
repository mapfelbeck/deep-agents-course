# Interview Sheet Site

A monorepo with a **Python/FastAPI backend** and a **React/TypeScript frontend**
that lets an interviewer pick a role, upload a candidate resume, and get a
tabbed interview sheet (with autosaved per-question notes) plus the redacted
resume. See [docs/site_plan.md](docs/site_plan.md) for the full design.

```
backend/   FastAPI API + the deep-agent generation pipeline
frontend/  React 19 + Vite UI
docs/      Plans and brand guide
```

## Prerequisites

- Python 3.12+ and Node 20+.
- An `OPENAI_API_KEY` (used by the agent). Confluence credentials are only
  needed if you want to (re)import the cached guidelines in `backend/confluence/`.

## Configure

Copy the sample env and fill in values:

```bash
cp .env.sample .env   # set OPENAI_API_KEY (and DATABASE_URL for Postgres)
```

By default the backend uses a zero-setup **SQLite** file (`backend/app.db`).
For **Postgres**, start it with Docker and point `DATABASE_URL` at it:

```bash
docker compose up -d postgres
# DATABASE_URL=postgresql+psycopg://interview:interview@localhost:5432/interview
```

## Run the backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # if not already set up
pip install -r requirements.txt
alembic upgrade head            # or rely on auto-create on first run
uvicorn app.main:app --reload   # http://localhost:8000  (docs at /docs)
```

## Run the frontend

```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173 (proxies /api to :8000)
```

Open http://localhost:5173, choose a role, optionally upload a `.pdf`/`.md`
resume, and generate. The resume is always PII-redacted before use or storage.

## Tests

```bash
cd backend && pytest            # API smoke tests (agent stubbed, offline)
cd frontend && npm run build    # type-check + production build
```

---

Course reference:
https://academy.langchain.com/courses/take/foundation-introduction-to-deepagents/lessons/76263273-getting-set-up-python
