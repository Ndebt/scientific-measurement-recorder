"""Foundation command-line entry point."""

from typing import Annotated

import typer

from smr import __version__

app = typer.Typer(
    name="smr",
    help="Capture and validate scientific measurements locally.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """Run the Scientific Measurement Recorder command group."""


@app.command()
def version(
    short: Annotated[
        bool,
        typer.Option("--short", help="Print only the semantic version."),
    ] = False,
) -> None:
    """Show the installed SMR version."""
    typer.echo(
        __version__ if short else f"Scientific Measurement Recorder {__version__}"
    )
