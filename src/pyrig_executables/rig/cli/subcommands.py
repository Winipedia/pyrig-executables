"""Project-specific CLI commands.

Functions defined directly in this module are discovered and registered as
top-level CLI commands. Module-level `typer.Typer` instances are registered
as command groups, with each group named after the kebab-case form of its
variable name.
"""


def run() -> None:
    """Run the project's entry point locally, as the built executable does."""
    from pyrig_executables.rig.cli.commands.run import run_main  # noqa: PLC0415

    run_main()
