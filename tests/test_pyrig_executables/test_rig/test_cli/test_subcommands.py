"""Test module."""

from collections.abc import Callable, Iterable
from types import FunctionType

from pyrig_executables.rig.cli.commands.run import run_main
from pyrig_executables.rig.cli.subcommands import run


def test_run(
    command_works: Callable[[FunctionType], bool],
    command_calls_function: Callable[[FunctionType, FunctionType, Iterable[str]], bool],
) -> None:
    """Test function."""
    assert command_works(run)
    assert command_calls_function(run, run_main, [])
