"""Test module."""

import sys
from runpy import run_module

from pyrig_executables import main as main_module
from pyrig_executables.rig.cli.commands.run import run_main


def test_run_main() -> None:
    """Test function."""
    module_name = main_module.__name__
    del sys.modules[module_name]
    assert run_main() is None
    run_module(module_name, run_name="__main__")
