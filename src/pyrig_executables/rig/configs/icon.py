"""Config that scaffolds the executable's icon as ``resources/icon.png``."""

import shutil
from pathlib import Path
from typing import Any

from pyrig.core.resources import resource_path
from pyrig.rig.configs.base.config_file import DictConfigFile
from pyrig_resources.rig.configs.resources_init import ResourcesInitConfigFile

from pyrig_executables.rig import resources


class IconConfigFile(DictConfigFile):
    """Scaffold the ``icon.png`` used as the executable's icon.

    Copies the plugin's bundled default ``icon.png`` into the project's
    ``rig/resources`` package, where the release workflow passes it to
    ``pyinstaller --icon``. ``pyinstaller`` converts the PNG to the per-OS icon
    format (``.ico`` on Windows, ``.icns`` on macOS; ignored on Linux) at build
    time. The copied file is a default -- replace it with your own; it is only
    created when missing, so a project's own icon is preserved.
    """

    def parent_path(self) -> Path:
        """Return the directory the icon lives in.

        Returns:
            The project's ``rig/resources`` package directory, shared with
            :class:`~pyrig_resources.rig.configs.resources_init.ResourcesInitConfigFile`.
        """
        return ResourcesInitConfigFile.I.parent_path()

    def stem(self) -> str:
        """Return the icon filename stem.

        Returns:
            ``"icon"``, producing ``icon.png``.
        """
        return "icon"

    def extension(self) -> str:
        """Return the icon file extension.

        Returns:
            ``"png"``.
        """
        return "png"

    def _configs(self) -> dict[str, Any]:
        """Return the required structured content.

        Returns:
            An empty dict; the icon is a binary file copied verbatim, with no
            structured content to enforce.
        """
        return {}

    def _load(self) -> dict[str, Any]:
        """Raise -- the icon is binary and is never loaded as a dict.

        :meth:`is_correct` only checks for the file's existence, so an existing
        icon is always correct and ``validate`` never reaches the merge step
        that would read the file. This guard surfaces a bug if the dict-loading
        machinery is ever invoked on the icon.

        Raises:
            RuntimeError: Always; the icon is never loaded as a dict.
        """
        msg = "The icon is a binary PNG and is never loaded as a dict."
        raise RuntimeError(msg)

    def _dump(self, configs: dict[str, Any]) -> None:
        """Copy the plugin's bundled default icon into the project.

        Copies the ``icon.png`` shipped in this plugin's resources package to
        the project's resources directory. ``pyinstaller`` converts it to the
        per-OS icon format at build time. Only runs when the icon is missing, so
        a user-provided icon is never overwritten.

        Args:
            configs: Ignored; the icon is a binary file copied verbatim.
        """
        del configs
        shutil.copy(
            resource_path(name=self.filename(), package=resources),
            self.path(),
        )

    def is_correct(self) -> bool:
        """Return whether the icon file exists.

        Existence is the only requirement: the bundled default is a valid PNG
        and any user-provided icon is preserved, so the file's contents are not
        validated.

        Returns:
            ``True`` if the icon file exists.
        """
        return self.path().exists()
