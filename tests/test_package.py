"""M0 smoke tests for the installable package shell."""

from importlib.metadata import version as distribution_version

import pytest
from typer.testing import CliRunner

import smr
from smr.cli import app

DISTRIBUTION_NAME = "scientific-measurement-recorder"


def test_package_and_distribution_versions_agree() -> None:
    assert smr.__version__ == distribution_version(DISTRIBUTION_NAME)


@pytest.mark.parametrize(
    ("arguments", "expected"),
    [
        (["version", "--short"], smr.__version__),
        (["version"], f"Scientific Measurement Recorder {smr.__version__}"),
    ],
)
def test_cli_version(arguments: list[str], expected: str) -> None:
    result = CliRunner().invoke(app, arguments)

    assert result.exit_code == 0
    assert result.stdout.strip() == expected


def test_cli_help_and_no_args_behavior() -> None:
    runner = CliRunner()

    help_result = runner.invoke(app, ["--help"])
    no_args_result = runner.invoke(app, [])

    assert help_result.exit_code == 0
    assert "Usage:" in help_result.stdout
    assert "version" in help_result.stdout
    assert no_args_result.exit_code == 2
    assert "Usage:" in no_args_result.stdout
