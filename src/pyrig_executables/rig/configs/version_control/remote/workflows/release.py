"""Extension of the release workflow that builds and attaches executables."""

from collections.abc import Iterable
from types import ModuleType
from typing import Any

from pyrig.rig.configs.base.config_file import Priority
from pyrig.rig.configs.version_control.remote.workflows.release import (
    ReleaseWorkflowConfigFile as BaseReleaseWorkflowConfigFile,
)
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig_resources.rig.configs.resources_init import ResourcesInitConfigFile

from pyrig_executables.rig.configs.icon import IconConfigFile
from pyrig_executables.rig.configs.main import MainConfigFile
from pyrig_executables.rig.tools.executables.builder import ExecutableBuilder


class ReleaseWorkflowConfigFile(BaseReleaseWorkflowConfigFile):
    """Release workflow that builds and attaches standalone executables.

    Extends the base release workflow with a matrix job that builds a
    single-file executable for every supported operating system and attaches
    each one to the GitHub release as a release asset, alongside the
    generated changelog.
    """

    def jobs(self) -> dict[str, Any]:
        """Build the complete set of workflow jobs.

        Adds the executable build job to the base release jobs.

        Returns:
            Dict containing the executable build job together with the base
            release jobs.
        """
        return {
            **self.job_executable(),
            **super().jobs(),
        }

    def job_publish(self) -> dict[str, Any]:
        """Build the release job, gated on the executable build job.

        Adds a `needs` dependency on `executable` so the release is
        only published once every platform's binary is available to attach.

        Returns:
            The base release job with a `needs` dependency added.
        """
        jobs = super().job_publish()
        jobs[self.id_from_method(self.job_publish)]["needs"] = [
            self.id_from_method(self.job_executable),
        ]
        return jobs

    def steps_publish(self) -> list[dict[str, Any]]:
        """Build the ordered steps for the release job.

        Extends the base steps with a download step that pulls every platform's
        executable into `dist/` immediately before the release is created.

        Returns:
            The base publish steps with the executable download step inserted
            just before the create-release step.
        """
        steps = super().steps_publish()
        create_release_id = self.id_from_method(self.step_create_release)
        create_release_index = next(
            index for index, step in enumerate(steps) if step["id"] == create_release_id
        )
        steps.insert(create_release_index, self.step_download_executables())
        return steps

    def step_create_release(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build the create-release step, attaching the built executables.

        Extends the base release step by attaching every binary downloaded into
        `dist/` as a release asset.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            The base create-release step with `dist/*` added as artifacts.
        """
        step = super().step_create_release(step=step)
        step["with"]["artifacts"] = (ExecutableBuilder.I.dist_dir() / "*").as_posix()
        return step

    def priority(self) -> float:
        """Return a priority one step after the resources config's.

        Building the executable requires the project's resources package to
        already exist, so this config must validate after it. Deriving from
        its priority instead of hard-coding a value keeps this config's
        priority in step with any future change to the resources config's own
        priority.

        Returns:
            The resources config's priority lowered by one `Priority.STEP`.
        """
        return Priority.decrease(ResourcesInitConfigFile.I.priority())

    def job_executable(self) -> dict[str, Any]:
        """Build the matrix job that compiles the executable on every OS.

        Runs across the default OS matrix (Linux, Windows, macOS), since
        `pyinstaller` cannot cross-compile and each binary must be built on
        its target platform.

        Returns:
            Job configuration with an OS matrix strategy, a dynamic `runs-on`
            value, and the build and upload steps.
        """
        return self.job(
            self.job_executable,
            strategy=self.strategy_matrix_os(),
            runs_on=self.insert_matrix_os(),
            steps=self.steps_executable(),
        )

    def steps_executable(self) -> list[dict[str, Any]]:
        """Build the ordered steps for the executable build job.

        Returns:
            Steps that set up the environment, build the single-file
            executable, and upload it as a per-OS artifact.
        """
        return [
            *self.steps_core_installed_setup(),
            self.step_build_executable(),
            self.step_upload_executable(),
        ]

    def step_build_executable(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that compiles the project into a single-file executable.

        Runs `pyinstaller --onefile` against the project's entry-point module,
        naming the binary after the project and the current runner OS so the
        per-platform assets do not collide on the release.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step that runs the executable builder via uv.
        """
        return self.step(
            self.step_build_executable,
            run=" \\\n".join(
                PackageManager.I.run_args(
                    *ExecutableBuilder.I.build_args(
                        name=self.executable_name(),
                        entry_point=MainConfigFile.I.path(),
                        icon=IconConfigFile.I.path(),
                        resource_modules=self.resource_modules(),
                    ),
                ),
            ),
            step=step,
        )

    def step_upload_executable(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that uploads the built executable as a workflow artifact.

        Uploads the contents of `dist/` under the per-OS `artifact_name` so
        the `publish` job can later download every platform's binary.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step using `actions/upload-artifact@main`.
        """
        return self.step(
            self.step_upload_executable,
            uses="actions/upload-artifact@main",
            with_={
                "name": self.artifact_name(self.insert_os()),
                "path": ExecutableBuilder.I.dist_dir().as_posix(),
            },
            step=step,
        )

    def step_download_executables(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a step that downloads every executable artifact into `dist/`.

        Merges every per-OS executable artifact, matched by the
        `artifact_name` glob, into a single `dist/` directory so they can be
        attached to the release with one glob. The narrow prefix avoids
        pulling in unrelated artifacts that other actions may name after the
        project.

        Args:
            step: Additional keys to merge into the step configuration.

        Returns:
            Step using `actions/download-artifact@main`.
        """
        return self.step(
            self.step_download_executables,
            uses="actions/download-artifact@main",
            with_={
                "pattern": self.artifact_name("*"),
                "path": ExecutableBuilder.I.dist_dir().as_posix(),
                "merge-multiple": "true",
            },
            step=step,
        )

    def artifact_name(self, os: str) -> str:
        """Build the workflow-artifact name for the given runner OS.

        Single source of the `executable-<os>` artifact label, shared by the
        upload step (with the resolved runner OS) and the download step (with
        `"*"` to match every platform). It is deliberately generic and
        distinct from `executable_name` so it does not collide with
        artifacts that other actions name after the project.

        Args:
            os: The runner OS suffix, or `"*"` to form the download glob.

        Returns:
            The `executable-<os>` artifact name.
        """
        return f"executable-{os}"

    def executable_name(self) -> str:
        """Build the per-OS name of the executable binary and release asset.

        Combines the project name with the runner OS so each platform's binary
        gets a unique, recognizable, collision-free name (e.g.
        `pyrig-executables-Linux`). The OS is resolved at workflow runtime.

        Returns:
            The `<project>-<os>` name string.
        """
        return f"{PackageManager.I.project_name()}-{self.insert_os()}"

    def insert_os(self) -> str:
        """Get the `${{ runner.os }}` expression.

        Returns:
            GitHub Actions expression resolving to the current runner's
            operating system (e.g. `Linux`, `Windows`, `macOS`).
        """
        return self.insert_expression("runner.os")

    def resource_modules(self) -> Iterable[ModuleType]:
        """Return the resource modules to bundle into the executable.

        Resolves the project's `rig/resources` package, the location the
        `pyrig-resources` plugin scaffolds and validates. Locating the
        project's resources is a config concern, so it lives here rather than
        in the project-agnostic executable builder tool. Override to bundle
        additional resource packages.

        Returns:
            The project's resource modules (the `rig/resources` package).
        """
        return (ResourcesInitConfigFile.I.module(),)
