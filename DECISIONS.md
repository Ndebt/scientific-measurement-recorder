# Architecture and Scientific Decisions

This file records decisions with lasting architectural or scientific impact.
Status values are `proposed`, `accepted`, `superseded`, or `rejected`.

## ADR-0001 — Python package and repository layout

- **Status:** accepted
- **Date:** 2026-09-03
- **Decision:** Use Python 3.12, `uv`, PEP 621 metadata, Hatchling, and a `src/`
  layout with import package `smr`. Tests, schemas, examples, and architecture
  documents remain top-level concerns.
- **Rationale:** The `src/` layout prevents accidental imports from the checkout;
  PEP 621 and `uv` keep packaging reproducible without coupling runtime code to
  a build backend.
- **Consequences:** CI must test an installed package. The distribution name is
  `scientific-measurement-recorder`; the concise Python namespace is `smr`.

## ADR-0002 — Core boundaries and dependency direction

- **Status:** accepted
- **Date:** 2026-09-03
- **Decision:** The measurement core is a UI- and adapter-independent Python
  package. Input adapters, persistence, exports, CLI, and GUI depend inward on
  core interfaces; core never imports GUI, OCR, speech, or instrument adapters.
- **Rationale:** Scientific validation must remain deterministic, reusable, and
  testable without optional hardware or heavyweight interfaces.
- **Consequences:** PySide6 is an optional dependency. OCR and speech packages
  are deferred beyond v0.1 and live behind adapters.

## ADR-0003 — Immutable observations and append-only provenance

- **Status:** accepted
- **Date:** 2026-09-03
- **Decision:** Raw observations are immutable. Parsing, confirmation,
  normalization, correction, and derivation append typed provenance events and
  create new representations/records; they never overwrite the source.
- **Rationale:** Traceability is a scientific invariant, not an audit feature.
- **Consequences:** The record store and lossless record serializations retain
  source lexical values, references, confirmation, conversion policy, and
  transformation history. Export activity itself is handled separately by
  ADR-0015.

## ADR-0004 — Pydantic at boundaries, Pint for units

- **Status:** accepted
- **Date:** 2026-09-03
- **Decision:** Pydantic v2 validates serializable domain boundaries. Pint is the
  unit parser/converter. Pint objects do not become the canonical persisted
  format; normalized magnitudes, canonical unit symbols, dimensionality, and
  registry/policy versions are serialized explicitly.
- **Rationale:** This provides strict validation and predictable JSON/SQLite
  round trips while retaining established unit semantics.
- **Consequences:** M1 must define one configured registry owned by SMR and must
  test registry-version-sensitive behavior.

## ADR-0005 — Quantity registry is domain-extensible

- **Status:** accepted
- **Date:** 2026-09-03
- **Decision:** Quantity definitions map stable identifiers to value semantics,
  physical dimensionality (or null for non-physical values), canonical units,
  and accepted conversion policies. The generic core owns the mechanism;
  photonics is supplied as versioned definitions, schemas, examples, and later
  adapters.
- **Rationale:** Unit dimensionality alone cannot distinguish all scientific
  meanings (for example wavelength versus displacement), while hard-coded
  photonics concepts would violate the domain-agnostic core.
- **Consequences:** A dimensionally compatible value may still fail quantity
  policy. Changes to quantity definitions are versioned.

## ADR-0006 — Logarithmic quantities require explicit policies

- **Status:** accepted
- **Date:** 2026-09-03
- **Decision:** v0.1 distinguishes absolute logarithmic power (`dBm`) from
  logarithmic ratios (`dB`). `dBm` may normalize to watts only through the
  explicit formula `P_W = 10 ** ((P_dBm - 30) / 10)` with the original retained.
  `dB` is a ratio and cannot be converted to watts without a reference power and
  declared semantics. Generic linear conversion is forbidden for both.
- **Rationale:** Treating logarithmic quantities as ordinary units creates
  scientifically invalid arithmetic and conversions.
- **Consequences:** Optical loss declares power-ratio loss semantics using
  `10 * log10(P_in / P_out)`. Dedicated conversion-policy IDs and regression
  tests are required.

## ADR-0007 — Temperature points and intervals are different types

- **Status:** accepted
- **Date:** 2026-09-03
- **Decision:** Absolute temperatures (for example `degC`) use offset-aware
  conversion to kelvin; temperature intervals use delta units and multiplicative
  conversion. They cannot be interchanged implicitly.
- **Rationale:** Conflating 25 degC with a 25 degC interval yields incorrect
  canonical values.
- **Consequences:** Quantity definitions and APIs must identify point versus
  interval semantics before conversion.

## ADR-0008 — MeasurementSeries follows xarray concepts

- **Status:** accepted
- **Date:** 2026-09-03
- **Decision:** Series consist of named coordinates, named data variables, and
  explicit dimension references. Units and quantity IDs are per coordinate or
  variable; shared and per-point provenance remain representable.
- **Rationale:** Named dimensions avoid positional ambiguity and enable natural
  NumPy/pandas/xarray interoperability.
- **Consequences:** Shapes must be validated against named dimensions, and CSV
  is a documented projection rather than the authoritative series format.

## ADR-0009 — SQLite persistence behind repositories

- **Status:** accepted
- **Date:** 2026-09-03
- **Decision:** SQLite is the authoritative v0.1 SMR record store, accessed
  through repository interfaces. It does not replace external raw evidence;
  source payloads/references/digests remain part of the record contract. Schema
  migrations are forward, transactional, and backed up before destructive
  transformations; reliable restore/recovery is required, not reversible down
  migrations. JSON payloads may hold evolving metadata while indexed
  identity/state fields remain relational.
- **Rationale:** This keeps local deployment simple while preventing storage
  details from leaking into the scientific domain model.
- **Consequences:** M2 must test migrations, transactions, and lossless
  serialization round trips.

## ADR-0010 — Synthetic fixture labeling

- **Status:** accepted
- **Date:** 2026-09-03
- **Decision:** The initial WG-17 photonics fixture is synthetic and MUST be
  labeled as such in file metadata and documentation. It is a validation example,
  not empirical data.
- **Rationale:** Example data must not be mistaken for scientific evidence.
- **Consequences:** Future real datasets require provenance, permission, and
  de-identification/license review before inclusion.

## ADR-0011 — Validation state and record lifecycle are orthogonal

- **Status:** accepted
- **Date:** 2026-09-04
- **Decision:** Validation state is limited to `pending`, `valid`, and `invalid`.
  Lifecycle status is separately `active` or `superseded`.
- **Rationale:** Supersession describes lineage/currentness, not scientific or
  schema validity.
- **Consequences:** A valid historical record can be superseded while remaining
  valid. Storage, queries, UI, and exports must not collapse the two axes.

## ADR-0012 — Confirmation targets a candidate revision

- **Status:** accepted
- **Date:** 2026-09-04
- **Decision:** A confirmation records `target_type`, `target_id`, and
  `target_revision`. Scalar drafts and parsed series candidates are distinct
  targets. One user action may confirm a complete series candidate and mapping.
- **Rationale:** Hidden/default confirmation violates observation integrity, while
  per-row confirmation makes valid CSV/array workflows unusable.
- **Consequences:** A final `Measurement` or `MeasurementSeries` cannot be
  created without explicit user confirmation of an exact candidate revision.

## ADR-0013 — Quantity semantics are separate from physical dimension

- **Status:** accepted
- **Date:** 2026-09-04
- **Decision:** `QuantityDefinition` separately declares `value_kind`,
  `physical_dimension`, `canonical_unit`, and a list of
  `accepted_conversion_policies`. Each normalization records one selected policy.
- **Rationale:** `categorical` and logarithmic ratio semantics are not SI
  dimensions. One physical quantity may accept linear and logarithmic input
  representations.
- **Consequences:** Polarization has null physical dimension/unit. Optical loss
  is dimensionless with explicit logarithmic power-ratio-loss semantics. Optical
  power accepts both linear SI and absolute dBm policies.

## ADR-0014 — Runtime resources live inside the installed distribution

- **Status:** accepted
- **Date:** 2026-09-04
- **Decision:** Any quantity definitions or schemas required at runtime must be
  packaged inside `smr` and loaded with a supported package-resource API. The
  top-level `schemas/` directory remains a repository/specification and M0 test
  artifact.
- **Rationale:** Installed wheels cannot assume a source checkout or repository
  relative path exists.
- **Consequences:** M1 must copy/generate validated runtime resources into the
  package and test access from an isolated installed wheel; it must not read
  `../../schemas`.

## ADR-0015 — Scientific provenance excludes export activity

- **Status:** accepted
- **Date:** 2026-09-04
- **Decision:** Scientific provenance records capture, parse, confirm, normalize,
  derive, and supersede events. Export operations create separate immutable
  export manifests/activity records referencing input record IDs/digests and
  output digest/location.
- **Rationale:** Writing a CSV, JSON, or MAT file does not change scientific
  meaning and must not mutate an immutable measurement.
- **Consequences:** Export history remains auditable without contaminating record
  lineage or changing record digests.

## ADR-0016 — Package version has one source

- **Status:** accepted
- **Date:** 2026-09-04
- **Decision:** `src/smr/_version.py` is the sole version source. PEP 621 declares
  the version dynamic and Hatchling reads that file. Tests compare module and
  installed distribution metadata.
- **Rationale:** Duplicating version literals in `pyproject.toml` and Python code
  permits silent divergence.
- **Consequences:** Release changes update only `_version.py`; build and smoke
  tests must prove wheel metadata and `smr.__version__` agree.
