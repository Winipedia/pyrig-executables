"""Test module."""

from pyrig_executables.rig.configs.version_control.remote.workflows.release import (
    ReleaseWorkflowConfigFile,
)
from pyrig_executables.rig.tools.version_control.remote.controller import (
    RemoteVersionController,
)


class TestReleaseWorkflowConfigFile:
    """Test class."""

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

    def test_job_executable(self) -> None:
        """Test method."""
        job = ReleaseWorkflowConfigFile.I.job_executable()
        assert isinstance(job, dict)
        assert job["job_id"] == "executable"
        assert job["permissions"] == {"contents": "read"}
        assert job["uses"] == "$/.github/workflows/executable.yml"
        assert "runs-on" not in job
        assert "strategy" not in job
        assert "steps" not in job
        assert "secrets" not in job

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

    def test_steps_publish(self) -> None:
        """Test method."""
        steps = ReleaseWorkflowConfigFile.I.steps_publish()
        ids = [step["id"] for step in steps]
        assert "download-executables" in ids
        assert "create-release" in ids
        assert ids.index("download-executables") < ids.index("create-release")
