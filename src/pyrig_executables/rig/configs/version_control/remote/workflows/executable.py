"""Reusable workflow for building standalone executables."""

from collections.abc import Callable
from typing import Any, override

from pyrig.core.subprocesses import Args
from pyrig.rig.configs.base.workflow import WorkflowConfigFile
from pyrig.rig.tools.formatting.shell import ShellFormatter
from pyrig.rig.tools.packages.manager import PackageManager

from pyrig_executables.rig.configs.build_executable import BuildExecutableConfigFile


class ExecutableWorkflowConfigFile(WorkflowConfigFile):
    """Build and upload an executable for each supported operating system."""

    @override
    def concurrency_cancel_in_progress(self) -> bool:
        """Return `False`; release builds must not be cancelled."""
        return False

    @override
    def jobs(self) -> tuple[Callable[[], dict[str, Any]], ...]:
        """Return the executable build matrix."""
        return (self.job_build,)

    @override
    def stem(self) -> str:
        """Return the workflow file stem, `executable`."""
        return "executable"

    @override
    def workflow_triggers(self) -> dict[str, Any]:
        """Return a reusable-workflow trigger."""
        return self.on_workflow_call()

    def job_build(self) -> dict[str, Any]:
        """Build and upload executables on their target platforms."""
        return self.job(
            self.job_build,
            strategy=self.strategy_matrix_os(),
            permissions=self.job_build_permissions(),
            runs_on=self.insert_matrix_os(),
            steps=self.steps_build(),
            timeout_minutes=60,
        )

    def job_build_permissions(self) -> dict[str, str]:
        """Return read-only repository permissions for checkout."""
        return self.permission_contents()

    def steps_build(self) -> list[dict[str, Any]]:
        """Return setup, executable build, and artifact-upload steps."""
        return [
            *self.steps_core_installed_setup(),
            self.step_build_executable(),
            self.step_upload_executable(),
        ]

    def step_build_executable(self) -> dict[str, Any]:
        """Run the generated executable build script."""
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
        """Upload this platform's executable artifact."""
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
