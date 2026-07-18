"""Test module."""

from pyrig.rig.cli.subcommands import sync
from pyrig.rig.tools.pyrigger import Pyrigger


class TestPyrigger:
    """Test class."""

    def test_setup_steps(self) -> None:
        """Test method."""
        steps = Pyrigger.I.setup_steps()
        sync_args = Pyrigger.I.cmd_args(cmd=sync)
        count = sum(1 for args, _ in steps if args == sync_args)
        expected_count = 2
        assert count == expected_count
