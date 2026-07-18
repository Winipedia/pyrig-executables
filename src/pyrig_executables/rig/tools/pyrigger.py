"""Tool wrapper for the pyrig CLI itself, used for self-referential commands."""

from typing import Any

from pyrig.core.subprocesses import Args
from pyrig.rig.cli.subcommands import sync
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig.rig.tools.pyrigger import Pyrigger as BasePyrigger


class Pyrigger(BasePyrigger):
    """You can override methods from the base class to customize behavior."""

    def setup_steps(self) -> tuple[tuple[Args, dict[str, Any]], ...]:
        """Override this method to customize the setup steps for the Pyrigger tool."""
        steps = list(super().setup_steps())
        sync_args = self.cmd_args(cmd=sync)
        sync_step = next((args, kwargs) for args, kwargs in steps if args == sync_args)
        second_install_args = PackageManager.I.install_dependencies_args()
        index = next(
            (i for i, (args, _) in enumerate(steps) if args == second_install_args),
        )
        steps.insert(index + 1, sync_step)
        return tuple(steps)
