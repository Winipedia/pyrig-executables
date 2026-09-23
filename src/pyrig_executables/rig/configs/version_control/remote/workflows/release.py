"""Extension of the release workflow that builds and attaches executables."""

from collections.abc import Iterable
from types import MethodType, ModuleType
from typing import Any

from pyrig.rig.configs.base.config_file import ConfigFile
from pyrig.rig.configs.version_control.remote.workflows.release import (
    ReleaseWorkflowConfigFile as BaseReleaseWorkflowConfigFile,
)
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig_resources.rig.configs.resources_init import ResourcesInitConfigFile

from pyrig_executables.rig import resources
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

    def job_publish_needs(self) -> tuple[MethodType, ...]:
        """Return the jobs required before publishing a release.

        Returns:
            The base class's dependencies plus the executable build job.
        """
        return (*super().job_publish_needs(), self.job_executable)

    def steps_publish(self) -> list[dict[str, Any]]:
        """Build the ordered steps for the release job.

        Inserts a step that downloads every platform's executable immediately
        before the create-release step, since the release must not be
        created before every binary is available to attach.

        Returns:
            The base publish steps with the executable download step inserted
            just before the create-release step.
        """
        steps = super().steps_publish()
        create_release_id = self.step_id_from_method(self.step_create_release)
        create_release_index = next(
            index for index, step in enumerate(steps) if step["id"] == create_release_id
        )
        steps.insert(create_release_index, self.step_download_executables())
        return steps

    def dependencies(self) -> Iterable[type[ConfigFile[Any]]]:
        """Return config files required before building the workflow.

        The `ResourcesInitConfigFile` is required because it is needed as a
        loaded module in `collect_data_modules`.

        Returns:
            Direct config file dependencies for this workflow.
        """
        return (*super().dependencies(), ResourcesInitConfigFile)

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
            permissions=self.permission_contents(),
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

    def step_build_executable(self) -> dict[str, Any]:
        """Build a step that compiles the project into a single-file executable.

        Runs `pyinstaller --onefile` against the project's entry-point
        module, naming the output binary via `executable_name`.

        Returns:
            Step that runs the executable builder via uv.
        """
        os_var = "OS"
        return self.step(
            self.step_build_executable,
            run=PackageManager.I.run_args(
                *ExecutableBuilder.I.build_args(
                    name=f"{PackageManager.I.project_name()}-{self.insert_parameter_expansion(os_var)}",
                    entry_point=MainConfigFile.I.path(),
                    icon=IconConfigFile.I.path(),
                    collect_all_modules=self.collect_all_modules(),
                    collect_data_modules=self.collect_data_modules(),
                ),
            ).multiline(),
            env={
                os_var: self.insert_os(),
            },
        )

    def step_upload_executable(self) -> dict[str, Any]:
        """Build a step that uploads the built executable as a workflow artifact.

        Uploads the contents of `dist/` under the per-OS `artifact_name` so
        the `publish` job can later download every platform's binary.

        Returns:
            Step using `actions/upload-artifact@<ref>`.
        """
        return self.step(
            self.step_upload_executable,
            uses=self.upload_artifact_action(),
            with_={
                "name": self.artifact_name(self.insert_os()),
                "path": PackageManager.I.dist_dir().as_posix(),
            },
        )

    def upload_artifact_action(self) -> tuple[str, str, str]:
        """Return action metadata for `actions/upload-artifact`.

        Returns:
            Tuple of action name, pinned commit SHA, and release tag.
        """
        return self.action_from_resource(self.upload_artifact_action, resources)

    def step_download_executables(self) -> dict[str, Any]:
        """Build a step that downloads every executable artifact into `dist/`.

        Merges every per-OS executable artifact, matched by the
        `artifact_name` glob, into a single `dist/` directory so they can be
        attached to the release with one glob.

        Returns:
            Step using `actions/download-artifact@<ref>`.
        """
        return self.step(
            self.step_download_executables,
            uses=self.download_artifact_action(),
            with_={
                "pattern": self.artifact_name("*"),
                "path": PackageManager.I.dist_dir().as_posix(),
                "merge-multiple": "true",
            },
        )

    def download_artifact_action(self) -> tuple[str, str, str]:
        """Return action metadata for `actions/download-artifact`.

        Returns:
            Tuple of action name, pinned commit SHA, and release tag.
        """
        return self.action_from_resource(self.download_artifact_action, resources)

    def artifact_name(self, os: str) -> str:
        """Build the workflow-artifact name for the given runner OS.

        Single source of the `executable-<os>` artifact label. Kept
        deliberately generic and distinct from `executable_name`, so it does
        not collide with artifacts that other actions may name after the
        project.

        Args:
            os: The runner OS suffix, or `"*"` to build a name matching
                every OS.

        Returns:
            The `executable-<os>` artifact name.
        """
        return f"executable-{os}"

    def insert_os(self) -> str:
        """Return the expression that resolves to the current runner's OS.

        Returns:
            GitHub Actions expression for `runner.os` (e.g. `Linux`,
            `Windows`, `macOS`).
        """
        return self.insert_expression("runner.os")

    def collect_all_modules(self) -> Iterable[ModuleType]:
        """Return the modules to bundle in full (data, submodules, binaries).

        Empty by default, since the project's own resources package is pure
        data and is covered by `collect_data_modules` instead. Override to
        bundle additional modules that ship submodules or binaries alongside
        their data.

        Returns:
            No modules, by default.
        """
        return ()

    def collect_data_modules(self) -> Iterable[ModuleType]:
        """Return the resource modules whose data files to bundle into the executable.

        Resolves the project's `rig/resources` package, the location the
        `pyrig-resources` plugin scaffolds and validates. Locating the
        project's resources is a config concern, so it lives here rather than
        in the project-agnostic executable builder tool. Override to bundle
        additional pure-data resource packages.

        Returns:
            The project's resource modules (the `rig/resources` package).
        """
        return (ResourcesInitConfigFile.I.module(),)
