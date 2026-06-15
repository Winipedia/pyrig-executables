"""Test module."""

from pyrig_executables.rig.configs.remote_version_control.workflows.release import (
    ReleaseWorkflowConfigFile,
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

    def test_job_publish(self) -> None:
        """Test method."""
        job = ReleaseWorkflowConfigFile.I.job_publish()
        assert isinstance(job, dict)
        assert "publish" in job
        assert job["publish"]["needs"] == ["executable"]

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
            "run": (
                "uv run pyinstaller --onefile --windowed --name pyrig-executables-${{ runner.os }} src/pyrig_executables/main.py"  # noqa: E501
            ),
        }

    def test_step_upload_executable(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.step_upload_executable() == {
            "name": "Upload Executable",
            "id": "upload-executable",
            "uses": "actions/upload-artifact@main",
            "with": {
                "name": "pyrig-executables-${{ runner.os }}",
                "path": "dist",
            },
        }

    def test_step_download_executables(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.step_download_executables() == {
            "name": "Download Executables",
            "id": "download-executables",
            "uses": "actions/download-artifact@main",
            "with": {
                "pattern": "pyrig-executables*",
                "path": "dist",
                "merge-multiple": "true",
            },
        }

    def test_step_create_release(self) -> None:
        """Test method."""
        step = ReleaseWorkflowConfigFile.I.step_create_release()
        assert step["id"] == "create-release"
        assert step["with"]["artifacts"] == "dist/*"

    def test_executable_name(self) -> None:
        """Test method."""
        assert (
            ReleaseWorkflowConfigFile.I.executable_name()
            == "pyrig-executables-${{ runner.os }}"
        )

    def test_insert_os(self) -> None:
        """Test method."""
        assert ReleaseWorkflowConfigFile.I.insert_os() == "${{ runner.os }}"
