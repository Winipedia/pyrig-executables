"""Test module."""

from pyrig_resources.rig.configs.resources_init import ResourcesInitConfigFile

from pyrig_executables.rig.configs.version_control.remote.workflows.release import (
    ReleaseWorkflowConfigFile,
)
from pyrig_executables.rig.tools.version_control.remote.controller import (
    RemoteVersionController,
)


class TestReleaseWorkflowConfigFile:
    """Test class."""

    def test_artifact_name(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.artifact_name("${{ runner.os }}") == (
            "executable-${{ runner.os }}"
        )
        assert ReleaseWorkflowConfigFile.I.artifact_name("*") == "executable-*"

    def test_collect_all_modules(self) -> None:
        """Test method."""
        modules = ReleaseWorkflowConfigFile.I.collect_all_modules()
        assert modules == ()

    def test_collect_data_modules(self) -> None:
        """Test method."""
        modules = list(ReleaseWorkflowConfigFile.I.collect_data_modules())
        assert [module.__name__ for module in modules] == [
            "pyrig_executables.rig.resources",
        ]

    def test_create_release_args(self) -> None:
        """Test that executable artifacts are release arguments."""
        assert tuple(RemoteVersionController.I.create_release_args(tag="v1.2.3")) == (
            "gh",
            "release",
            "create",
            "v1.2.3",
            "dist/*",
            "--title=v1.2.3",
            "--generate-notes",
        )

    def test_create_release_args_preserves_additional_args(self) -> None:
        """Test that caller arguments and files are preserved."""
        assert tuple(
            RemoteVersionController.I.create_release_args(
                "--draft",
                tag="v1.2.3",
                files=("package.zip",),
            ),
        ) == (
            "gh",
            "release",
            "create",
            "v1.2.3",
            "dist/*",
            "package.zip",
            "--title=v1.2.3",
            "--generate-notes",
            "--draft",
        )

    def test_dependencies(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.dependencies() == (ResourcesInitConfigFile,)

    def test_insert_os(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.insert_os() == "${{ runner.os }}"

    def test_job_executable(self) -> None:
        """Test method."""
        job = ReleaseWorkflowConfigFile.I.job_executable()
        assert isinstance(job, dict)
        assert job["job_id"] == "executable"
        assert job["permissions"] == {"contents": "read"}
        assert "if" not in job

    def test_job_executable_permissions(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.job_executable_permissions() == {
            "contents": "read",
        }

    def test_job_publish(self) -> None:
        """Test method."""
        workflow = ReleaseWorkflowConfigFile.I
        job = workflow.job_publish()
        assert isinstance(job, dict)
        assert job["job_id"] == "publish"
        assert job["needs"] == ["health-check", "executable"]
        steps = job["steps"]
        ids = [step["id"] for step in steps]
        assert ids.index("download-executables") < ids.index("create-release")

    def test_job_publish_needs(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.job_publish_needs() == (
            ReleaseWorkflowConfigFile.I.job_health_check,
            ReleaseWorkflowConfigFile.I.job_executable,
        )

    def test_jobs(self) -> None:
        """Test method."""
        workflow = ReleaseWorkflowConfigFile.I
        jobs = workflow.jobs()
        assert isinstance(jobs, tuple)
        assert workflow.job_executable in jobs
        assert workflow.job_publish in jobs

    def test_step_build_executable(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.step_build_executable() == {
            "name": "Build Executable",
            "id": "build-executable",
            "run": r"""uv \
run \
pyinstaller \
--onefile \
--name=pyrig-executables-"${OS}" \
--icon=src/pyrig_executables/rig/resources/icon.png \
--collect-data=pyrig_executables.rig.resources \
src/pyrig_executables/main.py""",
            "env": {
                "OS": "${{ runner.os }}",
            },
        }

    def test_step_download_executables(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.step_download_executables() == {
            "name": "Download Executables",
            "id": "download-executables",
            "uses": (
                "actions/download-artifact@"
                f"{ReleaseWorkflowConfigFile.I.action_download_artifact()[1]}"
            ),
            "with": {
                "pattern": "executable-*",
                "path": "dist",
                "merge-multiple": "true",
            },
        }

    def test_step_upload_executable(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.step_upload_executable() == {
            "name": "Upload Executable",
            "id": "upload-executable",
            "uses": (
                "actions/upload-artifact@"
                f"{ReleaseWorkflowConfigFile.I.action_upload_artifact()[1]}"
            ),
            "with": {
                "name": "executable-${{ runner.os }}",
                "path": "dist",
                "if-no-files-found": "error",
            },
        }

    def test_steps_executable(self) -> None:
        """Test method."""
        steps = ReleaseWorkflowConfigFile.I.steps_executable()
        names = [step["name"] for step in steps]
        assert "Build Executable" in names
        assert "Upload Executable" in names

    def test_steps_publish(self) -> None:
        """Test method."""
        steps = ReleaseWorkflowConfigFile.I.steps_publish()
        ids = [step["id"] for step in steps]
        assert "download-executables" in ids
        assert "create-release" in ids
        assert ids.index("download-executables") < ids.index("create-release")
