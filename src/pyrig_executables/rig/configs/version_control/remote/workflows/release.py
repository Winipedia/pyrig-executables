"""Extension of the release workflow that builds and attaches executables."""

from collections.abc import Callable
from types import MethodType
from typing import Any, override

from pyrig.core.subprocesses import Args
from pyrig.rig.configs.version_control.remote.workflows.release import (
    ReleaseWorkflowConfigFile as BaseReleaseWorkflowConfigFile,
)
from pyrig.rig.tools.formatting.shell import ShellFormatter
from pyrig.rig.tools.packages.manager import PackageManager

from pyrig_executables.rig.configs.build_executable import BuildExecutableConfigFile


class ReleaseWorkflowConfigFile(BaseReleaseWorkflowConfigFile):
    """Extend the release workflow to build and attach executables."""

    @override
    def job_publish_needs(self) -> tuple[MethodType, ...]:
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
    def steps_publish(self) -> list[dict[str, Any]]:
        """Insert executable downloads immediately before release creation."""
        steps = super().steps_publish()
        create_release_id = self.step_id_from_method(self.step_create_release)
        create_release_index = next(
            index for index, step in enumerate(steps) if step["id"] == create_release_id
        )
        steps.insert(create_release_index, self.step_download_executables())
        return steps

    def job_executable(self) -> dict[str, Any]:
        """Build the matrix job that compiles the executable."""
        return self.job(
            self.job_executable,
            strategy=self.strategy_matrix_os(),
            permissions=self.job_executable_permissions(),
            runs_on=self.insert_matrix_os(),
            steps=self.steps_executable(),
            timeout_minutes=60,
        )

    def step_download_executables(self) -> dict[str, Any]:
        """Build a step that merges executable artifacts into `dist/`."""
        return self.step_download_artifact(
            self.step_download_executables,
            pattern=self.executable_artifact_name("*"),
            path=PackageManager.I.dist_dir(),
            merge_multiple=True,
        )

    def job_executable_permissions(self) -> dict[str, Any]:
        """Return the permissions for the executable build job."""
        return self.permission_contents()

    def steps_executable(self) -> list[dict[str, Any]]:
        """Return the setup, build, and artifact-upload steps."""
        return [
            *self.steps_core_installed_setup(),
            self.step_build_executable(),
            self.step_upload_executable(),
        ]

    def step_build_executable(self) -> dict[str, Any]:
        """Build a step that runs the generated build script."""
        return self.step(
            self.step_build_executable,
            run=str(
                Args(
                    ShellFormatter.I.dialect(),
                    BuildExecutableConfigFile.I.path().as_posix(),
                ),
            ),
        )

    def step_upload_executable(self) -> dict[str, Any]:
        """Build a step that uploads the executable artifact."""
        return self.step_upload_artifact(
            self.step_upload_executable,
            name=self.executable_artifact_name(self.insert_matrix_os()),
            path=PackageManager.I.dist_dir(),
        )

    def executable_artifact_name(self, os: str) -> str:
        """Return the workflow-artifact name for a runner.

        Args:
            os: Matrix OS label, or `"*"` to match every OS.
        """
        return f"executable-{os}"
