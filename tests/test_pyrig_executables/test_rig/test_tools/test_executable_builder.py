"""Test module."""

from pathlib import Path

from pyrig.core.subprocesses import Args

from pyrig_executables import main
from pyrig_executables.rig import tools
from pyrig_executables.rig.tools.executable_builder import ExecutableBuilder


class TestExecutableBuilder:
    """Test class."""

    def test_dev_dependencies(self) -> None:
        """Test method."""
        assert ExecutableBuilder.I.dev_dependencies() == ("pyinstaller", "pillow")

    def test_name(self) -> None:
        """Test method."""
        assert ExecutableBuilder.I.name() == "pyinstaller"

    def test_group(self) -> None:
        """Test method."""
        assert ExecutableBuilder.I.group() == "project-info"

    def test_image_url(self) -> None:
        """Test method."""
        assert (
            ExecutableBuilder.I.image_url()
            == "https://img.shields.io/github/downloads/Winipedia/pyrig-executables/total?logo=github&label=downloads"
        )

    def test_link_url(self) -> None:
        """Test method."""
        assert (
            ExecutableBuilder.I.link_url()
            == "https://github.com/Winipedia/pyrig-executables/releases"
        )

    def test_build_args(self) -> None:
        """Test method."""
        assert ExecutableBuilder.I.build_args(
            "--some-arg",
            "some-val",
            name="exename",
            entry_point=Path("entry/point.py"),
            icon=Path("icon.png"),
            resource_modules=[main],
        ) == Args(
            "pyinstaller",
            "--onefile",
            "--name",
            "exename",
            "--icon",
            "icon.png",
            "--collect-data",
            "pyrig_executables.main",
            "--some-arg",
            "some-val",
            "entry/point.py",
        )
        assert ExecutableBuilder.I.build_args(
            name="exename",
            entry_point=Path("entry/point.py"),
            icon=Path("icon.png"),
            resource_modules=[main, tools],
        ) == Args(
            "pyinstaller",
            "--onefile",
            "--name",
            "exename",
            "--icon",
            "icon.png",
            "--collect-data",
            "pyrig_executables.main",
            "--collect-data",
            "pyrig_executables.rig.tools",
            "entry/point.py",
        )

    def test_version_control_ignore_paths(self) -> None:
        """Test method."""
        assert ExecutableBuilder.I.version_control_ignore_paths() == (
            "dist/",
            "*.spec",
            "build/",
        )

    def test_dist_dir(self) -> None:
        """Test method."""
        assert ExecutableBuilder.I.dist_dir() == Path("dist")
