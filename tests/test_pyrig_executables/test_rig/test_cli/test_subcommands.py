"""Test module."""

from collections.abc import Callable
from typing import Any

from pyrig_executables.rig.cli.commands.run import run_main
from pyrig_executables.rig.cli.subcommands import run


def test_run(
    command_works: Callable[[Callable[..., Any]], None],
    command_calls_function: Callable[[Callable[..., Any], Callable[..., Any]], None],
) -> None:
    """Test function."""
    command_works(run)
    command_calls_function(run, run_main)
