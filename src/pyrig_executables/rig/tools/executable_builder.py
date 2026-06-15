"""Executable builder tool wrapper.

Wraps commands and information of the executable builder tool, which bundles
the project into standalone binaries that are attached to GitHub releases.
"""

from pathlib import Path

from pyrig.core.subprocesses import Args
from pyrig.rig.tools.base.tool import Group, Tool
from pyrig.rig.tools.package_manager import PackageManager
from pyrig.rig.tools.version_control.remote import RemoteVersionController
from pyrig.rig.tools.version_control.version_controller import VersionController


class ExecutableBuilder(Tool):
    """Executable builder wrapper.

    Builds standalone executables of the project and exposes a project-specific
    badge that advertises the downloadable release binaries. The badge shows the
    cumulative download count of all release assets and links to the GitHub
    releases page, where the executables produced by this plugin are published.
    """

    def name(self) -> str:
        """Get tool name."""
        return "pyinstaller"

    def group(self) -> str:
        """Returns the group the tool belongs to."""
        return Group.PROJECT_INFO

    def image_url(self) -> str:
        """Get the GitHub release downloads badge URL."""
        owner, repo = (
            VersionController.I.repo_owner(check_repo_url=False),
            PackageManager.I.project_name(),
        )
        return f"https://img.shields.io/github/downloads/{owner}/{repo}/total?logo=github&label=downloads"

    def link_url(self) -> str:
        """Get the GitHub releases page URL where the binaries are published."""
        return RemoteVersionController.I.releases_url()

    def build_args(self, name: str, entry_point: Path, *args: str) -> Args:
        """Construct the command that bundles a single-file executable.

        Produces ``pyinstaller --onefile --noconsole --name <name>
        <entry_point>``, which builds one self-contained, windowed binary (no
        console window) from the given entry-point script. The result is written
        to the ``dist/`` directory. Override this method for a console
        application, which keeps a terminal attached on Windows.

        Args:
            name: Output name for the executable (without an OS-specific
                extension; ``pyinstaller`` appends ``.exe`` on Windows).
            entry_point: Path to the entry-point script to bundle.
            *args: Additional arguments forwarded to ``pyinstaller``.

        Returns:
            Args for ``pyinstaller --onefile --noconsole --name <name>
            <entry_point>``.
        """
        return self.args(
            "--onefile", "--noconsole", "--name", name, *args, entry_point.as_posix()
        )

    def version_control_ignore_paths(self) -> tuple[str, ...]:
        """Return the build artifact paths to exclude from version control.

        Returns:
            The ``dist`` directory that ``pyinstaller`` writes the built
            executables to.
        """
        return (self.dist_dir().as_posix(), "*.spec", "build/")

    def dist_dir(self) -> Path:
        """Return the directory ``pyinstaller`` writes built executables to.

        Single source of truth for the output location, reused by the version
        control ignore paths and by the release workflow when uploading,
        downloading, and attaching the binaries.

        Returns:
            The ``dist`` output directory, relative to the project root.
        """
        return Path("dist")
