# Roadmap

Milestones are sequential quality gates. Later work may be specified, but its
implementation does not begin until the current gate closes.

## M0 — Foundation (complete)

Goal: establish a trustworthy, installable project shell and freeze enough of
the scientific contract to begin the core safely.

Current execution order:

1. Complete independent technical/scientific R2 findings across canonical docs,
   schema, fixture, tests, package metadata, and CI.
2. Generate `uv.lock` only from final `pyproject.toml` and verify locked install.
3. Run Work-environment Python 3.12 checks and create the R2 archive.
4. Import R2 into the owner's existing local `m0/foundation` branch.
5. Inspect the local diff and run owner-local locked checks.
6. Commit and push the reviewed R2 foundation.
7. Open a PR linked to GitHub issue #1; run CI and review the complete diff.
8. Fix important findings, rerun gates, merge, and update canonical state.
9. Open M1 only after every M0 exit criterion is true.

Exit criteria:

- [x] GitHub tracking issue #1 exists.
- [x] Owner-local branch `m0/foundation` exists.
- [x] Initial foundation documents, conceptual models, acceptance criteria,
  validation matrix, and synthetic photonics fixture were drafted.
- [x] Independent technical/scientific review was completed.
- [x] R2 contract and foundation assets are revised in the package workspace.
- [x] R2 passes Work-environment Python 3.12 lock, core/dev sync, format, lint,
  type, test, build, isolated-wheel import, version, and CLI checks.
- [x] R2 package is imported into the owner's local branch.
- [x] Owner-local Python 3.12 lock, sync, import, CLI, format, lint, type, test,
  build, and isolated-wheel checks pass.
- [x] The revised branch is pushed.
- [x] CI passes for the revised PR.
- [x] The foundation PR is reviewed and merged.
- [x] `STATE.md` records M0 complete and explicitly opens M1.

M1 is open.

## M1 — Measurement core (current)

Deliver runtime `MeasurementDraft`, `ParsedCandidate`,
`ParsedSeriesCandidate`, targeted `Confirmation`, `Measurement`, and
`MeasurementSeries` models; quantity registry; Pint integration; dimensional
validation; raw/parsed/canonical separation; lifecycle separation; and
deterministic tests.

M1 must pass all cases tagged `M1` in `tests/UNIT_VALIDATION_MATRIX.md`. M2/M3
cases in that matrix are frozen contracts, not M1 deliverables.

Exit: all M1 scientific-validation acceptance criteria pass with no unresolved
critical defect capable of silently corrupting, changing, losing, or materially
misrepresenting scientific data.

## M2 — Storage and export

Deliver SQLite repositories and forward migrations with backup/recovery, CSV
import/export, lossless JSON, NumPy/pandas/xarray conversion, MATLAB MAT export,
and separate export manifests/activity records.

Exit: all M2-tagged persistence, import, export, fixture, and round-trip cases
pass without discarding external raw-source references or digests.

## M3 — Statistics

Deliver arithmetic mean, sample variance, sample standard deviation, and SEM,
clearly separated from Type A/Type B/combined/expanded uncertainty.

Confidence intervals are deferred beyond v0.1 until their method, assumptions,
degrees of freedom, edge cases, unit behavior, and deterministic reference tests
are specified.

Exit: all M3-tagged formulas, edge cases, units, and derived-result provenance
pass deterministic reference tests.

## M4 — Desktop MVP

Deliver the minimal PySide6 workflow: capture, preview, explicit confirmation,
validate, add metadata, save, view series/statistics, and export. Add a dedicated
GUI dependency/test job; do not burden core M0/M1 CI with PySide6.

Exit: a photonics researcher completes the v0.1 end-to-end workflow locally
without using Python directly or encountering hidden confirmation.

## M5 — Voice (v0.1.1)

Add a local faster-whisper adapter, voice-to-candidate parsing, targeted
confirmation UI, and preserved raw audio. Voice never bypasses confirmation.

## M6 — OCR (v0.2)

Add a local PaddleOCR adapter, photograph preservation, candidate extraction,
confidence display, and targeted confirmation workflow.

## Later releases

- **v0.3:** richer GUM-aware uncertainty, explicitly specified confidence
  interval support if justified, additional visualization, HDF5/NetCDF, and
  enhanced provenance.
- **v0.4:** begin controlled instrument-adapter research (for example PyVISA,
  optical spectrum analyzers, power meters, oscilloscopes) only after earlier
  milestones are stable.

Explicitly out of scope: general ELN/LIMS, cloud collaboration, broad plugin
marketplace, AI chatbot, autonomous lab, and generic instrument-control platform.
