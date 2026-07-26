"""Customization of the pyrig CLI tool for projects that build executables."""

from typing import Any

from pyrig.core.subprocesses import Args
from pyrig.rig.cli.subcommands import sync
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig.rig.tools.pyrigger import Pyrigger as BasePyrigger


class Pyrigger(BasePyrigger):
    """Pyrig CLI tool wrapper that extends project initialization for this plugin."""

    def setup_steps(self) -> tuple[tuple[Args, dict[str, Any]], ...]:
        """Insert an extra `pyrig sync` step into the base initialization sequence.

        A duplicate of the base `pyrig sync` step is inserted right after the
        *second* occurrence of the dependency-install step, not the first. Without
        this later pass, the mirrored test stub for the plugin-scaffolded `main.py`
        is not generated during initialization.
        """
        steps = list(super().setup_steps())
        sync_args = self.cmd_args(cmd=sync)
        sync_step = next((args, kwargs) for args, kwargs in steps if args == sync_args)
        install_args = PackageManager.I.install_dependencies_args()
        install_step_indexes = (
            i for i, (args, _) in enumerate(steps) if args == install_args
        )
        _ = next(install_step_indexes)
        second_install_step_index = next(install_step_indexes)
        steps.insert(second_install_step_index + 1, sync_step)
        return tuple(steps)
