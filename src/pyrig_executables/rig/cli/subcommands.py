"""Project-specific CLI commands.

All functions in this module are automatically discovered and registered
as CLI commands for this project.
"""


def run() -> None:
    """Run the project by executing its ``main.py`` as the entry module.

    Runs the project's ``main.py`` under the ``__main__`` name so its
    ``if __name__ == "__main__"`` guard fires and calls ``main``, mirroring how
    the built executable runs.
    """
    from pyrig_executables.rig.cli.commands.run import run_main  # noqa: PLC0415

    run_main()
