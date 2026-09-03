# Agent Instructions

These rules apply to every coding or review agent working in this repository.

## Repository source of truth

At the start of meaningful work, read all five files:

1. `AGENTS.md` — operating and safety rules;
2. `SPEC.md` — stable product and scientific requirements;
3. `STATE.md` — current transient status and blockers;
4. `DECISIONS.md` — lasting architecture/scientific decisions;
5. `ROADMAP.md` — milestone scope and gates.

Chat history is not project memory. If canonical repository documents conflict,
do not silently choose the convenient rule. Stop the conflicting work, identify
the conflict, and resolve it in the correct source-of-truth document:

- stable requirements -> `SPEC.md`;
- lasting architecture/scientific decisions -> `DECISIONS.md`;
- milestone scope/gates -> `ROADMAP.md`;
- current transient status -> `STATE.md`.

Confirm the current milestone before implementation. Do not implement a later
milestone while its gate is closed. Define the problem and acceptance criteria
and link or create the GitHub issue for meaningful work.

## Non-negotiable scientific rules

- Never silently infer, correct, replace, normalize away, discard, or confirm a
  scientific observation.
- Keep raw observation, parsed scalar/series candidate, explicit confirmation,
  confirmed record, canonical representation, and derived result distinct.
- AI/OCR/speech outputs are candidates, never scientific authority.
- Validation state (`pending`, `valid`, `invalid`) is separate from lifecycle
  (`active`, `superseded`).
- Use deterministic schemas, rules, dimensional analysis, and explicit user
  confirmation.
- Do not call sample variance, sample standard deviation, or SEM measurement
  uncertainty without a valid uncertainty model and declared assumptions.
- Treat temperature points, temperature intervals, `dBm`, and power-ratio `dB`
  through their explicit policies.
- Preserve rejected rows, outliers, corrections, source references/digests, and
  scientific transformation provenance.
- Record export activity separately; exporting must not mutate scientific
  provenance.

## Architecture rules

- The core must not import GUI, CLI, SQLite/CSV/export adapters, OCR, speech,
  instruments, or cloud services.
- Outer application/adapters depend inward on core types and ports.
- Photonics belongs in versioned definitions, schemas, examples, and adapters
  unless a rule is physically generic.
- Runtime resources must be packaged inside `smr` and loaded through supported
  package-resource APIs; never assume top-level `schemas/` exists after install.
- Use typed interfaces, timezone-aware datetimes, versioned schemas, and
  append-only scientific provenance.
- Do not add cloud databases, hosted AI, telemetry, or required accounts.

## Data and secret safety

Never commit credentials, tokens, private keys, `.env` contents, access URLs,
personal data, or secret-bearing logs. Never commit confidential, proprietary,
unlicensed, export-controlled, or unpublished laboratory data. Synthetic data
must be labeled synthetic; real data requires documented permission, provenance,
license, and privacy review.

If sensitive data appears in the worktree or history, stop, avoid copying it into
tool output, and notify the owner through the approved private channel.

## Git safety

Without explicit repository-owner permission, agents must not:

- force-push or bypass branch protection;
- rewrite public/shared history;
- delete branches, tags, repository content, releases, issues, or artifacts;
- merge to `main` or another protected/default branch;
- use destructive cleanup/reset commands;
- commit secrets or restricted laboratory data.

Preserve unrelated owner changes. Use focused branches and non-destructive,
reviewable commits.

## Engineering workflow

For each meaningful change: issue -> branch -> implementation -> deterministic
tests -> format/lint/type checks -> review -> PR -> fixes -> rerun -> owner-
authorized merge -> canonical document/state update. Add a regression test for
every corrected scientific defect.

M0/core checks:

```bash
uv lock --check
uv sync --locked --dev
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest --cov=smr --cov-report=term-missing
uv build
```

GUI dependencies are not installed in M0/M1 quality paths. M4 owns a dedicated
`gui` extra job.

## Current gate

M0 is open and M1 is CLOSED. Do not add runtime `Measurement`,
`MeasurementSeries`, quantity-registry, storage, statistics, or GUI modules until
M0 exit criteria are satisfied and `STATE.md` explicitly opens M1.
