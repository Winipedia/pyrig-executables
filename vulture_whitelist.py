"""Explicit references for reviewed dead code false positives."""

from pyrig.rig.configs.base.config_file import ConfigFile
from pyrig.rig.configs.base.copy_module import CopyModuleConfigFile
from pyrig.rig.tools.base.tool import Tool

from pyrig_executables.rig.cli.subcommands import run
from pyrig_executables.rig.configs.icon import IconConfigFile
from pyrig_executables.rig.configs.main import MainConfigFile
from pyrig_executables.rig.tools.executables.builder import ExecutableBuilder

_COMMANDS = (run,)
_CONFIG_FILE_OVERRIDES = (
    ConfigFile._configs,
    ConfigFile._dump,
    ConfigFile._load,
    ConfigFile.extension,
    ConfigFile.is_correct,
    ConfigFile.stem,
    CopyModuleConfigFile.copy_module,
)
_CONFIG_FILES = (
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
