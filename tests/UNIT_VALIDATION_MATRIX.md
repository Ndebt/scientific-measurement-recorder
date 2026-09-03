# Unit and Dimensional Validation Matrix

This M0 document freezes deterministic contracts for later milestones; it does
not authorize their implementation. `ROADMAP.md` requires M1 to pass only rows
tagged M1, M2 to pass M2 rows, and M3 to pass M3 rows.

Original lexical/source fields remain unchanged in every case, including
failures. Exact declared decimal cases compare exactly. Other finite numeric
conversions use relative tolerance `1e-12` and absolute tolerance `0` unless the
case specifies otherwise.

## Quantity fixtures

Production quantity IDs refer to `schemas/quantity-definitions.v0.1.json`.
Generic conversion-engine cases use test-only definitions and MUST NOT be added
to the photonics production seed merely to satisfy tests:

| Test-only quantity ID | Value kind | Physical dimension | Canonical unit | Policy |
| --- | --- | --- | --- | --- |
| `test.area_normalized_power` | numeric | power / area | `W/m^2` | `linear_si` |
| `test.speed` | numeric | length / time | `m/s` | `linear_si` |

The `repeat` coordinate is an index coordinate and intentionally has no
`QuantityDefinition`.

## Conversion and validation cases

| ID | Milestone | Quantity | Original input | Expected result | Required assertion |
| --- | --- | --- | --- | --- | --- |
| LIN-001 | M1 | optical wavelength | `1550 nm` | valid; `1.55e-6 m` | length dimension; selected policy `linear_si`; lexical `1550`/`nm` retained |
| LIN-002 | M1 | optical wavelength | `1.55 µm` | valid; `1.55e-6 m` | Unicode micro sign retained |
| LIN-003 | M1 | optical wavelength | `1.55 um` | valid; `1.55e-6 m` | accepted ASCII alias retained as `um` |
| LIN-004 | M1 | optical power | `2.4 mW` | valid; `0.0024 W` | power dimension; `linear_si` |
| LIN-005 | M1 | laser current | `80 mA` | valid; `0.08 A` | current dimension |
| LIN-006 | M1 | `test.area_normalized_power` | `2.4 mW/mm^2` | valid; `2400 W/m^2` | test-only definition; compound exponents converted |
| LIN-007 | M1 | `test.speed` | `3.6 km/h` | valid; `1 m/s` | test-only definition; numerator/denominator converted |
| LIN-008 | M1 | transmission | `0.80 1` | valid; `0.80 1` | dimensionless physical ratio; `linear_ratio` |
| DIM-001 | M1 | optical wavelength | `2.4 mW` | invalid | `unit.dimension_mismatch`; no canonical result |
| DIM-002 | M1 | optical power | `1550 nm` | invalid | `unit.dimension_mismatch` |
| DIM-003 | M1 | laser current | `2 V` | invalid | current versus potential mismatch |
| DIM-004 | M1 | transmission | `0.8 W` | invalid | dimensional input rejected |
| DIM-005 | M1 | unknown quantity | `1 m` | pending | `quantity.unknown`; dimension alone does not infer meaning |
| UNIT-001 | M1 | optical wavelength | value `1550`, unit absent | pending | `unit.missing`; no invented `nm` |
| UNIT-002 | M1 | temperature point | `25 C` | pending/invalid | `unit.ambiguous_alias`; require explicit `degC` or `K` |
| UNIT-003 | M1 | optical wavelength | `1550 u` | pending/invalid | unknown/ambiguous unit; no inferred `µm` |
| UNIT-004 | M1 | optical power | `2.4 milliwatt` | valid; `0.0024 W` | Pint long name accepted; original spelling retained |
| UNIT-005 | M1 | optical wavelength | `1 meter` | valid; `1 m` | canonical symbol stored separately |
| TEMP-001 | M1 | temperature point | `25 degC` | valid; `298.15 K` | offset-aware `temperature_point`; exact declared decimal |
| TEMP-002 | M1 | temperature point | `77 degF` | valid; `298.15 K` | offset-aware point conversion |
| TEMP-003 | M1 | temperature interval | `5 delta_degC` | valid; `5 K` | `environment.temperature_interval`; multiplicative policy |
| TEMP-004 | M1 | temperature interval | `5 degC` | invalid | point unit cannot silently become interval |
| TEMP-005 | M1 | temperature point | `-1 K` | invalid | `quantity.constraint`; canonical absolute-temperature bound |
| LOG-001 | M1 | optical power | `0 dBm` | valid; `0.001 W` | `log_absolute_power_dbm`, reference 1 mW; not generic linear |
| LOG-002 | M1 | optical power | `30 dBm` | valid; `1 W` | explicit absolute-log formula |
| LOG-003 | M1 | optical power | `-30 dBm` | valid; `1e-6 W` | canonical constraint applies to watts, not dBm sign |
| LOG-004 | M1 | optical power | `0 dB` | invalid | ratio is not absolute power; never watts |
| LOG-005 | M1 | optical loss | `3 dB` | valid; canonical `3 dB` | dimensionless POWER-ratio loss; `log_power_ratio_loss_db` |
| LOG-006 | M1 | optical loss | `3 dBm` | invalid | absolute log power is not a loss ratio |
| ARR-001 | M1 | wavelength coordinate | `[1550, 1551] nm` | valid; `[1.55e-6, 1.551e-6] m` | element order/shape and raw source retained |
| ARR-002 | M1 | optical power | `[2.4, 2.5, 2.6] mW` | valid; `[0.0024, 0.0025, 0.0026] W` | homogeneous unit |
| ARR-003 | M1 | optical power | `[2.4 mW, 0.0025 W]` in one raw array | pending/invalid in v0.1 | explicit pre-normalization required; raw source retained |
| ARR-004 | M1 | series dimensions | coordinate length 3, variable shape 4 | invalid | `series.shape_mismatch` |
| ARR-005 | M1 | numeric array | `[1.0, NaN] mW` | invalid by default | issue identifies index; no dropped element |
| RAW-001 | M1 | wavelength | `1.5500e3 nm` | valid; `1.55e-6 m` | exact value lexeme `1.5500e3` survives normalization |
| RAW-002 | M1 | corrected OCR candidate | raw `l550 nm`, proposed `1550 nm` | pending until explicit confirmation | both candidate revisions/confidence retained; confirmation targets accepted revision |
| SER-001 | M2 | scalar JSON/SQLite round trip | full valid/active record | equivalent record | both states, IDs, lexical/canonical fields, confirmation target, metadata, provenance equal |
| SER-002 | M2 | series JSON/SQLite round trip | WG-17 fixture | equivalent series | candidate mapping, confirmation, shapes, units, dimensions, metadata equal |
| SER-003 | M1 | validation repeat | same input and versions twice | equivalent reports | validation state and issue codes equal; validation timestamps excluded from equivalence |

## Reference statistics cases

These M3 cases validate unit propagation and forbid relabeling variability as
measurement uncertainty.

| ID | Milestone | Values | Unit | Expected |
| --- | --- | --- | --- | --- |
| STAT-001 | M3 | `[1, 2, 3]` | `mW` | mean `2 mW`; sample variance `1 mW^2`; sample SD `1 mW`; SEM `1/sqrt(3) mW` |
| STAT-002 | M3 | `[2.4]` | `mW` | mean `2.4 mW`; variance/SD/SEM explicit insufficient-data outcome |
| STAT-003 | M3 | `[]` | `mW` | every statistic explicit insufficient-data outcome |
| STAT-004 | M3 | `[2.4 mW, 0.0025 W]` after explicit conversion | `W` | mean `0.00245 W`; source units remain inspectable |

No confidence-interval case belongs to v0.1. Type A, Type B, combined, and
expanded uncertainty require separate declared models and inputs; none is an
alias for these descriptive statistics.

## Reference fixture checks

All cases in this subsection belong to M2 implementation even though M0 freezes
and structurally validates the fixture.

- CSV has 27 rows: 3 repeats x 9 wavelength points.
- `repeat` is a non-physical index coordinate with values 1, 2, and 3.
- Wavelength runs from 1548.0 through 1552.0 nm in 0.5 nm steps.
- Raw variables are input/output optical power in mW; transmission and loss are
  absent and may be explicit derived results only.
- Shared conditions are `24.8 degC`, `80 mA`, and TE polarization; expected
  canonical numeric conditions are `297.95 K` and `0.08 A`.
- One confirmation targets the exact parsed series candidate revision and source
  mapping.
- Import diagnostics plus accepted rows total 27; no row silently disappears.
