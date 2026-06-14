"""Executable builder tool wrapper.

Wraps commands and information of the executable builder tool, which bundles
the project into standalone binaries that are attached to GitHub releases.
"""

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
