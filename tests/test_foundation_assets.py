"""M0 structural tests for schemas and the synthetic photonics fixture."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime
from importlib.metadata import version as distribution_version
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

import smr

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "quantity-definition.schema.json"
SEED_PATH = ROOT / "schemas" / "quantity-definitions.v0.1.json"
CSV_PATH = ROOT / "examples" / "data" / "photonics_wg17_spectral_sweep.csv"
METADATA_PATH = CSV_PATH.with_suffix(".metadata.json")
EXPECTED_COLUMNS = {
    "repeat_index",
    "wavelength_nm",
    "input_power_mW",
    "output_power_mW",
}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_digest(value: object) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def test_quantity_seed_validates_and_ids_are_unique() -> None:
    schema = _read_json(SCHEMA_PATH)
    seed = _read_json(SEED_PATH)

    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(seed),
        key=lambda error: tuple(str(part) for part in error.path),
    )

    assert errors == []
    quantity_ids = [
        definition["quantity_id"] for definition in seed["quantity_definitions"]
    ]
    assert len(quantity_ids) == len(set(quantity_ids))
    assert "environment.temperature_interval" in quantity_ids
    assert "core.repeat_index" not in quantity_ids


def test_fixture_structure_references_and_digests() -> None:
    seed = _read_json(SEED_PATH)
    metadata = _read_json(METADATA_PATH)
    quantity_ids = {
        definition["quantity_id"] for definition in seed["quantity_definitions"]
    }

    with CSV_PATH.open(encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    assert set(reader.fieldnames or []) == EXPECTED_COLUMNS
    assert len(rows) == 27
    assert len({row["repeat_index"] for row in rows}) == 3
    assert len({row["wavelength_nm"] for row in rows}) == 9
    assert metadata["series"]["dimensions"] == {"repeat": 3, "wavelength": 9}

    repeat = metadata["series"]["coordinates"]["repeat"]
    assert repeat == {
        "column": "repeat_index",
        "coordinate_kind": "index",
        "values": [1, 2, 3],
    }

    referenced_ids = {
        mapping["quantity_id"]
        for mapping in metadata["series_candidate"]["source_mapping"].values()
        if "quantity_id" in mapping
    }
    referenced_ids.update(
        coordinate["quantity_id"]
        for coordinate in metadata["series"]["coordinates"].values()
        if "quantity_id" in coordinate
    )
    referenced_ids.update(
        variable["quantity_id"]
        for variable in metadata["series"]["data_variables"].values()
    )
    referenced_ids.update(
        condition["quantity_id"] for condition in metadata["conditions"].values()
    )
    assert referenced_ids <= quantity_ids

    assert (
        hashlib.sha256(CSV_PATH.read_bytes()).hexdigest()
        == metadata["source"]["sha256"]
    )
    assert (
        _canonical_digest(metadata["series_candidate"])
        == metadata["confirmation"]["accepted_fields_digest"]
    )


def test_fixture_is_synthetic_and_timestamps_are_coherent() -> None:
    metadata = _read_json(METADATA_PATH)

    assert metadata["data_classification"] == "synthetic_validation_fixture"
    assert metadata["is_empirical_evidence"] is False
    assert metadata["confirmation"]["target_type"] == "series_candidate"
    assert (
        metadata["confirmation"]["target_id"]
        == metadata["series_candidate"]["candidate_id"]
    )
    assert (
        metadata["confirmation"]["target_revision"]
        == metadata["series_candidate"]["candidate_revision"]
    )
    assert metadata["derived_variables"]["present_in_raw_csv"] is False

    ordered_timestamps = [
        metadata["timestamps"]["observed_at"],
        metadata["source"]["captured_at"],
        metadata["series_candidate"]["parsed_at"],
        metadata["confirmation"]["confirmed_at"],
        metadata["series"]["created_at"],
    ]
    parsed_timestamps = [datetime.fromisoformat(value) for value in ordered_timestamps]
    assert parsed_timestamps == sorted(parsed_timestamps)


def test_fixture_producer_matches_installed_package() -> None:
    metadata = _read_json(METADATA_PATH)
    installed_version = distribution_version("scientific-measurement-recorder")

    assert smr.__version__ == installed_version
    assert metadata["producer"] == {
        "distribution": "scientific-measurement-recorder",
        "package_version": installed_version,
    }
