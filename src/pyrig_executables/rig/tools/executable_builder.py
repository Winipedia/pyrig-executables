"""Executable builder tool wrapper.

Wraps commands and information of the executable builder tool, which bundles
the project into standalone binaries that are attached to GitHub releases.
"""

from collections.abc import Iterable
from pathlib import Path
from types import ModuleType

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

    def build_args(
        self,
        *args: str,
        name: str,
        entry_point: Path,
        icon: Path,
        resource_modules: Iterable[ModuleType],
    ) -> Args:
        """Construct the command that bundles a single-file executable.

        Produces ``pyinstaller --onefile --name <name> --icon <icon>
        <--collect-data ...> <entry_point>``, building one self-contained binary
        from the entry-point script, applying the icon, and bundling each
        resource module via its own ``--collect-data`` flag. Collecting by
        package (rather than ``--add-data`` by path) preserves the package
        layout so resources stay locatable at runtime through
        ``importlib.resources`` -- which
        :func:`pyrig.core.resources.resource_path` uses -- in both development
        and the frozen executable, and avoids the platform-specific
        ``--add-data`` path separator. The result is written to the ``dist/``
        directory. The build runs in console mode so the binary is a single file
        on every OS (on macOS ``--windowed`` would instead emit a ``.app``
        bundle directory). Override this method to add ``--windowed`` for a GUI
        application that should run without a console window.

        Args:
            name: Output name for the executable (without an OS-specific
                extension; ``pyinstaller`` appends ``.exe`` on Windows).
            entry_point: Path to the entry-point script to bundle.
            icon: Path to the icon image. A non-native format (e.g. PNG) is
                converted to the per-OS format (``.ico`` / ``.icns``) at build
                time via Pillow (see :meth:`dev_dependencies`); ignored on Linux.
            *args: Additional arguments forwarded to ``pyinstaller``.
            resource_modules: Modules whose data files are bundled, one
                ``--collect-data`` flag per module. Where the project keeps its
                resources is the caller's concern, so this is required.

        Returns:
            Args for the ``pyinstaller`` command.
        """
        collect_data = (
            arg
            for module in resource_modules
            for arg in ("--collect-data", module.__name__)
        )
        return self.args(
            "--onefile",
            "--name",
            name,
            "--icon",
            icon.as_posix(),
            *collect_data,
            *args,
            entry_point.as_posix(),
        )

    def dev_dependencies(self) -> tuple[str, ...]:
        """Return the dev dependencies required to build executables.

        Extends the default (the tool's own name) with ``pillow`` so
        ``pyinstaller`` can convert a non-native icon image (e.g. PNG) into the
        per-OS icon format (``.ico`` / ``.icns``) at build time.

        Returns:
            ``pyinstaller`` and ``pillow``.
        """
        return (*super().dev_dependencies(), "pillow")

    def version_control_ignore_paths(self) -> tuple[str, ...]:
        """Return the build artifact paths to exclude from version control.

        Returns:
            The ``pyinstaller`` build artifacts: the ``dist/`` output directory
            (where the executables are written), the generated ``*.spec`` files,
            and the ``build/`` working directory.
        """
        return (f"{self.dist_dir().as_posix()}/", "*.spec", "build/")

    def dist_dir(self) -> Path:
        """Return the directory ``pyinstaller`` writes built executables to.

        Single source of truth for the output location, reused by the version
        control ignore paths and by the release workflow when uploading,
        downloading, and attaching the binaries.

        Returns:
            The ``dist`` output directory, relative to the project root.
        """
        return Path("dist")
