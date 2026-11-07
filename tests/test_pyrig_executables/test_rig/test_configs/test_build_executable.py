"""Tests for the generated executable build script."""

from pathlib import Path

import pytest
from pyrig.core.subprocesses import Args
from pyrig_resources.rig.configs.resources_init import ResourcesInitConfigFile
from pytest_mock import MockerFixture

from pyrig_executables.rig import resources
from pyrig_executables.rig.configs.build_executable import BuildExecutableConfigFile


class TestBuildExecutableConfigFile:
    """Test the build script's path, prerequisites, and command."""

    def test_collect_all_modules(self) -> None:
        """Test that no modules are bundled in full by default."""
        assert BuildExecutableConfigFile.I.collect_all_modules() == ()

    def test_collect_data_modules(self) -> None:
        """Test that the project's resources package is bundled as data."""
        modules = BuildExecutableConfigFile.I.collect_data_modules()
        assert [module.__name__ for module in modules] == [
            "pyrig_executables.rig.resources",
        ]

    def test_dependencies(self) -> None:
        """Test that only the imported resource package is a hard dependency."""
        assert BuildExecutableConfigFile.I.dependencies() == (ResourcesInitConfigFile,)

    def test_parent_path(self) -> None:
        """Test that the platform-independent script lives at the project root."""
        assert BuildExecutableConfigFile.I.parent_path() == Path()

    def test_required_env_vars(self) -> None:
        """Test that no caller-provided environment variables are required."""
        assert BuildExecutableConfigFile.I.required_env_vars() == ()

    def test_script(self) -> None:
        """Test that the original build command and shared header are preserved."""
        script = BuildExecutableConfigFile.I
        assert (
            script.script()
            == r"""uv \
  run \
  pyinstaller \
  --onefile \
  --name=pyrig-executables-"${OSTYPE}" \
  --icon=src/pyrig_executables/rig/resources/icon.png \
  --collect-data=pyrig_executables.rig.resources \
  src/pyrig_executables/main.py
"""
        )
        assert script.content() == (
            "#!/usr/bin/env bash\nset -euo pipefail\n\n" + script.script()
        )

    def test_script_collect_modules(self, mocker: MockerFixture) -> None:
        """Test that module-bundling overrides affect the generated command."""
        mocker.patch.object(
            BuildExecutableConfigFile,
            "collect_all_modules",
            return_value=(resources,),
        )
        mocker.patch.object(
            BuildExecutableConfigFile,
            "collect_data_modules",
            return_value=(),
        )
        script = BuildExecutableConfigFile.I.script()
        assert "--collect-all=pyrig_executables.rig.resources" in script
        assert "--collect-data=" not in script

    @pytest.mark.parametrize("os_type", ["linux-gnu", "darwin25", "msys", "cygwin"])
    def test_script_execution(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        os_type: str,
    ) -> None:
        """Test Bash expansion and build arguments without invoking PyInstaller."""
        monkeypatch.delenv("OS", raising=False)
        script = tmp_path / "build-executable.sh"
        script.write_text(BuildExecutableConfigFile.I.content(), encoding="utf-8")
        result = Args(
            "bash",
            "-c",
            'OSTYPE="$2"; uv() { printf "%s\\n" "$@"; }; source "$1"',
            "bash",
            str(script),
            os_type,
        ).run()
        assert result.stdout.splitlines() == [
            "run",
            "pyinstaller",
            "--onefile",
            f"--name=pyrig-executables-{os_type}",
            "--icon=src/pyrig_executables/rig/resources/icon.png",
            "--collect-data=pyrig_executables.rig.resources",
            "src/pyrig_executables/main.py",
        ]

    def test_script_execution_failure(
        self,
        tmp_path: Path,
    ) -> None:
        """Test that a failed build is propagated to the caller."""
        script = tmp_path / "build-executable.sh"
        script.write_text(BuildExecutableConfigFile.I.content(), encoding="utf-8")
        result = Args(
            "bash",
            "-c",
            'uv() { return 1; }; export -f uv; bash "$1"',
            "bash",
            str(script),
        ).run(check=False)
        assert result.returncode == 1

    @pytest.mark.parametrize("os_name", [None, "", "ignored"])
    def test_script_execution_without_os(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        os_name: str | None,
    ) -> None:
        """Test that Bash supplies the suffix independently of the OS variable."""
        monkeypatch.delenv("OS", raising=False)
        if os_name is not None:
            monkeypatch.setenv("OS", os_name)
        script = tmp_path / "build-executable.sh"
        script.write_text(BuildExecutableConfigFile.I.content(), encoding="utf-8")
        result = Args(
            "bash",
            "-c",
            'uv() { printf "%s\\n" "$@"; }; export -f uv; '
            'printf "%s\\n" "$OSTYPE"; bash "$1"',
            "bash",
            str(script),
        ).run()
        os_type, *arguments = result.stdout.splitlines()
        assert os_type
        assert f"--name=pyrig-executables-{os_type}" in arguments

    def test_stem(self) -> None:
        """Test the generated script's filename."""
        assert BuildExecutableConfigFile.I.stem() == "build-executable"
        assert BuildExecutableConfigFile.I.path() == Path("build-executable.sh")
