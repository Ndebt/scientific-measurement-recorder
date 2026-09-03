# Scientific Measurement Recorder Specification

Status: M0 Revision Round 2 baseline

Target release: v0.1

Normative language: MUST, MUST NOT, SHOULD, and MAY are requirements.

## 1. Mission

Scientific Measurement Recorder (SMR) is an open-source, local-first capture and
validation layer for scientific measurements. It turns laboratory observations
into structured, reusable records without erasing, silently changing, or
silently confirming the original observation.

Photonics is the v0.x reference domain. The core data model and validation
mechanism remain domain-agnostic.

## 2. Product boundary

SMR implements this scientific-data flow:

`raw observation -> parsed candidate/draft -> explicit user confirmation -> confirmed measurement -> deterministic normalization and validation -> derived result`

Pre-confirmation validation previews MAY help a user resolve errors, but they do
not create a confirmed `Measurement` or `MeasurementSeries`.

The core MUST be usable as a normal Python package and MUST NOT import the
desktop UI, CLI, SQLite adapter, CSV adapter, exporters, OCR, speech, instrument
adapters, or cloud services.

v0.1 includes:

- scalar and array/series measurement entry;
- physical-quantity naming and expected-dimensionality validation;
- immutable original lexical/source representations;
- parsed and canonical numeric representations;
- sample, instrument, timestamp, conditions, notes, tags, and provenance;
- repeated-measurement descriptive statistics;
- CSV import and CSV/JSON/MAT export;
- NumPy, pandas, and xarray access;
- SQLite local record persistence;
- CLI, minimal desktop GUI, and automated tests.

v0.1 excludes instrument control, OCR, speech, cloud synchronization, telemetry,
collaboration services, plugin marketplaces, LIMS/ELN functionality, confidence
intervals, and automatic correction of scientific observations.

## 3. Scientific invariants

### 3.1 Observation integrity

SMR MUST keep these concepts distinct:

1. raw observation;
2. parsed scalar or series candidate/draft;
3. explicit user confirmation;
4. confirmed measurement or measurement series;
5. canonical representation and deterministic validation report;
6. derived result.

Raw observations and their source references/digests MUST be immutable after
capture. Corrections create new candidates and confirmation events. A corrected
confirmed record supersedes rather than overwrites an earlier record.

Canonical values MUST be reproducible from the confirmed interpretation, the
quantity-definition version, the unit-registry version, and the selected
conversion policy. Canonical values never replace original values.

### 3.2 Explicit confirmation

Candidate construction MUST NOT silently create a confirmed measurement. A
confirmation targets a specific candidate ID and target type. v0.1 confirmation
is an explicit user action.

CSV and array workflows MUST support one explicit confirmation of a complete
series candidate and its mapping. Per-row confirmation is not required when the
user confirms the batch interpretation. The raw file/array and mapping
provenance remain preserved.

### 3.3 Validation and lifecycle

Scientific/schema validation state is exactly:

- `pending`: validation is incomplete or confirmation/required input is absent;
- `valid`: all required deterministic checks passed;
- `invalid`: at least one error-level deterministic check failed.

Record lifecycle status is separate:

- `active`;
- `superseded`.

A historically valid record MAY be superseded while its validation state remains
`valid`. Supersession MUST NOT rewrite its scientific validation history.

### 3.4 Deterministic authority

Unit parsing, dimensional compatibility, normalization, constraints, and schema
validation MUST be deterministic. AI-generated extraction MAY create candidates
but MUST NOT confirm measurements, fabricate metadata or uncertainty, remove
outliers, or replace source data.

### 3.5 Numeric and lexical fidelity

Where lexical input exists, its exact text (for example `1.5500e3` and `µm`) MUST
remain recoverable. For files and arrays, preserved source bytes or payload,
reference, digest, and import mapping are authoritative evidence of the original
representation.

The conceptual contract distinguishes:

- original lexical/source representation;
- parsed numeric representation;
- canonical numeric representation;
- deterministic persisted/exported serialization.

M0 does not mandate an unjustified Python numeric implementation. M1 MUST record
the chosen numeric/serialization policy before implementation. Deterministic
tests compare exact strings and exact decimal transformations where specified;
otherwise finite numeric conversions use relative tolerance `1e-12` and absolute
tolerance `0`, unless a case documents another tolerance. Non-finite inputs are
invalid by default.

### 3.6 Metrology

Terminology SHOULD follow the current SI Brochure and GUM concepts. Arithmetic
mean, sample variance, sample standard deviation, standard error, Type A
standard uncertainty, Type B uncertainty, combined standard uncertainty, and
expanded uncertainty MUST remain semantically distinct.

SMR MUST NOT label descriptive variability or SEM as measurement uncertainty
without a declared uncertainty model, required assumptions, and inputs.
Unsupported uncertainty calculations return an actionable outcome, never an
invented value.

## 4. Domain concepts

### 4.1 `MeasurementDraft`

A scalar pre-confirmation object referencing one immutable `RawObservation` and
one `ParsedCandidate`. It may contain deterministic validation previews but is
not a scientific measurement and cannot be persisted as confirmed.

### 4.2 `ParsedSeriesCandidate`

A pre-confirmation series interpretation containing named coordinate and data
variable candidates, source-to-field mapping, row diagnostics, raw file/array
reference or payload, digest where available, and parser version. One user
confirmation may accept the candidate as a batch.

### 4.3 `Confirmation`

A confirmation identifies `target_type` (`scalar_candidate` or
`series_candidate`), `target_id`, user actor, timestamp, and the exact accepted
candidate revision. It cannot target an unversioned or implicit object.

### 4.4 `Measurement`

A confirmed scalar interpretation linked to its source, candidate, confirmation,
original representation, optional canonical representation, metadata,
validation report, lifecycle status, and scientific provenance. Construction
requires an explicit confirmation; no public constructor default may fabricate
one.

### 4.5 `MeasurementSeries`

A confirmed xarray-compatible set of named coordinates and dependent variables,
created from a confirmed `ParsedSeriesCandidate`. Every scientific coordinate
and variable carries quantity, unit/representation semantics, and provenance.
Index coordinates such as `repeat` MAY be explicitly typed as non-physical
indexes and need no `QuantityDefinition`.

### 4.6 `QuantityDefinition`

A versioned definition contains:

- stable quantity ID and display name;
- value kind/representation semantics;
- physical dimension, or null for non-physical categorical values;
- canonical representation unit, or null when units do not apply;
- a non-empty list of accepted conversion-policy IDs;
- declarative constraints and controlled values where applicable.

Physical dimension describes only physical dimensionality. It MUST NOT contain
categorical or logarithmic-representation labels masquerading as dimensions.

A specific normalization records one selected conversion policy. Optical power
accepts both linear power and explicit `dBm` policies. Optical loss is physically
dimensionless but semantically a logarithmic POWER-ratio loss using
`10 * log10(P_in / P_out)`. It is not an amplitude-ratio policy. `dBm` is
absolute logarithmic power referenced to 1 mW.

### 4.7 Reports and records

`ValidationReport` contains validation state, validator/policy versions,
timestamp, and ordered issues with stable code, severity, field path, observed
input, violated rule, and actionable resolution.

`ScientificProvenanceEvent` covers scientific/data transformations only:
capture, parse, confirm, normalize, derive, and supersede. It is append-only.

`ExportManifest` or activity records separately describe export format,
timestamp, software version, immutable input record IDs/digests, output
location/reference, and output digest. Exporting MUST NOT mutate scientific
records or append a scientific provenance event merely because a file was
written.

## 5. Functional requirements

### Capture and confirmation

- **FR-001** Manual scalar entry MUST create a `MeasurementDraft` containing
  quantity, value, and unit candidates and preserve original lexical forms.
- **FR-002** Only an explicit user confirmation targeting that draft/candidate
  MAY create a `Measurement`.
- **FR-003** Series entry MUST accept homogeneous numeric arrays plus named
  coordinates, units, dimensions, and source mapping as a
  `ParsedSeriesCandidate`.
- **FR-004** CSV import MUST preserve the source reference/digest and import
  mapping and report row-level failures without silently dropping rows.
- **FR-005** One explicit batch confirmation MAY create a `MeasurementSeries`
  from a complete series candidate.
- **FR-006** Missing or ambiguous required units remain pending or invalid until
  explicitly resolved.
- **FR-007** Candidate corrections preserve source text, earlier candidate,
  suggestion/confidence, and the final targeted confirmation.

### Units, dimensions, and representations

- **FR-010** Pint is the unit engine; SMR owns quantity definitions, canonical
  unit policy, ambiguity policy, and logarithmic conversion policies.
- **FR-011** A confirmed quantity/unit pair MUST match the quantity's physical
  dimensionality before validation may be `valid`.
- **FR-012** Linear conversion preserves original representation and writes a
  separate canonical representation.
- **FR-013** Absolute temperatures and temperature intervals use distinct
  quantity definitions and policies and cannot be interchanged implicitly.
- **FR-014** `dBm` normalization uses
  `P_W = 10 ** ((P_dBm - 30) / 10)` and records the absolute-log-power policy.
- **FR-015** `dB` optical loss uses the declared power-ratio-loss policy and MUST
  NOT be converted to watts by generic unit conversion.
- **FR-016** Validation and normalization results are deterministic across
  persistence round trips within the recorded schema/policy versions.

### Metadata and evidence

- **FR-020** Confirmed records contain stable ID, timezone-aware record creation
  time, source type, raw source/payload/reference, confirmation, validation state,
  lifecycle status, and scientific provenance.
- **FR-021** Observed time, sample, instrument, conditions, uncertainty, notes,
  and tags MAY be absent only when optional; absence is never inferred data.
- **FR-022** External raw files SHOULD be content-addressed with SHA-256 when
  practical. A missing external file MUST NOT erase its retained reference or
  digest.
- **FR-023** Supersession creates a lifecycle/provenance event and leaves the
  earlier record's observation, confirmation, canonical result, and validation
  result intact.

### Persistence and interoperability

- **FR-030** SQLite is the authoritative local v0.1 SMR record store, not a
  replacement for external raw scientific evidence. It preserves source
  payloads where embedded and always preserves references/digests/provenance.
- **FR-031** JSON export is lossless for the versioned SMR record schema.
- **FR-032** CSV export is documented as a tabular projection and uses a sidecar
  when needed to prevent context loss.
- **FR-033** NumPy, pandas, and xarray conversions preserve values, shapes,
  coordinate names, and representable quantity/unit metadata.
- **FR-034** MAT export produces a loadable file containing values, coordinates,
  units, and essential metadata.
- **FR-035** Every export creates a separate export manifest/activity record and
  does not mutate scientific provenance.

### Statistics

- **FR-040** Repeated numeric observations expose arithmetic mean, sample
  variance, sample standard deviation (`ddof=1`), and SEM.
- **FR-041** Sample variance, sample standard deviation, and SEM require at least
  two observations; insufficient input produces an explicit outcome.
- **FR-042** Statistics reject dimensionally heterogeneous series unless values
  are explicitly converted to a common compatible unit first.
- **FR-043** Default statistics include all confirmed values. Exclusion requires
  a provenance-linked derived series with user reason and excluded IDs.
- **FR-044** Confidence intervals are deferred beyond v0.1 until method,
  assumptions, degrees of freedom, edge cases, units, and reference tests are
  specified.

### Interfaces

- **FR-050** The planned Python API MUST make confirmation explicit, for example:

  ```python
  draft = MeasurementDraft.manual(
      quantity_id="photonics.optical_wavelength",
      value_text="1550",
      unit_text="nm",
  )
  measurement = draft.confirm(user_confirmation)
  result = validator.validate(measurement)
  ```

  Names remain design-level until M1; hidden auto-confirmation is forbidden.
- **FR-051** The CLI supports draft/create, confirm, validate, list/show, import,
  statistics, and export workflows without requiring the GUI.
- **FR-052** The desktop MVP supports capture -> preview -> explicit confirmation
  -> deterministic validation -> metadata/save -> view/statistics -> export.

## 6. Non-functional requirements

- **NFR-001 Local first:** Core capture, confirmation, validation, persistence,
  statistics, and export work offline without an account.
- **NFR-002 Privacy:** No telemetry or network transmission is enabled by
  default.
- **NFR-003 Reproducibility:** Schemas, quantity definitions, conversion policy,
  unit-registry version, and software version are recorded where they affect
  results.
- **NFR-004 Testability:** Scientific rules have deterministic tests; every fixed
  scientific defect receives a regression test.
- **NFR-005 Compatibility:** Python 3.12 is the initial supported interpreter.
  Other operating systems are supported only after their CI jobs pass.
- **NFR-006 Licensing:** Project code is Apache-2.0. Dependency license
  compatibility is reviewed before release.
- **NFR-007 Actionability:** Validation issues identify field, rule, observed
  input, and practical resolution.
- **NFR-008 Packaging:** Runtime resources are installed inside the `smr`
  distribution and accessed through supported package-resource APIs. Runtime
  code MUST NOT assume the repository's top-level `schemas/` directory exists.

## 7. v0.1 release contract

The normative release gates are in `docs/V0.1_ACCEPTANCE_CRITERIA.md`. Release
requires every mandatory criterion to pass in its declared milestone and no
unresolved critical defect capable of silently corrupting, changing, losing, or
materially misrepresenting scientific data.

## 8. Reference fixture

The first fixture is the explicitly synthetic
`examples/data/photonics_wg17_spectral_sweep.csv` with its metadata sidecar. It
tests a batch `ParsedSeriesCandidate` and targeted series confirmation. It is not
experimental evidence.

## 9. Versioning and change control

Stored records include schema and policy versions. Breaking schema or scientific
semantic changes require a migration plan and decision record. Stable
requirements live in `SPEC.md`, lasting decisions in `DECISIONS.md`, milestone
scope in `ROADMAP.md`, and transient state in `STATE.md`.
