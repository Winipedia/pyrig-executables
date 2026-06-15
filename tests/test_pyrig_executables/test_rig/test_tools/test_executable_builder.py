"""Test module."""

from pathlib import Path

from pyrig.core.subprocesses import Args

from pyrig_executables.rig.tools.executable_builder import ExecutableBuilder


class TestExecutableBuilder:
    """Test class."""

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
        ) == Args(
            (
                "pyinstaller",
                "--onefile",
                "--name",
                "exename",
                "--some-arg",
                "some-val",
                "entry/point.py",
            )
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
