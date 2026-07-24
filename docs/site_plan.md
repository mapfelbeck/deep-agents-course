# Interview Sheet Site — Monorepo Plan

## Goal

Turn this repository into a monorepo with a **Python backend** and a **React
frontend** that lets an interviewer:

1. Select the **role** they are interviewing a candidate for.
2. Upload the **candidate resume** (`.pdf` or `.md`).
3. Receive a **tabbed interface** with (a) the generated **interview sheet** and
   (b) the **redacted resume**.
4. Write **notes under each question** on the interview sheet.
5. Have those notes **saved automatically**.
6. **Revisit** their previously generated sheets and notes.

The backend wraps the existing agent in
[backend/interview_notes_agent.py](../backend/interview_notes_agent.py); the
frontend replaces the current Vite starter in
[frontend/src/App.tsx](../frontend/src/App.tsx).

---

## Confirmed decisions

| Topic | Decision |
| --- | --- |
| Auth (now) | **Single user**, no login. Architect so the app can sit behind **company SSO** later (see Auth Seam below). |
| Backend framework | **FastAPI** (async, typed, auto OpenAPI docs). |
| Storage | **Postgres** for metadata + saved notes; object/file storage for generated markdown and redacted resumes. |
| Generation UX | **Async job + poll**: submit returns a `job_id`, frontend polls status until the sheet is ready. |
| Monorepo tooling | **Simple folders** (`backend/`, `frontend/`) + root-level README and dev scripts. No workspace/turborepo layer. |
| Role list | **Backend endpoint** that lists Confluence Job Descriptions, reusing `find_job_descriptions` / `role_label`. |
| Notes | **Plain markdown**: render the sheet, provide editable **note blocks** per section/question, save the whole notes document. |
| Resume agent | `resume_agent.py` UI is **out of scope**, but its shared helpers stay (see note below). |

### Note on `resume_agent`

Per the request we ignore `resume_agent.py` as a *feature*. However,
[interview_notes_agent.py](../backend/interview_notes_agent.py) imports
`ensure_confluence_cache`, `resume_to_markdown`, `CONFLUENCE_ROOT_PAGE_ID`, and
`CRITERIA_CHAR_BUDGET` from it. Rather than depend on a module we are otherwise
retiring, **Phase 0** extracts those helpers into a shared module
(`backend/app/agent/shared.py`) so the interview flow no longer imports
`resume_agent`. No behavior changes.

---

## Recommended tech stack

### Backend
- **FastAPI** + **Uvicorn** — HTTP API and ASGI server.
- **Pydantic v2** — request/response models (already transitively installed).
- **SQLAlchemy 2.x** + **Alembic** — ORM and migrations for Postgres.
- **psycopg[binary]** — Postgres driver.
- **Background jobs** — start with **FastAPI `BackgroundTasks`** + a `jobs` table
  for status polling (no extra infra). Documented upgrade path to **ARQ** or
  **Celery + Redis** if concurrency grows.
- Existing agent stack stays: `deepagents`, `langchain`, `pymupdf4llm`,
  `atlassian-python-api`, `presidio-*`, `truststore` Netskope workaround.

### Frontend
- **React 19** + **TypeScript** + **Vite** (already scaffolded).
- **React Router** — routes for New Interview, Sheet view, History.
- **TanStack Query** — server state, polling the job status, caching sheets.
- **react-markdown** + **remark-gfm** — render the generated markdown sheet and
  redacted resume.
- **Design tokens** — a small CSS-variables theme derived from the brand guide
  (see Style Guide below). No heavy UI kit; keep it lightweight and accessible.
- Autosave notes via debounced `PUT` (TanStack Query mutation).

### Shared / infra
- **Postgres** (local via Docker Compose; managed instance later).
- **Docker Compose** for local dev (Postgres + backend + frontend).
- `.env` files per service; backend already loads `.env` via `python-dotenv`.

---

## Monorepo layout

```
deep-agents-course/
├── README.md                 # root: what it is + how to run everything
├── docker-compose.yml        # postgres (+ optional backend/frontend)
├── .env.sample               # root-level shared sample (db url, etc.)
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app + router registration + CORS
│   │   ├── config.py         # settings (env: DB URL, model, dirs)
│   │   ├── db.py             # SQLAlchemy engine/session
│   │   ├── models_db.py      # ORM: Interview, Job, Note
│   │   ├── schemas.py        # Pydantic request/response models
│   │   ├── deps.py           # auth seam (get_current_user) + db session dep
│   │   ├── storage.py        # read/write sheet + resume artifacts
│   │   ├── routers/
│   │   │   ├── roles.py      # GET /api/roles
│   │   │   ├── interviews.py # POST /api/interviews, GET list/detail
│   │   │   ├── jobs.py       # GET /api/jobs/{id}
│   │   │   └── notes.py      # GET/PUT /api/interviews/{id}/notes
│   │   └── agent/
│   │       ├── shared.py     # extracted from resume_agent (Phase 0)
│   │       └── runner.py     # wraps interview_notes_agent generation
│   ├── interview_notes_agent.py  # kept; refactored to import agent/shared
│   ├── confluence_tool.py … pii_redact.py  # unchanged tools
│   ├── alembic/              # migrations
│   ├── requirements.txt      # + fastapi, uvicorn, sqlalchemy, alembic, psycopg
│   └── tests/
├── frontend/
│   └── src/
│       ├── main.tsx          # router + query client providers
│       ├── theme.css         # brand design tokens (Style Guide)
│       ├── api/              # typed fetch client + hooks
│       ├── routes/
│       │   ├── NewInterview.tsx   # role select + resume upload
│       │   ├── Generating.tsx     # poll job status
│       │   ├── InterviewSheet.tsx # tabs: Sheet | Redacted Resume
│       │   └── History.tsx        # list past interviews
│       └── components/       # Tabs, NoteBlock, RoleSelect, FileUpload, Markdown
└── docs/
    └── site_plan.md          # this file
```

---

## Data model (Postgres)

```
interviews
  id            uuid  pk
  user_id       text            -- "default" for now; real id once SSO lands
  role          text            -- selected role label
  jd_paths      text[]          -- matched Confluence job description paths
  candidate     text  null      -- optional display label (from resume file name)
  sheet_md      text            -- generated interview sheet markdown
  resume_md     text            -- redacted resume markdown
  status        text            -- queued | generating | ready | error
  created_at    timestamptz
  updated_at    timestamptz

jobs
  id            uuid  pk
  interview_id  uuid  fk -> interviews.id
  status        text            -- queued | running | done | error
  error         text  null
  created_at    timestamptz
  updated_at    timestamptz

notes
  interview_id  uuid  pk fk -> interviews.id   -- one notes doc per interview
  notes_md      text            -- interviewer's saved notes (markdown)
  updated_at    timestamptz
```

`sheet_md`/`resume_md` can live in Postgres `text` columns initially; the
`storage.py` seam allows moving large artifacts to object storage later without
changing the API.

---

## API design

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/roles` | List selectable roles from Confluence Job Descriptions. |
| `POST` | `/api/interviews` | Multipart: `role` + optional `resume` file. Creates an interview + job, returns `{ interview_id, job_id }`. |
| `GET` | `/api/jobs/{job_id}` | Poll job status: `queued \| running \| done \| error`. |
| `GET` | `/api/interviews` | List past interviews (id, role, candidate, created_at, status). |
| `GET` | `/api/interviews/{id}` | Full detail: `sheet_md`, `resume_md`, `notes_md`, metadata. |
| `GET` | `/api/interviews/{id}/notes` | Current saved notes markdown. |
| `PUT` | `/api/interviews/{id}/notes` | Save notes markdown (autosave target). |

**Generation flow**
1. `POST /api/interviews` validates the role (via `match_role`), saves the
   uploaded resume to a temp path, creates `interview` (status `queued`) + `job`,
   schedules the background task, and returns ids immediately.
2. Background task runs `agent/runner.py`: `ensure_confluence_cache`,
   `resume_to_markdown` (redacts), `load_criteria`, `build_user_message`, invoke
   the deep agent, then persist `sheet_md` + `resume_md`, set status `ready`.
3. Frontend polls `GET /api/jobs/{job_id}` until `done`, then loads
   `GET /api/interviews/{id}` and shows the tabbed view.

**Security**
- Validate uploaded file type/size; only accept `.pdf`/`.md`.
- Resume is **always redacted** before storage (reuse existing PII pipeline);
  never persist the raw upload — delete the temp file after conversion.
- CORS restricted to the frontend origin.
- Parameterized queries via SQLAlchemy (no string SQL).

---

## Auth seam (single user now, SSO later)

- A single dependency `get_current_user()` in `deps.py` returns a fixed
  `User(id="default")` today.
- All rows are stamped with `user_id`; queries filter by it. Nothing else in the
  code assumes a single user.
- To enable SSO later, swap `get_current_user()` for an OIDC/SAML validator
  (e.g. via `Authorization` header / session cookie) — **no schema or query
  changes required**.

---

## Frontend flow & screens

1. **New Interview** (`/`)
   - `RoleSelect` (populated from `GET /api/roles`).
   - `FileUpload` for the resume (optional per the agent, but primary flow uploads one).
   - Submit → `POST /api/interviews` → navigate to Generating.
2. **Generating** (`/interviews/:id/generating`)
   - Polls the job; brand-styled progress state; on `done` redirects to the sheet.
3. **Interview Sheet** (`/interviews/:id`)
   - **Tabs**: `Interview Sheet` | `Redacted Resume`.
   - Sheet tab renders `sheet_md` with editable **note blocks** interleaved by
     section/question; a single notes markdown doc is autosaved (debounced `PUT`).
   - Resume tab renders `resume_md` (read-only).
4. **History** (`/history`)
   - Lists past interviews from `GET /api/interviews`; click opens the sheet with
     saved notes restored.

**Notes capture (plain-markdown approach)**
- The rendered sheet is parsed into sections/questions on the client for layout;
  each question gets a note textarea.
- Notes are serialized into one markdown document keyed by question and saved via
  `PUT …/notes`. On load, notes are re-hydrated back into the matching blocks.

---

## Style guide (derived from the brand guide)

Source: [docs/brand_guide.md](./brand_guide.md). Implement as CSS variables in
`frontend/src/theme.css`.

### Design tokens
```css
:root {
  /* Core palette — Slalom Blue must appear in every composition */
  --color-primary:        #0C62FB; /* Slalom Blue */
  --color-primary-dark:   #002FAF; /* Slalom Dark Blue */
  --color-accent-cyan:    #1BE1F2;
  --color-accent-coral:   #FF4D5F;
  --color-accent-purple:  #C7B9FF;
  --color-accent-chart:   #DEFF4D;

  /* Neutrals (use freely) */
  --color-black:   #000000;
  --color-text:    #666666; /* Dark Gray, text only */
  --color-border:  #E6E6E6; /* Light Gray */
  --color-surface: #FFFFFF;

  /* Typography */
  --font-sans: "Slalom Sans", system-ui, sans-serif; /* Avenir Next NOT allowed on web */
  --font-serif: "Lora", Georgia, serif;              /* supporting/optional */

  /* Type scale (test for AA) */
  --fs-h1: 2.75rem;  --lh-h1: 0.9;
  --fs-h2: 2rem;     --lh-h2: 0.9;
  --fs-h3: 1.5rem;   --lh-h3: 1.0;
  --fs-body: 1.0625rem; --lh-body: 1.1;
  --fs-eyebrow: 0.8125rem; --tracking-eyebrow: 0.075em;

  --radius: 8px; /* only ONE rounded corner per rectangle where used */
}
```

### Rules baked into components
- **One secondary color per view.** Pair Slalom Blue with a single accent
  (default: Cyan). Neutrals are unrestricted. Never a "rainbow" screen.
- **Accessibility (WCAG 2.1 AA):** body text ≥ 4.5:1, large text ≥ 3:1. Never
  convey meaning by color alone — pair with icon/shape/text (esp. Coral & Chartreuse).
- **Typography:** Slalom Sans primary; sentence case headings; flush-left,
  ragged-right; max three type sizes per layout; all-caps only for short eyebrows.
- **Buttons:** primary actions = Slalom Blue with AA contrast; focus/hover states
  are distinct and **not color-only** (add underline/weight/outline change).
- **Forms:** visible, consistent focus outlines; labels + helper text in Slalom
  Sans Regular; error/success states use color **plus** icon + text.
- **Icons:** single-color Slalom Blue / Dark Blue; always paired with text labels
  and accessible names.
- **Logo:** Slalom Blue/Dark Blue/White/Black only; preserve clear space; no
  effects or recolors.
- **Voice:** clear, confident, conversational, people-first; sentence case;
  active voice; define jargon on first use.

### Fonts
Slalom Sans / Lora are licensed brand fonts — load from the org's licensed web
font source (self-hosted `@font-face` or approved CDN). Provide the system-ui /
Georgia fallbacks above so the app remains usable before fonts resolve.

---

## Implementation phases

- **Phase 0 — Decouple shared agent code**
  Extract `ensure_confluence_cache`, `resume_to_markdown`,
  `CONFLUENCE_ROOT_PAGE_ID`, `CRITERIA_CHAR_BUDGET` into
  `backend/app/agent/shared.py`; update `interview_notes_agent.py` to import from
  it. Verify the CLI still works. No behavior change.

- **Phase 1 — Backend scaffold**
  Add FastAPI app, config, Docker Compose Postgres, SQLAlchemy models + Alembic
  migration, and the `/api/roles` endpoint. Add deps to `requirements.txt`.

- **Phase 2 — Generation pipeline**
  `agent/runner.py` wrapping the existing generation logic; `POST /api/interviews`
  + background job + `GET /api/jobs/{id}`; persist `sheet_md` / `resume_md`;
  enforce resume redaction and temp-file cleanup.

- **Phase 3 — Frontend foundation**
  Replace the Vite starter: router, TanStack Query, `theme.css` tokens, API
  client, New Interview + Generating screens end-to-end against the backend.

- **Phase 4 — Tabbed sheet + notes**
  Interview Sheet view with `Sheet | Redacted Resume` tabs, markdown rendering,
  per-question note blocks, and debounced autosave (`PUT …/notes`).

- **Phase 5 — History**
  `GET /api/interviews` list + detail navigation; restore saved notes on open.

- **Phase 6 — Polish & hardening**
  Accessibility pass (contrast, focus, labels), error/empty/loading states,
  upload validation, basic backend tests, root README with run instructions.

---

## Open items / future work

- Swap the fixed-user auth seam for company **SSO (OIDC/SAML)**.
- Move sheet/resume artifacts from Postgres `text` to object storage if they grow.
- Upgrade background jobs to **ARQ/Celery + Redis** if concurrent generations
  increase.
- Optional: export a finished sheet + notes to PDF/Markdown.
- Confirm the licensed source for **Slalom Sans / Lora** web fonts.
```
