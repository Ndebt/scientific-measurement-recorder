# Scientific Measurement Recorder

Scientific Measurement Recorder (SMR) is an open-source, local-first application
for capturing, validating, preserving, analyzing, and exporting scientific
measurements without losing their original context.

> **Status: M0 foundation, Revision Round 2.** Only the installable package shell
> and version CLI exist. Measurement APIs shown below are design targets and do
> not run yet. M1 remains closed until the foundation PR passes CI, is reviewed,
> and is merged.

## Why

A note such as `1550, 2.4, sample17` quickly becomes unusable when its quantity,
unit, conditions, instrument, uncertainty, or source are missing. SMR turns that
observation into a traceable record while preserving the exact raw input and
requiring explicit user confirmation for every interpretation or correction.

SMR never silently changes or confirms a scientific observation.

## Scientific-data flow

```text
raw observation
-> parsed scalar/series candidate
-> explicit user confirmation of that candidate revision
-> confirmed measurement/series
-> deterministic normalization and validation
-> optional derived result
```

Validation (`pending`, `valid`, `invalid`) and lifecycle (`active`, `superseded`)
are independent. Export activity is recorded separately from scientific
provenance.

## v0.1 target

- Scalar drafts and explicitly confirmed measurements
- Batch-confirmable, named-dimension measurement series
- Pint-based unit parsing, dimensional validation, and canonical normalization
- Raw source, sample, instrument, condition, timestamp, note, and provenance
  preservation
- SQLite local record persistence without discarding external raw evidence
- Repeated-measurement mean, sample variance, sample standard deviation, and SEM
- CSV/JSON/MAT export and NumPy/pandas/xarray access
- CLI and a minimal PySide6 desktop workflow

Photonics supplies the first definitions and fixtures, while the core remains
domain-agnostic. Confidence intervals, OCR, voice, and instrument integration are
outside v0.1.

## Foundation setup

Requirements: Python 3.12 and the lock-compatible `uv` version declared in
`pyproject.toml`.

```bash
uv lock --check
uv sync --locked --dev
uv run smr version
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest --cov=smr --cov-report=term-missing
uv build
```

The optional `gui` extra is deliberately excluded from M0/M1 setup. M4 will add
a dedicated GUI install/test job.

## Planned API — not implemented

The API must expose confirmation rather than hide it. Names remain provisional
until M1:

```python
draft = MeasurementDraft.manual(
    quantity_id="photonics.optical_wavelength",
    value_text="1550",
    unit_text="nm",
)

measurement = draft.confirm(user_confirmation)
validation = validator.validate(measurement)
```

Direct construction must never turn
`Measurement(quantity=..., value=..., unit=...)` into a confirmed record through
a default or implicit confirmation.

## Repository map

```text
.
├── .github/workflows/       locked CI
├── docs/                    architecture, conceptual model, release contract
├── examples/data/           versioned, explicitly labeled fixtures
├── schemas/                 repository JSON Schema and seed definitions
├── src/smr/                 installable Python package shell
├── tests/                   M0 tests and milestone-tagged scientific matrix
├── SPEC.md                  stable product/scientific specification
├── STATE.md                 concise transient state and pending gates
├── DECISIONS.md             lasting architecture/scientific decisions
└── ROADMAP.md               sequential milestone gates
```

Read [SPEC.md](SPEC.md), [the conceptual data model](docs/DATA_MODEL.md),
[v0.1 acceptance criteria](docs/V0.1_ACCEPTANCE_CRITERIA.md), and the
[unit-validation matrix](tests/UNIT_VALIDATION_MATRIX.md) before implementation.

## Data policy

Core workflows operate offline. Scientific data stays local by default. There
is no required account, telemetry, hosted database, or mandatory external AI.
Fixtures are explicitly labeled synthetic or real with provenance. Do not commit
confidential, proprietary, unlicensed, personal, or unpublished laboratory data.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md),
and [SECURITY.md](SECURITY.md). Project code is licensed under Apache-2.0.
