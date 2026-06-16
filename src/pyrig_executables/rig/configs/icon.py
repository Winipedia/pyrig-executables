"""Config that scaffolds the executable's icon as ``resources/icon.png``."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pyrig.rig.configs.base.config_file import ConfigDict, DictConfigFile
from pyrig.rig.tools.package_manager import PackageManager
from pyrig_resources.rig.configs.resources_init import ResourcesInitConfigFile


class IconConfigFile(DictConfigFile):
    """Scaffold the ``icon.png`` used as the executable's icon.

    Creates a placeholder ``icon.png`` inside the project's ``rig/resources``
    package, which the release workflow passes to ``pyinstaller --icon``.
    ``pyinstaller`` converts the PNG to the per-OS icon format (``.ico`` on
    Windows, ``.icns`` on macOS; ignored on Linux) at build time. The generated
    file is a simple default icon rendering the project name -- replace it with
    your own. Only the PNG signature is validated, so any valid PNG is
    preserved while a missing or non-PNG file is regenerated.
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

    def _configs(self) -> ConfigDict:
        """Return the spec that defines the generated icon.

        Returns:
            The icon spec consumed by :meth:`_dump`: the ``text`` to render
            (the project name).
        """
        return {"text": PackageManager.I.project_name()}

    def _load(self) -> ConfigDict:
        """Load the file's structured content.

        Returns:
            An empty dict; a binary icon has no structured content to parse.
        """
        return {}

    def _dump(self, configs: ConfigDict) -> None:
        """Render the icon text to a PNG.

        Draws ``configs["text"]`` with Pillow's bundled default font on a canvas
        sized from the text's glyph mask, using default colors (no external
        assets, no color settings). ``pyinstaller`` converts the PNG to the
        per-OS icon format at build time. Only runs when the icon is missing or
        invalid, so a user-provided icon is never overwritten.

        Args:
            configs: The icon spec from :meth:`_configs` (just ``text``).
        """
        text = configs["text"]
        image = Image.new("RGB", ImageFont.load_default().getmask(text).size)
        ImageDraw.Draw(image).text((0, 0), text)
        image.save(self.path())

    def is_correct(self) -> bool:
        """Return whether the icon file is a valid PNG.

        Validates only the PNG signature (the file's leading magic bytes), not
        the image contents, so any valid PNG is accepted and a user-provided
        icon is preserved. A non-PNG file is regenerated. Existence is assumed:
        ``is_correct`` is only ever called once the file is present (``validate``
        creates it first; the drift check runs over committed files).

        Returns:
            ``True`` if the icon file begins with the PNG signature.
        """
        return self.path().read_bytes().startswith(self.png_signature())

    def png_signature(self) -> bytes:
        """Return the PNG file signature.

        Returns:
            The 8-byte magic header that every PNG file starts with, used by
            :meth:`is_correct` to verify the icon is a PNG.
        """
        return b"\x89PNG\r\n\x1a\n"
