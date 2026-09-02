"""Test module."""

from pyrig_executables.rig.tools.version_control.remote.controller import (
    RemoteVersionController,
)


class TestRemoteVersionController:
    """Test class."""

    def test_create_release_args(self) -> None:
        """Test that executable artifacts are included in release arguments."""
        assert tuple(RemoteVersionController.I.create_release_args(tag="v1.2.3")) == (
            "gh",
            "release",
            "create",
            "v1.2.3",
            "dist/*",
            "--title=v1.2.3",
            "--generate-notes",
        )

    def test_create_release_args_preserves_additional_args(self) -> None:
        """Test that caller arguments and files are preserved."""
        assert tuple(
            RemoteVersionController.I.create_release_args(
                "--draft",
                tag="v1.2.3",
                files=("package.zip",),
            ),
        ) == (
            "gh",
            "release",
            "create",
            "v1.2.3",
            "dist/*",
            "package.zip",
            "--title=v1.2.3",
            "--generate-notes",
            "--draft",
        )
