"""Config that scaffolds the executable's icon as `rig/resources/icon.png`."""

import shutil
from pathlib import Path
from typing import Any

from pyrig.core.resources import resource_path
from pyrig.rig.configs.base.config_file import DictConfigFile
from pyrig_resources.rig.configs.resources_init import ResourcesInitConfigFile

from pyrig_executables.rig import resources


class IconConfigFile(DictConfigFile):
    """Config file that scaffolds the `icon.png` used as the executable's icon.

    The release workflow bundles this file into the built executable as its
    icon. The scaffolded file is a default -- replace it with your own; it is
    created only when missing, so a project's own icon is preserved.

    Note:
        If the file exists but is not a valid PNG, validation raises
        `RuntimeError` rather than automatically restoring the default icon.
    """

    def _configs(self) -> dict[str, Any]:
        """Return the required configuration structure.

        Returns:
            An empty dict; the icon is a binary file with no structured
            content to enforce.
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
        """Raise `RuntimeError`; the icon is binary and should never be loaded.

        Raises:
            RuntimeError: Always; the icon is never loaded.
        """
        msg = "The icon is a binary PNG and should never be loaded."
        raise RuntimeError(msg)

    def extension(self) -> str:
        """Return `"png"` as the icon's file extension."""
        return "png"

    def is_correct(self) -> bool:
        """Return whether the icon file starts with the PNG signature.

        Only the 8-byte PNG magic number is checked; the rest of the file's
        bytes are not otherwise validated.

        Returns:
            `True` if the icon file starts with the PNG signature; `False`
            otherwise.
        """
        with self.path().open("rb") as f:
            return f.read(8) == b"\x89PNG\r\n\x1a\n"

    def parent_path(self) -> Path:
        """Return the directory the icon lives in.

        Returns:
            The project's `rig/resources` package directory, shared with the
            config file that scaffolds that package's `__init__.py`.
        """
        return ResourcesInitConfigFile.I.parent_path()

    def stem(self) -> str:
        """Return `"icon"` as the icon's filename stem."""
        return "icon"
