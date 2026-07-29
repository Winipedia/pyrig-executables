"""Customization of the pyrig CLI tool for projects that build executables."""

from typing import Any

from pyrig.core.subprocesses import Args
from pyrig.rig.cli.subcommands import sync
from pyrig.rig.tools.pyrigger import Pyrigger as BasePyrigger


class Pyrigger(BasePyrigger):
    """Pyrig CLI tool wrapper that extends project initialization for this plugin."""

    def setup_steps(self) -> tuple[tuple[Args, dict[str, Any]], ...]:
        """Insert an extra `pyrig sync` step into the base initialization sequence.

        A duplicate of the base `pyrig sync` step is inserted before the original one.
        We need them to run twice so that the test stubs for the generated main.py file.
        """
        steps = list(super().setup_steps())
        sync_args = self.cmd_args(cmd=sync)
        index, sync_step = next(
            (i, (args, kwargs))
            for i, (args, kwargs) in enumerate(steps)
            if args == sync_args
        )
        steps.insert(index, sync_step)
        return tuple(steps)
