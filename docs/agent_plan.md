# Resume Evaluator Agent — Implementation Plan

## Goal

Build a LangChain (deepagents) based agent, driven from `backend/resume_agent.py`,
that evaluates a candidate resume against Slalom's interview guidelines (cached
from Confluence) and produces a short report recommending the Slalom **role** and
**seniority** the resume best aligns with, and why.

The agent is invoked from the command line:

```bash
python resume_agent.py --resume path/to/resume.(md|pdf)
```

---

## Decisions (confirmed)

| Topic | Decision |
| --- | --- |
| Criteria cache folder | New folder named `confluence/`. If missing, populate it with the `import_confluence` tool. |
| Agent framework | `deepagents.create_deep_agent` (same style as `langchain_test.py`). |
| Role / seniority taxonomy | Derived **dynamically** from the cached Confluence docs (Job Descriptions, discipline guides). Not hardcoded. |
| Report output | Printed to stdout **and** written to a Markdown file under `reports/`. |

---

## 1. Existing building blocks (reuse, do not rewrite)

- `backend/confluence_tool.py` → `import_confluence(page_id, out)` tool. Exports a
  Confluence page tree to Markdown. Root page id defaults to `56819899`, output
  dir defaults to `imported`.
- `backend/pdf_tool.py` → `convert_pdf_to_markdown(input_path, output_path)` tool.
  Converts a PDF to Markdown on disk.
- `backend/models.py` → `openai` chat model (`openai:gpt-4.1-mini`).
- `backend/langchain_test.py` → reference pattern for `create_deep_agent` usage.
- `truststore` Netskope workaround block — **must be the first thing** at the top of
  `resume_agent.py`, before any network-using imports run.

No new third-party dependencies are required; everything needed
(`deepagents`, `langchain`, `pymupdf4llm`, `atlassian-python-api`) is already in
`requirements.txt`.

---

## 2. Command-line interface

In `backend/resume_agent.py`:

- Use `argparse` with a required `--resume` argument (path to `.md` or `.pdf`).
- Optional args (nice-to-have, keep minimal):
  - `--confluence-dir` (default `confluence`) — criteria cache location.
  - `--report-dir` (default `reports`) — where the report is written.
- Validate that the resume file exists; error out clearly if not.

---

## 3. Step-by-step runtime flow

### Step A — Ensure the Confluence criteria cache exists

1. Check whether the `confluence/` folder exists and is non-empty.
2. If it does **not** exist (or is empty):
   - Call `import_confluence(out="confluence")` to export the guideline tree
     (uses the default root page id `56819899`).
3. If it exists, skip the import (avoid re-fetching on every run).

> Implementation note: this check can be done directly in Python before invoking
> the agent (deterministic, avoids spending model turns on a filesystem check),
> while still exposing `import_confluence` as a tool so the agent can refresh if
> asked.

### Step B — Normalize the resume to Markdown

1. Inspect the `--resume` file extension.
2. If `.pdf`: call `convert_pdf_to_markdown(input_path=<resume>)` and use the
   resulting `.md` path.
3. If `.md`: use it directly.
4. Otherwise: error out with a clear message (only `.md` / `.pdf` supported).
5. Read the resulting Markdown text into memory to pass to the agent.

### Step C — Load the evaluation criteria

1. Recursively read the Markdown files under `confluence/` that describe:
   - Interview process / guidance,
   - Job descriptions per discipline (SE, DE, QE, PE, XD, SO, …),
   - Sample questions / evaluation rubrics.
2. Because the full tree may be large, use a **selection strategy** to stay within
   context limits (see §5):
   - Prioritize `Job Descriptions/**` (role + seniority signals) and
     `Interviewing Guidance/**` (evaluation criteria).
   - Concatenate with clear file-path headers so the model can cite sources.

### Step D — Run the agent evaluation

1. Build the agent with `create_deep_agent`:
   - `model=openai`
   - `tools=[import_confluence, convert_pdf_to_markdown]` (available for
     on-demand refresh/conversion).
   - System prompt describing the evaluator role (see §4).
2. Invoke with a user message containing:
   - The resume Markdown,
   - The selected criteria text (or instructions on how it was provided),
   - The required output format.

### Step E — Produce and persist the report

1. Extract the agent's final message content.
2. Print it to stdout.
3. Write it to `reports/<resume-stem>-evaluation.md` (create `reports/` if needed).

---

## 4. Agent system prompt (content outline)

The system prompt should instruct the model to:

- Act as a Slalom hiring evaluator that scores resumes strictly against the
  **provided Confluence guidelines** (do not invent criteria).
- Identify the candidate's strongest-matching **discipline/role** (e.g. Software
  Engineering, Data Engineering, Quality Engineering, Platform Engineering,
  Experience Design, Solution Ownership) using signals in the Job Descriptions.
- Recommend a **seniority level** consistent with Slalom's descriptions
  (e.g. Consultant / Senior Consultant / Principal — as found in the docs).
- Justify the recommendation with concrete evidence from the resume mapped to
  guideline requirements.
- Flag notable gaps or missing signals.
- Output a **short, structured report** (see §6 format) — concise, not exhaustive.

---

## 5. Handling large criteria context

The `confluence/` tree can be large. Chosen approach for a first version:

- **Curated file selection**: include only the highest-signal folders
  (`Job Descriptions/**`, `Interviewing Guidance/**`, top-level
  `Interview Process`) rather than every file.
- Truncate/limit total characters to a safe budget for `gpt-4.1-mini`.
- (Future enhancement, out of scope now) replace curation with a retrieval step
  (embed guideline chunks, retrieve the top matches for the resume). Note this in
  the code as a TODO but do not build it yet.

---

## 6. Report format (target output)

```markdown
# Resume Evaluation — <candidate name or file>

## Recommended Role
<discipline / role>

## Recommended Seniority
<level>

## Rationale
- <evidence point mapped to a guideline requirement>
- <evidence point ...>

## Strengths
- ...

## Gaps / Risks
- ...

## Sources
- <confluence file paths referenced>
```

Keep it to roughly one screen — this is a "short report", not a full scorecard.

---

## 7. File layout after implementation

```
backend/
  resume_agent.py        # NEW — CLI entry point + agent orchestration
  confluence_tool.py     # reuse
  pdf_tool.py            # reuse
  models.py              # reuse
confluence/               # NEW — cached guideline markdown (created on first run)
reports/                 # NEW — generated evaluation reports
```

---

## 8. Implementation checklist

- [ ] Add truststore workaround block at the very top of `resume_agent.py`.
- [ ] Parse `--resume` (and optional `--confluence-dir`, `--report-dir`).
- [ ] Ensure `confluence/` cache exists; import via tool if missing.
- [ ] Convert PDF → Markdown when needed; read resume text.
- [ ] Load & curate criteria from `confluence/`.
- [ ] Build `create_deep_agent` with tools + evaluator system prompt.
- [ ] Invoke agent, capture final message.
- [ ] Print report to stdout and write `reports/<name>-evaluation.md`.
- [ ] Basic error handling for missing file / unsupported extension / import failure.

---

## 9. Open follow-ups (not blocking)

- Retrieval-based criteria selection instead of curated concatenation.
- Confidence score / multiple role candidates ranked.
- Batch mode for evaluating a folder of resumes.
