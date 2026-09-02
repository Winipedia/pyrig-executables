"""Customization of the remote version controller."""

from collections.abc import Iterable

from pyrig.core.subprocesses import Args
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig.rig.tools.version_control.remote.controller import (
    RemoteVersionController as BaseRemoteVersionController,
)


class RemoteVersionController(BaseRemoteVersionController):
    """Overrides the base class to include executable artifacts in releases."""

    def create_release_args(
        self,
        *args: str,
        tag: str,
        files: Iterable[str] = (),
    ) -> Args:
        """Build release arguments with the executable artifacts included.

        Args:
            *args: Additional arguments forwarded to `gh release create`.
            tag: The tag to release, also used as the release title.
            files: Release asset paths to upload alongside the executable
                artifacts.

        Returns:
            Args for `gh release create` with every file in `dist/` attached.
        """
        return super().create_release_args(
            *args,
            tag=tag,
            files=(
                f"{PackageManager.I.dist_dir().as_posix()}/*",
                *files,
            ),
        )
