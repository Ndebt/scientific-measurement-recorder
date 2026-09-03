# Conceptual Data Model

Status: M0 Revision Round 2 design baseline. M1 will implement and test runtime
types; this document freezes semantics and invariants, not Python storage types.

## Scientific-data flow

```text
RawObservation
  -> ParsedCandidate or ParsedSeriesCandidate
  -> explicit Confirmation targeting that candidate
  -> Measurement or MeasurementSeries
  -> NormalizationResult + ValidationReport
  -> optional DerivedResult
```

A convenience API may orchestrate these steps but cannot hide or invent
confirmation.

## Shared value objects

### `RawObservation`

| Field | Conceptual type | Requirement |
| --- | --- | --- |
| `observation_id` | UUID string | Stable and immutable |
| `source_type` | enum | `manual`, `array`, `csv`, `file`; later `image`, `audio`, `instrument` |
| `raw_text` | string or null | Exact lexical observation when text exists |
| `raw_payload` | JSON value or null | Original structured input when safely embeddable |
| `source_reference` | URI/path-like string or null | Reference to preserved external source |
| `sha256` | hex string or null | Source digest when available |
| `captured_at` | timezone-aware datetime | When SMR captured the source |
| `media_type` | string or null | Source media type |

At least one of `raw_text`, `raw_payload`, or `source_reference` is required.
Files/arrays preserve source bytes or payload, reference, digest, and mapping as
the authoritative lexical evidence. The observation is immutable.

### `ParsedCandidate`

| Field | Conceptual type | Requirement |
| --- | --- | --- |
| `candidate_id` | UUID string | Stable target identity |
| `candidate_revision` | positive integer | Changes create a new revision |
| `observation_id` | UUID string | Links to immutable source |
| `quantity_id` | string or null | Proposed controlled quantity |
| `value_lexeme` | string | Exact parsed lexical value |
| `unit_lexeme` | string or null | Exact parsed unit token |
| `parsed_numeric_value` | abstract finite numeric or null | Parser output; no M0 Python type mandated |
| `parser` | identifier + version | `manual`, CSV mapper, later OCR/speech parser |
| `confidence` | decimal in [0, 1] or null | Parser confidence, not scientific confidence |
| `suggestions` | ordered list | Proposed corrections with reasons |

Editing creates a new revision and retains the prior revision. Parsing never
confirms.

### `MeasurementDraft`

A scalar pre-confirmation container for one `RawObservation` and one selected
`ParsedCandidate` revision. Deterministic preview issues may be attached for the
UI, but the draft is not a `Measurement` and cannot masquerade as confirmed.

### `ParsedSeriesCandidate`

| Field | Conceptual type | Requirement |
| --- | --- | --- |
| `candidate_id` | UUID string | Batch confirmation target |
| `candidate_revision` | positive integer | Mapping/data changes create a revision |
| `observation_id` | UUID string | Raw CSV/array source |
| `source_mapping` | immutable mapping | Columns/axes to coordinates, variables, units, quantities |
| `coordinate_candidates` | ordered mapping | Includes physical and index coordinates |
| `data_variable_candidates` | ordered mapping | Parsed arrays plus semantics |
| `row_diagnostics` | ordered list | Source row/index and accepted/rejected reason |
| `parser` | identifier + version | Import/parser identity |
| `confidence` | decimal in [0, 1] or null | Mapping/parser confidence only |

One explicit confirmation can accept the complete revision and mapping. This is
batch confirmation; the user need not confirm every row. Rejected rows remain in
diagnostics and the raw source remains preserved.

### `Confirmation`

| Field | Conceptual type | Requirement |
| --- | --- | --- |
| `confirmation_id` | UUID string | Stable event identity |
| `target_type` | enum | `scalar_candidate` or `series_candidate` |
| `target_id` | UUID string | Candidate being confirmed |
| `target_revision` | positive integer | Exact accepted revision |
| `actor_type` | enum | v0.1: `user` only |
| `actor_id` | string or null | Local identity when configured |
| `confirmed_at` | timezone-aware datetime | Explicit action time |
| `accepted_fields_digest` | digest | Binds confirmation to accepted content |

A confirmation cannot target an implicit candidate, future revision, or whole
record class. Automated parsing/AI cannot be the v0.1 confirmation actor.

### `QuantityDefinition`

| Field | Conceptual type | Example |
| --- | --- | --- |
| `quantity_id` | stable namespaced string | `photonics.optical_wavelength` |
| `display_name` | string | `Optical wavelength` |
| `value_kind` | enum | `numeric`, `categorical`, `numeric_log_power_ratio_loss` |
| `physical_dimension` | normalized dimension or null | `[length]`, `dimensionless`, or null |
| `canonical_unit` | unit symbol or null | `m`, `dB`, or null |
| `accepted_conversion_policies` | non-empty ordered set | `linear_si`, `log_absolute_power_dbm` |
| `constraints` | declarative object | positive canonical wavelength |
| `allowed_values` | strings or null | controlled categorical values |
| `definition_version` | semantic version | inherited seed version in M0 |

Physical dimension is never overloaded with semantic/value type. Categorical
values have null physical dimension and canonical unit. Logarithmic power ratios
are physically dimensionless but retain explicit logarithmic semantics.

Constraints apply to canonical physical magnitude unless a rule names another
representation. A concrete `NormalizationResult` records exactly one selected
policy from the accepted list.

### `NormalizationResult`

Contains quantity-definition version, unit-registry version, selected conversion
policy, parsed numeric input, canonical numeric result, canonical unit, physical
dimension, deterministic serializer version, and any conversion diagnostics.
It never replaces source/candidate lexical fields.

M0 deliberately leaves the Python numeric class open. M1 must record a decision
before implementation. Exact lexical strings always compare exactly. Exact
declared decimal cases compare as specified; otherwise finite conversion tests
use relative tolerance `1e-12`, absolute tolerance `0` unless overridden.

### `ValidationReport`

Contains only scientific/schema validation state (`pending`, `valid`, or
`invalid`), validator and policy versions, validation timestamp, and ordered
issues. Every issue includes a stable code, severity (`info`, `warning`,
`error`), field path, observed input, rule, and actionable resolution.

### `RecordLifecycle`

Contains lifecycle status (`active` or `superseded`), status timestamp, and the
superseding record ID when applicable. Lifecycle never changes the scientific
validity of the historical record.

### Metadata value objects

- `SampleRef`: sample ID and optional type, batch, and attributes.
- `InstrumentRef`: instrument ID and optional manufacturer, model, serial number,
  calibration reference, role, and attributes.
- `Condition`: numeric quantity/value/unit or controlled categorical value;
  original/canonical separation follows the same rules.
- `Uncertainty`: optional explicitly typed Type A, Type B, combined, or expanded
  statement with value, unit, coverage information where relevant, method,
  assumptions, inputs, and provenance. Absence is not zero.

## Scientific provenance and activity

`ScientificProvenanceEvent` is append-only and limited to transformations that
affect scientific meaning or record lineage:

- `capture`;
- `parse`;
- `confirm`;
- `normalize`;
- `derive`;
- `supersede`.

It contains event ID/type, timestamp, actor/software identity, software/schema/
policy versions, input IDs/digests, and output IDs/digests.

`ExportManifest` is separate. It records export ID, time, format, software
version, immutable input record IDs/digests, output reference/digest, and status.
Creating CSV/JSON/MAT output does not mutate a scientific record or append a
scientific provenance event.

## `Measurement`

Conceptual immutable aggregate:

```text
Measurement
  record_id: UUID
  schema_version: str
  quantity_definition_id/version: str
  observation: RawObservation reference
  candidate: ParsedCandidate revision reference/snapshot
  confirmation: Confirmation
  original_value_lexeme: str
  original_unit_lexeme: str | null
  parsed_numeric_value: abstract numeric | null
  normalization: NormalizationResult | null
  observed_at: datetime | null
  created_at: datetime
  sample: SampleRef | null
  instruments: tuple[InstrumentRef, ...]
  conditions: immutable mapping[str, Condition]
  uncertainty: Uncertainty | null
  validation: ValidationReport
  lifecycle: RecordLifecycle
  scientific_provenance: tuple[ScientificProvenanceEvent, ...]
  tags: tuple[str, ...]
  notes: str | null
```

Invariants:

1. Construction requires a confirmation targeting the exact scalar candidate
   revision. There is no default confirmation.
2. `created_at` is when the confirmed measurement record is created and cannot
   precede `confirmed_at`.
3. Original lexical fields equal the confirmed candidate fields.
4. `valid` requires known quantity, parseable representation/unit, compatible
   physical dimension, permitted conversion policy, successful normalization,
   and passing constraints.
5. `observed_at` may be absent; all present datetimes are timezone-aware.
6. Missing metadata remains absence; no scientific context is invented.
7. Supersession changes lifecycle/lineage, not historical validation state.

Planned API semantics (names remain provisional until M1):

```text
draft = MeasurementDraft.manual(...)
measurement = draft.confirm(explicit_user_confirmation)
validated = validator.validate(measurement)
```

Calling `Measurement(quantity=..., value=..., unit=...)` MUST NOT silently create
a confirmed record.

## `MeasurementSeries`

Conceptual immutable aggregate:

```text
MeasurementSeries
  series_id: UUID
  schema_version: str
  name: str
  observation: RawObservation reference
  series_candidate: ParsedSeriesCandidate revision reference/snapshot
  confirmation: Confirmation(target_type=series_candidate)
  coordinates: mapping[str, Coordinate]
  data_variables: mapping[str, DataVariable]
  shared_sample: SampleRef | null
  shared_instruments: tuple[InstrumentRef, ...]
  shared_conditions: mapping[str, Condition]
  created_at: datetime
  validation: ValidationReport
  lifecycle: RecordLifecycle
  scientific_provenance: tuple[ScientificProvenanceEvent, ...]
  tags: tuple[str, ...]
  notes: str | null
```

`Coordinate` has a `coordinate_kind`:

- `physical`: values plus quantity-definition ID, original/canonical unit data,
  physical dimension, and normalization policy;
- `index`: labels/order only, with no physical quantity or unit requirement.

`DataVariable` contains values, an ordered tuple of coordinate names, quantity
definition, original/canonical representation, optional uncertainty, and
optional per-point source/record references.

Series invariants:

1. Confirmation targets the exact series candidate revision and accepts its
   batch mapping.
2. Every variable dimension names an existing coordinate and shape matches
   coordinate lengths.
3. Each physical coordinate/variable is unit-homogeneous in v0.1. Mixed units
   require explicit pre-normalization while retaining the raw source.
4. Repetition uses a named `repeat` index coordinate, not implicit row order.
5. Derived variables identify input IDs and derivation policy in scientific
   provenance.
6. xarray conversion preserves names, dimensions, shapes, quantity IDs, unit
   attributes, and representable record metadata.

## Photonics quantity mappings in v0.1

| Quantity ID | Value kind | Physical dimension | Canonical unit | Accepted policies |
| --- | --- | --- | --- | --- |
| `photonics.optical_wavelength` | numeric | `[length]` | `m` | `linear_si` |
| `photonics.optical_power` | numeric | power | `W` | `linear_si`, `log_absolute_power_dbm` |
| `photonics.transmission` | numeric ratio | dimensionless | `1` | `linear_ratio` |
| `photonics.loss` | logarithmic power-ratio loss | dimensionless | `dB` | `log_power_ratio_loss_db` |
| `electronics.laser_current` | numeric | `[current]` | `A` | `linear_si` |
| `environment.temperature` | numeric temperature point | `[temperature]` | `K` | `temperature_point` |
| `environment.temperature_interval` | numeric temperature interval | `[temperature]` | `K` | `temperature_interval` |
| `photonics.polarization` | controlled categorical text | null | null | `controlled_text` |

For optical loss, `loss_dB = 10 * log10(P_in / P_out)` and an explicitly derived
linear transmission is `P_out / P_in = 10 ** (-loss_dB / 10)`. `dBm` represents
absolute power referenced to 1 mW and normalizes only through
`log_absolute_power_dbm`.
