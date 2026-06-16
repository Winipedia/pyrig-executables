"""Test module."""

from contextlib import chdir
from pathlib import Path

from pyrig_resources.rig.configs.resources_init import ResourcesInitConfigFile
from pytest_mock import MockerFixture

from pyrig_executables.rig.configs.icon import IconConfigFile


class TestIconConfigFile:
    """Test class."""

    def test_parent_path(self) -> None:
        """Test method."""
        assert IconConfigFile.I.parent_path() == ResourcesInitConfigFile.I.parent_path()

    def test_stem(self) -> None:
        """Test method."""
        assert IconConfigFile.I.stem() == "icon"

    def test_extension(self) -> None:
        """Test method."""
        assert IconConfigFile.I.extension() == "png"

    def test__configs(self) -> None:
        """Test method."""
        assert IconConfigFile.I._configs() == {  # noqa: SLF001
            "text": "pyrig-executables",
        }

    def test__load(self) -> None:
        """Test method."""
        assert IconConfigFile.I._load() == {}  # noqa: SLF001

    def test__dump(self, mocker: MockerFixture, tmp_path: Path) -> None:
        """Test method."""
        with chdir(tmp_path):
            icon = Path("icon.png")
            mocker.patch.object(IconConfigFile, "path", return_value=icon)
            IconConfigFile.I._dump({"text": "icon"})  # noqa: SLF001
            assert icon.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")

    def test_is_correct(self, mocker: MockerFixture) -> None:
        """Test method."""
        assert IconConfigFile.I.is_correct() is True
        path = mocker.patch.object(IconConfigFile, "path")
        path.return_value.read_bytes.return_value = b"not a png"
        assert IconConfigFile.I.is_correct() is False

    def test_png_signature(self) -> None:
        """Test method."""
        assert IconConfigFile.I.png_signature() == b"\x89PNG\r\n\x1a\n"
