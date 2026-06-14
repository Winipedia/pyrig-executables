"""CLI command implementation for running the project's entry-point module."""

from runpy import run_path

from pyrig_executables.rig.configs.main import MainConfigFile


def run_main() -> None:
    """Execute the project's ``main.py`` as the ``__main__`` module.

    Resolves the path to the project's entry-point file via
    :class:`~pyrig_executables.rig.configs.main.MainConfigFile` and runs it with
    ``runpy`` under the ``__main__`` name. Running by path avoids importing the
    module first, so its ``if __name__ == "__main__"`` guard fires and calls
    ``main``, mirroring how the built executable runs the same file.
    """
    run_path(MainConfigFile.I.path().as_posix(), run_name="__main__")
