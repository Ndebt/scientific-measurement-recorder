# Contributing

Thank you for helping make scientific measurements more trustworthy and reusable.

## Start here

Read `SPEC.md`, `STATE.md`, `DECISIONS.md`, `ROADMAP.md`, and `AGENTS.md`. Open or
identify an issue before meaningful work. Confirm that the issue belongs to the
current milestone; later-milestone implementation will not be merged early.

## Development

Use Python 3.12 and `uv`:

```bash
uv lock --check
uv sync --locked --dev
uv run ruff format .
uv run ruff check .
uv run mypy
uv run pytest --cov=smr --cov-report=term-missing
uv build
```

M0/M1 development does not install optional GUI dependencies. M4 will own a
dedicated `gui` extra job. Before opening a PR, `uv lock --check` and
`uv sync --locked --dev` must succeed without modifying `uv.lock`; regenerate
the lock with `uv lock` only after an intentional `pyproject.toml` dependency or
metadata change.

Pull requests should be focused, describe scientific assumptions, link their
issue, and include tests. If behavior changes a stable requirement or lasting
decision, update the canonical document in the same PR.

## Scientific changes

- Include authoritative references for metrology or unit semantics when relevant.
- Provide deterministic test vectors and tolerances.
- Preserve raw inputs and provenance in fixtures and implementations.
- Mark synthetic datasets as synthetic; do not commit confidential, personal,
  proprietary, or unlicensed laboratory data.
- Do not commit secrets, unpublished laboratory data, or source files without
  documented permission and license.
- A corrected scientific defect requires a regression test.

## Commit and review expectations

Use concise imperative commit messages. Before requesting review, run all quality
checks locally. Reviewers prioritize scientific correctness, data preservation,
API clarity, dependency direction, privacy, and test coverage over feature count.

By contributing, you agree that your contributions are licensed under Apache-2.0
and that you have the right to submit them.
