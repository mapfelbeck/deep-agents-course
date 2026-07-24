# Interview Notes Agent — Implementation Plan

## Goal

Build a LangChain (deepagents) based agent, driven from
`backend/interview_notes_agent.py`, that prepares an interviewer's prep sheet: a
set of **notes and questions** the interviewer takes into an interview. Inputs
are (1) Slalom's interview process/guidelines (cached from Confluence), (2) the
**role** the candidate is interviewing for, and (3) optionally the candidate's
**resume**. Output is a Markdown prep sheet where questions are grouped by
technology / skill / subject, and each skill section is ordered from easiest to
hardest. The purpose of the questions is to **verify the skills the candidate
lists on their resume** and to **confirm the skills required for the role**.

The agent is invoked from the command line:

```bash
# Role + resume (tailored to the candidate)
python interview_notes_agent.py --role "Software Engineer" --resume path/to/resume.(md|pdf)

# Role only (no resume) — role-based question bank
python interview_notes_agent.py --role "Software Engineer"
```

---

## Decisions (confirmed)

| Topic | Decision |
| --- | --- |
| Agent framework | `deepagents.create_deep_agent` (same style as `resume_agent.py` / `langchain_test.py`). |
| Resume | **Optional.** With a resume: tailor questions to verify listed skills + role skills. Without: generate a role-based question bank from the job description. |
| `--role` meaning | **Must match a Confluence Job Description.** Validate `--role` against the `Job Descriptions/**` tree; if no reasonable match is found, error out and list the available roles. |
| Output template | New file `backend/templates/interview_notes_template.md`, **read at runtime** so the user can edit the output format later without touching code. |
| Output destination | Written to a folder controlled by a `--interview-dir` arg (same pattern as `resume_agent.py`'s `--report-dir`). Default: `interviews`. |
| PII redaction | Same as `resume_agent.py`: `.md` resumes are redacted in-memory via `pii_redact.redact`; `.pdf` resumes are converted with `convert_pdf_to_markdown` (which redacts by default). Source files are never modified. |
| Criteria cache | Reuse the existing `confluence/` cache and `ensure_confluence_cache` logic; import via `import_confluence` if missing/empty. |

---

## 1. Existing building blocks (reuse, do not rewrite)

- `backend/confluence_tool.py` → `import_confluence(page_id, out)` tool. Exports a
  Confluence page tree to Markdown. Root page id defaults to `56819899`.
- `backend/pdf_tool.py` → `convert_pdf_to_markdown(input_path, output_path)` tool.
  Converts a PDF resume to Markdown on disk (PII-redacted by default).
- `backend/pii_redact.py` → `redact(text)` for in-memory redaction of `.md` resumes.
- `backend/models.py` → `openai` chat model (`openai:gpt-4.1-mini`).
- `backend/resume_agent.py` → reference pattern for CLI + cache + agent orchestration
  (reuse `ensure_confluence_cache`, `resume_to_markdown`, `load_criteria` shapes).
- `truststore` Netskope workaround block — **must be the first thing** at the top of
  `interview_notes_agent.py`, before any network-using imports run.

No new third-party dependencies are required; everything needed
(`deepagents`, `langchain`, `pymupdf4llm`, `atlassian-python-api`, `presidio-*`) is
already in `requirements.txt`.

---

## 2. Command-line interface

In `backend/interview_notes_agent.py`, use `argparse`:

- `--role` (**required**) — the role the interview is for; validated against the
  Confluence Job Descriptions (see §3, Step B).
- `--resume` (optional) — path to `.md` or `.pdf`. When omitted, the agent
  produces a role-based question bank.
- `--confluence-dir` (default `confluence`) — criteria cache location.
- `--interview-dir` (default `interviews`) — where the prep sheet is written.
- `--template` (default `templates/interview_notes_template.md`) — output template.

Validate that the resume file (when provided) and the template file exist; error
out clearly if not.

---

## 3. Step-by-step runtime flow

### Step A — Ensure the Confluence criteria cache exists

Reuse `ensure_confluence_cache(confluence_dir)` from `resume_agent.py`:
1. If `confluence/` exists and is non-empty, use it.
2. Otherwise call `import_confluence(out="confluence")` (default root page id).

### Step B — Resolve and validate `--role` against Job Descriptions

1. Enumerate available roles from `confluence/**/Job Descriptions/**/*.md`
   (derive candidate role names from the file/folder names and/or JD titles).
2. Match `--role` to the closest job description (case-insensitive; allow simple
   fuzzy/substring matching).
3. If no reasonable match is found, **error out** and print the list of available
   roles so the user can retry with a valid value.
4. Keep the matched JD file path(s) so the role's required skills can be loaded as
   primary criteria and cited as a source.

### Step C — Normalize the resume to Markdown (only if `--resume` given)

Reuse `resume_to_markdown(resume_path)` from `resume_agent.py`:
1. `.md` → read and `redact()` in memory (never modify the source file).
2. `.pdf` → `convert_pdf_to_markdown(...)`, then read the redacted `.md`.
3. Any other extension → clear error.
When `--resume` is omitted, skip this step and mark the run as "role-only".

### Step D — Load the evaluation / question criteria

Reuse a `load_criteria`-style selection to stay within context limits:
1. **Primary:** the matched Job Description(s) for `--role` (required skills).
2. **Secondary:** `Sample Questions and Scripts/**` and `Interviewing Guidance/**`
   (question banks, interview structure, evaluation rubrics).
3. Concatenate with clear `===== FILE: <path> =====` headers so the model can cite
   sources, capped by a character budget (reuse `CRITERIA_CHAR_BUDGET`).

### Step E — Load the output template

1. Read `backend/templates/interview_notes_template.md` at runtime.
2. Pass the template text to the agent as the required output structure so the
   user can change the format later by editing the file (no code change).

### Step F — Run the agent

1. Build the agent with `create_deep_agent`:
   - `model=openai`
   - `tools=[import_confluence, convert_pdf_to_markdown]` (on-demand refresh/convert).
   - System prompt describing the interviewer-prep role (see §4).
2. Invoke with a user message containing:
   - The resolved role + matched JD required skills,
   - The resume Markdown (or a note that no resume was provided),
   - The selected criteria / sample questions,
   - The output template to fill in.

### Step G — Produce and persist the prep sheet

1. Extract the agent's final message content.
2. Print it to stdout.
3. Write it to the `--interview-dir` folder (default `interviews/`), e.g.
   `interviews/<resume-stem>-interview-notes.md`, or when role-only,
   `interviews/<slugified-role>-interview-notes.md`. Create the folder if needed.

---

## 4. Agent system prompt (content outline)

Instruct the model to act as an **interview-prep assistant** for a Slalom
interviewer, and to:

- Use ONLY the provided Confluence guidelines, matched job description, and sample
  questions — do not invent Slalom process or criteria.
- Produce **notes** for the interviewer (talking points about the candidate and
  the role) plus **questions** to ask.
- **Group questions by technology / skill / subject** as appropriate.
- Within each technology/skill section, order questions from **easiest to hardest**
  (increasing difficulty).
- Ensure every question serves one of two purposes, and label which:
  1. **Verify a resume-claimed skill** (only when a resume is provided), or
  2. **Confirm a role-required skill** (from the matched job description).
- When a resume is provided, cross-reference resume skills against role
  requirements: highlight strong matches to probe deeply and gaps to explore.
- When no resume is provided, generate a role-based question bank covering the
  job description's required skills.
- Fill in the **provided output template** exactly (structure comes from the
  template file, not the prompt).
- Cite the Confluence source file paths used.

---

## 5. Output template (new editable file)

Create `backend/templates/interview_notes_template.md`. It defines the structure
the agent fills in and is fully user-editable. Proposed starting structure:

```markdown
# Interview Sheet — <role> — <candidate name or "role-based">

## Role Summary
- Role: <role>
- Source job description: <confluence path>
- Key skills required: <bulleted from JD>

## Candidate Snapshot
<!-- Omitted / "No resume provided" when run role-only -->
- Claimed skills relevant to this role: ...
- Notable strengths to probe: ...
- Potential gaps to explore: ...

## Interviewer Notes / Talking Points
- <topic to discuss with the candidate>
- ...

## Questions by Skill

### <Technology / Skill / Subject 1>
_Ordered easiest → hardest. Each question notes its purpose._
1. <question> — _(verify resume skill | confirm role skill)_
2. <question> — _(...)_
3. <question> — _(...)_

### <Technology / Skill / Subject 2>
1. ...

## Behavioral / Role-Fit Questions
- ...

## Sources
- <confluence file paths referenced>
```

The agent must respect whatever structure exists in this file at runtime.

---

## 6. Handling large criteria context

Same approach as `resume_agent.py`:
- Prioritize the matched Job Description(s) and `Sample Questions and Scripts/**`
  / `Interviewing Guidance/**`.
- Concatenate with file-path headers and enforce a character budget for
  `gpt-4.1-mini`.
- (Future, out of scope) replace curation with retrieval over guideline chunks;
  leave a `TODO` note but do not build it now.

---

## 7. File layout after implementation

```
backend/
  interview_notes_agent.py           # NEW — CLI entry point + agent orchestration
  templates/
    interview_notes_template.md      # NEW — editable output template (read at runtime)
  confluence_tool.py                 # reuse
  pdf_tool.py                        # reuse
  pii_redact.py                      # reuse
  models.py                          # reuse
confluence/                          # reuse — cached guideline markdown
interviews/                          # NEW — generated interview sheets
docs/
  interview_plan.md                  # THIS plan
```

---

## 8. Implementation checklist

- [ ] Add the `truststore` workaround block at the very top of
      `interview_notes_agent.py`.
- [ ] Parse `--role` (required), `--resume` (optional), `--confluence-dir`,
      `--interview-dir`, `--template`.
- [ ] Reuse `ensure_confluence_cache` to guarantee the `confluence/` cache.
- [ ] Enumerate Job Descriptions and validate `--role`; error with the list of
      available roles when no match is found.
- [ ] When `--resume` is given, reuse `resume_to_markdown` (redaction for `.md`,
      conversion for `.pdf`); otherwise run role-only.
- [ ] Load criteria: matched JD first, then sample questions / guidance, within a
      char budget.
- [ ] Read the output template file at runtime.
- [ ] Build `create_deep_agent` with tools + interviewer-prep system prompt.
- [ ] Invoke the agent with role + JD skills + resume (or "none") + criteria +
      template.
- [ ] Print the prep sheet to stdout and write it under `--interview-dir`.
- [ ] Basic error handling: missing/unsupported resume, missing template, invalid
      role, import failure.
- [ ] Create `backend/templates/interview_notes_template.md` with the §5 structure.
