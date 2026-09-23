"""Test module."""

from pyrig.core.resources import resource_content
from pyrig.core.strings import read_text_utf8
from pyrig_resources.rig.configs.resources_init import ResourcesInitConfigFile

from pyrig_executables.rig import resources
from pyrig_executables.rig.configs.version_control.remote.workflows.release import (
    ReleaseWorkflowConfigFile,
)
from pyrig_executables.rig.tools.version_control.remote.controller import (
    RemoteVersionController,
)


class TestReleaseWorkflowConfigFile:
    """Test class."""

    def test_jobs(self) -> None:
        """Test method."""
        jobs = ReleaseWorkflowConfigFile.I.jobs()
        assert isinstance(jobs, dict)
        assert "executable" in jobs
        assert "publish" in jobs

    def test_job_executable(self) -> None:
        """Test method."""
        job = ReleaseWorkflowConfigFile.I.job_executable()
        assert isinstance(job, dict)
        assert "executable" in job
        assert len(job) == 1
        assert job["executable"]["permissions"] == {"contents": "read"}
        assert "if" not in job["executable"]

    def test_job_publish(self) -> None:
        """Test method."""
        job = ReleaseWorkflowConfigFile.I.job_publish()
        assert isinstance(job, dict)
        assert "publish" in job
        assert job["publish"]["needs"] == ["health-check", "executable"]

    def test_job_publish_needs(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.job_publish_needs() == (
            ReleaseWorkflowConfigFile.I.job_health_check,
            ReleaseWorkflowConfigFile.I.job_executable,
        )

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

    def test_step_upload_executable(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.step_upload_executable() == {
            "name": "Upload Executable",
            "id": "upload-executable",
            "uses": (
                "actions/upload-artifact@"
                f"{ReleaseWorkflowConfigFile.I.upload_artifact_action()[1]}"
            ),
            "with": {
                "name": "executable-${{ runner.os }}",
                "path": "dist",
            },
        }

    def test_step_download_executables(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.step_download_executables() == {
            "name": "Download Executables",
            "id": "download-executables",
            "uses": (
                "actions/download-artifact@"
                f"{ReleaseWorkflowConfigFile.I.download_artifact_action()[1]}"
            ),
            "with": {
                "pattern": "executable-*",
                "path": "dist",
                "merge-multiple": "true",
            },
        }

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

    def test_artifact_name(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.artifact_name("${{ runner.os }}") == (
            "executable-${{ runner.os }}"
        )
        assert ReleaseWorkflowConfigFile.I.artifact_name("*") == "executable-*"

    def test_insert_os(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.insert_os() == "${{ runner.os }}"

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

    def test_upload_artifact_action(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.upload_artifact_action() == tuple(
            resource_content("UPLOAD_ARTIFACT_ACTION", resources).splitlines(),
        )

        action, ref, tag = ReleaseWorkflowConfigFile.I.upload_artifact_action()
        assert f'"uses": "{action}@{ref}"  # {tag}' in read_text_utf8(
            ReleaseWorkflowConfigFile.I.path(),
        )

    def test_download_artifact_action(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.download_artifact_action() == tuple(
            resource_content("DOWNLOAD_ARTIFACT_ACTION", resources).splitlines(),
        )

        action, ref, tag = ReleaseWorkflowConfigFile.I.download_artifact_action()
        assert f'"uses": "{action}@{ref}"  # {tag}' in read_text_utf8(
            ReleaseWorkflowConfigFile.I.path(),
        )

    def test_dependencies(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.dependencies() == (ResourcesInitConfigFile,)
