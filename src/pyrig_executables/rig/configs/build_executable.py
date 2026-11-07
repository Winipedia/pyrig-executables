"""Shell script that builds the project's standalone executable."""

from collections.abc import Iterable
from pathlib import Path
from types import ModuleType
from typing import Any, override

from pyrig.rig.configs.base.config_file import ConfigFile
from pyrig.rig.configs.base.shell import ShellConfigFile
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig_resources.rig.configs.resources_init import ResourcesInitConfigFile
from pyrig_runtime.core.introspection.modules import replace_root_module

from pyrig_executables.rig import resources
from pyrig_executables.rig.configs.icon import IconConfigFile
from pyrig_executables.rig.configs.main import MainConfigFile
from pyrig_executables.rig.tools.executables.builder import ExecutableBuilder


class BuildExecutableConfigFile(ShellConfigFile):
    """Generate the project-root script used to build the executable."""

    @override
    def dependencies(self) -> Iterable[type[ConfigFile[Any]]]:
        """Return the config files required before generating the script."""
        return (*super().dependencies(), ResourcesInitConfigFile)

    @override
    def parent_path(self) -> Path:
        """Return the project root."""
        return Path()

    @override
    def script(self) -> str:
        """Return the command that builds the executable."""
        command = PackageManager.I.run_args(
            *ExecutableBuilder.I.build_args(
                name=f'{PackageManager.I.project_name()}-"${{OSTYPE}}"',
                entry_point=MainConfigFile.I.path(),
                icon=IconConfigFile.I.path(),
                collect_all_modules=self.collect_all_modules(),
                collect_data_modules=self.collect_data_modules(),
            ),
        )
        return command.multiline() + "\n"

    @override
    def stem(self) -> str:
        """Return the script filename without its extension."""
        return "build-executable"

    def collect_all_modules(self) -> Iterable[ModuleType]:
        """Return modules to bundle with their data, submodules, and binaries."""
        return ()

    def collect_data_modules(self) -> Iterable[ModuleType]:
        """Return the project's resource package for data collection."""
        return (replace_root_module(resources, PackageManager.I.package_name()),)
