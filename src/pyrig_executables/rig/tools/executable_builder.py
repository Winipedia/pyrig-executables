"""Tool wrapper for bundling the project into standalone release executables."""

from collections.abc import Iterable
from pathlib import Path
from types import ModuleType

from pyrig.core.subprocesses import Args
from pyrig.rig.tools.base.tool import Group, Tool
from pyrig.rig.tools.package_manager import PackageManager
from pyrig.rig.tools.version_control.controller import VersionController
from pyrig.rig.tools.version_control.remote import RemoteVersionController


class ExecutableBuilder(Tool):
    """Wrapper for `pyinstaller`, the tool that builds standalone executables.

    Exposes a project-info badge showing the cumulative download count across
    all GitHub release assets, linking to the releases page where the built
    executables are published.
    """

    def dev_dependencies(self) -> tuple[str, ...]:
        """Return the dev dependencies required to build executables.

        Extends the default with `pillow` so `pyinstaller` can convert a
        non-native icon image (e.g. PNG) into the per-OS icon format (`.ico`
        / `.icns`) at build time.

        Returns:
            `pyinstaller` and `pillow`.
        """
        return (*super().dev_dependencies(), "pillow")

    def group(self) -> str:
        """Return `Group.PROJECT_INFO`."""
        return Group.PROJECT_INFO

    def image_url(self) -> str:
        """Return the shields.io URL for the GitHub release downloads badge."""
        owner, repo = (
            VersionController.I.repo_owner(),
            PackageManager.I.project_name(),
        )
        return f"https://img.shields.io/github/downloads/{owner}/{repo}/total?logo=github&label=downloads"

    def link_url(self) -> str:
        """Return the GitHub releases page URL where the binaries are published."""
        return RemoteVersionController.I.releases_url()

    def name(self) -> str:
        """Return `'pyinstaller'`."""
        return "pyinstaller"

    def version_control_ignore_paths(self) -> tuple[str, ...]:
        """Return the build artifact paths to exclude from version control.

        Returns:
            The `pyinstaller` build artifacts: the `dist/` output directory
            (where the executables are written), the generated `*.spec` files,
            and the `build/` working directory.
        """
        return (f"{self.dist_dir().as_posix()}/", "*.spec", "build/")

    def build_args(
        self,
        *args: str,
        name: str,
        entry_point: Path,
        icon: Path,
        resource_modules: Iterable[ModuleType],
    ) -> Args:
        """Build the `pyinstaller` command that bundles a single-file executable.

        Bundles each module in `resource_modules` with its own
        `--collect-data` flag rather than pointing `--add-data` at a path.
        This preserves the package layout so resources stay locatable at
        runtime through `importlib.resources` in both development and the
        frozen executable, and sidesteps the platform-specific separator
        `--add-data` requires. The build runs in console mode by default;
        pass `--windowed` through `*args` for a GUI application that should
        run without a console window (this instead produces a `.app` bundle
        directory on macOS).

        Args:
            *args: Additional arguments forwarded to `pyinstaller`, inserted
                after the resource flags and before `entry_point`.
            name: Output name for the executable (without an OS-specific
                extension; `pyinstaller` appends `.exe` on Windows).
            entry_point: Path to the entry-point script to bundle.
            icon: Path to the icon image. A non-native format (e.g. PNG) is
                converted to the per-OS format (`.ico` / `.icns`) at build
                time via Pillow; ignored on Linux.
            resource_modules: Modules whose data files are bundled, one
                `--collect-data` flag per module. Where the project keeps its
                resources is the caller's concern, so this is required.

        Returns:
            Args for the `pyinstaller` command.
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

    def dist_dir(self) -> Path:
        """Return the directory `pyinstaller` writes built executables to.

        Single source of truth for the output location, so it never drifts
        out of sync with other places that need it.

        Returns:
            The `dist` output directory, relative to the project root.
        """
        return Path("dist")
