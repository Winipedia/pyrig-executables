"""Release integration for the reusable executable workflow."""

from collections.abc import Callable
from typing import Any, override

from pyrig.rig.configs.version_control.remote.workflows.release import (
    ReleaseWorkflowConfigFile as BaseReleaseWorkflowConfigFile,
)
from pyrig.rig.tools.packages.manager import PackageManager

from pyrig_executables.rig.configs.version_control.remote.workflows.executable import (
    ExecutableWorkflowConfigFile,
)


class ReleaseWorkflowConfigFile(BaseReleaseWorkflowConfigFile):
    """Call the executable workflow and attach its artifacts to the release."""

    @override
    def job_publish_needs(self) -> tuple[Callable[[], dict[str, Any]], ...]:
        """Return the jobs required before publishing."""
        return (*super().job_publish_needs(), self.job_executable)

    @override
    def jobs(self) -> tuple[Callable[[], dict[str, Any]], ...]:
        """Return builders for the executable and base release jobs."""
        return (
            self.job_executable,
            *super().jobs(),
        )

    @override
    def steps_publish(self) -> tuple[Callable[[], dict[str, Any]], ...]:
        """Insert executable downloads immediately before release creation."""
        steps = list(super().steps_publish())
        index = steps.index(self.step_create_release)
        steps.insert(index, self.step_download_executables)
        return tuple(steps)

    def job_executable(self) -> dict[str, Any]:
        """Call the reusable executable build workflow."""
        return self.job_workflow_call(
            workflow=ExecutableWorkflowConfigFile,
        )

    def step_download_executables(self) -> dict[str, Any]:
        """Build a step that merges executable artifacts into `dist/`."""
        return self.step_download_artifact(
            pattern=ExecutableWorkflowConfigFile.I.executable_artifact_name("*"),
            path=PackageManager.I.dist_dir(),
            merge_multiple=True,
        )
