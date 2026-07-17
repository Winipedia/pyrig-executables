"""Config that scaffolds the executable's icon as `rig/resources/icon.png`."""

import shutil
from pathlib import Path
from typing import Any

from pyrig.core.resources import resource_path
from pyrig.core.strings import file_has_content
from pyrig.rig.configs.base.config_file import DictConfigFile
from pyrig_resources.rig.configs.resources_init import ResourcesInitConfigFile

from pyrig_executables.rig import resources


class IconConfigFile(DictConfigFile):
    """Config file that scaffolds the `icon.png` used as the executable's icon.

    The release workflow passes the resulting file's path to
    `pyinstaller --icon`, which converts the PNG to the per-OS icon format
    (`.ico` on Windows, `.icns` on macOS; ignored on Linux) at build time. The
    scaffolded file is a default -- replace it with your own; it is only
    created when missing, so a project's own icon is preserved.
    """

    def _configs(self) -> dict[str, Any]:
        """Return the required structured content.

        Returns:
            An empty dict; the icon is a binary file copied verbatim, with no
            structured content to enforce.
        """
        return {}

    def _dump(self, configs: dict[str, Any]) -> None:
        """Copy this plugin's bundled default icon to the project's icon path.

        Overwrites whatever file is already at the destination.

        Args:
            configs: Ignored; the icon is a binary file copied verbatim.
        """
        del configs
        shutil.copy(
            resource_path(name=self.filename(), package=resources),
            self.path(),
        )

    def _load(self) -> dict[str, Any]:
        """Raise -- the icon is binary and should never be loaded.

        Raises:
            RuntimeError: Always; the icon is never loaded.
        """
        msg = "The icon is a binary PNG and should never be loaded."
        raise RuntimeError(msg)

    def extension(self) -> str:
        """Return the icon file extension.

        Returns:
            `"png"`.
        """
        return "png"

    def is_correct(self) -> bool:
        """Return whether the icon file is non-empty.

        Non-emptiness is the only requirement: the bundled default is a valid
        PNG and any user-provided icon is preserved, so the file's bytes are
        not otherwise validated.

        Returns:
            `True` if the icon file has content; `False` if it is empty.
        """
        return file_has_content(self.path())

    def parent_path(self) -> Path:
        """Return the directory the icon lives in.

        Returns:
            The project's `rig/resources` package directory, shared with the
            config file that scaffolds that package's `__init__.py`.
        """
        return ResourcesInitConfigFile.I.parent_path()

    def stem(self) -> str:
        """Return the icon filename stem.

        Returns:
            `"icon"`, producing `icon.png`.
        """
        return "icon"
