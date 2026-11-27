"""Explicit references for reviewed dead code false positives."""

from pyrig.rig.configs.base.config_file import ConfigFile
from pyrig.rig.configs.base.copy_module import CopyModuleConfigFile
from pyrig.rig.configs.base.shell import ShellConfigFile
from pyrig.rig.configs.base.workflow import WorkflowConfigFile
from pyrig.rig.tools.base.tool import Tool

from pyrig_executables.rig.cli.subcommands import run
from pyrig_executables.rig.configs.executables.build import BuildExecutableConfigFile
from pyrig_executables.rig.configs.executables.icon import IconConfigFile
from pyrig_executables.rig.configs.executables.main import MainConfigFile
from pyrig_executables.rig.tools.executables.builder import ExecutableBuilder

_COMMANDS = (run,)
_CONFIG_FILE_OVERRIDES = (
    ConfigFile._configs,  # noqa: SLF001
    ConfigFile._dump,  # noqa: SLF001
    ConfigFile._load,  # noqa: SLF001
    ConfigFile.extension,
    ConfigFile.is_correct,
    ConfigFile.stem,
    CopyModuleConfigFile.copy_module,
    ShellConfigFile.script,
    WorkflowConfigFile.workflow_triggers,
)
_CONFIG_FILES = (
    BuildExecutableConfigFile,
    IconConfigFile,
    MainConfigFile,
)
_TOOLS = (ExecutableBuilder,)
_TOOLS_OVERRIDES = (
    Tool.group,
    Tool.image_url,
    Tool.link_url,
    Tool.version_control_ignore_patterns,
)
