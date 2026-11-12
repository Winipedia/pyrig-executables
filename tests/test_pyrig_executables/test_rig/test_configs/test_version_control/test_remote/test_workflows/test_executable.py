"""Tests for the reusable executable workflow."""

from pyrig_executables.rig.configs.version_control.remote.workflows.executable import (
    ExecutableWorkflowConfigFile,
)


class TestExecutableWorkflowConfigFile:
    """Test executable build and artifact generation."""

    def test_concurrency_cancel_in_progress(self) -> None:
        """Check release builds are not cancelled."""
        assert ExecutableWorkflowConfigFile.I.concurrency_cancel_in_progress() is False

    def test_executable_artifact_name(self) -> None:
        """Check matrix and wildcard artifact names."""
        workflow = ExecutableWorkflowConfigFile.I
        assert workflow.executable_artifact_name("${{ matrix.os }}") == (
            "executable-${{ matrix.os }}"
        )
        assert workflow.executable_artifact_name("*") == "executable-*"

    def test_job_build(self) -> None:
        """Check the build matrix and permissions."""
        workflow = ExecutableWorkflowConfigFile.I
        job = workflow.job_build()
        timeout = 60
        assert job["job_id"] == "build"
        assert job["permissions"] == {"contents": "read"}
        assert job["runs-on"] == "${{ matrix.os }}"
        assert job["strategy"] == {
            "matrix": {"os": ["ubuntu-latest", "windows-latest", "macos-latest"]},
            "fail-fast": True,
        }
        assert job["timeout-minutes"] == timeout
        assert job["steps"] == workflow.steps_build()
        assert "environment" not in job

    def test_job_build_permissions(self) -> None:
        """Check checkout is read-only."""
        assert ExecutableWorkflowConfigFile.I.job_build_permissions() == {
            "contents": "read",
        }

    def test_jobs(self) -> None:
        """Check the workflow contains the build matrix."""
        workflow = ExecutableWorkflowConfigFile.I
        assert workflow.jobs() == (workflow.job_build,)

    def test_stem(self) -> None:
        """Check the workflow filename."""
        assert ExecutableWorkflowConfigFile.I.stem() == "executable"

    def test_step_build_executable(self) -> None:
        """Check the generated build script is invoked."""
        assert ExecutableWorkflowConfigFile.I.step_build_executable() == {
            "name": "Build Executable",
            "id": "build-executable",
            "run": "bash build-executable.sh",
        }

    def test_step_upload_executable(self) -> None:
        """Check per-platform artifacts keep their names and fail if missing."""
        step = ExecutableWorkflowConfigFile.I.step_upload_executable()
        assert step["uses"].startswith("actions/upload-artifact@")
        assert step["with"] == {
            "name": "executable-${{ matrix.os }}",
            "path": "dist",
            "if-no-files-found": "error",
        }

    def test_steps_build(self) -> None:
        """Check setup precedes building and uploading."""
        steps = ExecutableWorkflowConfigFile.I.steps_build()
        assert [step["id"] for step in steps] == [
            "checkout-repository",
            "setup-package-manager",
            "install-dependencies",
            "build-executable",
            "upload-executable",
        ]

    def test_workflow_triggers(self) -> None:
        """Check the workflow accepts calls without named secrets."""
        assert ExecutableWorkflowConfigFile.I.workflow_triggers() == {
            "workflow_call": {},
        }
