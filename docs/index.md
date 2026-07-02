# pyrig-executables Documentation

<!-- ci/cd -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-executables/health_check.yml?label=CI&logo=github)](https://github.com/Winipedia/pyrig-executables/actions/workflows/health_check.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-executables/deploy.yml?label=CD&logo=github)](https://github.com/Winipedia/pyrig-executables/actions/workflows/deploy.yml)
<!-- testing -->
[![CoverageTester](https://codecov.io/gh/Winipedia/pyrig-executables/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/pyrig-executables)
[![ProjectTester](https://img.shields.io/badge/tested%20with-pytest-46a2f1.svg?logo=pytest)](https://pytest.org)
<!-- code-quality -->
[![DependencyAuditor](https://img.shields.io/badge/security-pip--audit-blue?logo=python)](https://github.com/pypa/pip-audit)
[![DependencyChecker](https://img.shields.io/badge/dependencies-deptry-blue)](https://github.com/osprey-oss/deptry)
[![MarkdownLinter](https://img.shields.io/badge/markdown-rumdl-darkgreen)](https://github.com/rvben/rumdl)
[![PythonLinter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![SecurityChecker](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![SpellChecker](https://img.shields.io/badge/spell--check-typos-blue)](https://github.com/crate-ci/typos)
[![TypeChecker](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![VersionControlHookManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
<!-- tooling -->
[![PackageManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Pyrigger](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![RemoteVersionController](https://img.shields.io/github/stars/Winipedia/pyrig-executables?style=social)](https://github.com/Winipedia/pyrig-executables)
[![VersionController](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)](https://git-scm.com)
<!-- project-info -->
[![DocsBuilder](https://img.shields.io/badge/MkDocs-Documentation-326CE5?logo=mkdocs&logoColor=white)](https://Winipedia.github.io/pyrig-executables)
[![ExecutableBuilder](https://img.shields.io/github/downloads/Winipedia/pyrig-executables/total?logo=github&label=downloads)](https://github.com/Winipedia/pyrig-executables/releases)
[![PackageIndex](https://img.shields.io/pypi/v/pyrig-executables?logo=pypi&logoColor=white)](https://pypi.org/project/pyrig-executables)
[![ProgrammingLanguage](https://img.shields.io/pypi/pyversions/pyrig-executables)](https://www.python.org)
[![License](https://img.shields.io/github/license/Winipedia/pyrig-executables)](https://github.com/Winipedia/pyrig-executables/blob/main/LICENSE)

---

> A pyrig plugin to build executables.

---

## Overview

pyrig-executables turns a pyrig-managed project into standalone executables and
publishes them with every GitHub release. Installed as a development dependency,
it plugs into pyrig's config-generation and tooling system: the entry point, the
icon, the build tooling, and the release workflow steps needed to compile and
attach a per-OS binary are scaffolded, validated, and kept in sync
automatically. This page describes each piece; see the API Reference for the
generated, code-level documentation.

```bash
uv add pyrig-executables --dev
uv run pyrig sync
```

No tokens or secrets are required — the release workflow authenticates with the
automatic `GITHUB_TOKEN`. After `pyrig sync` you may need to fix up the badges in
`README.md` and `docs/index.md` once. The `pyinstaller` and `pillow` build
dependencies are added for you, so you can also build locally.

It builds on the
[pyrig-resources](https://github.com/Winipedia/pyrig-resources) plugin, which
provides the resources package the icon lives in and that is bundled into the
executable.

## Components

### Executable builder

`ExecutableBuilder` wraps PyInstaller. It builds the command that compiles a
single-file (`--onefile`) executable, applies the icon, and bundles the
project's resources package via `--collect-data`. It declares `pyinstaller` and
`pillow` as development dependencies, excludes the build artifacts (`dist/`,
`*.spec`, `build/`) from version control, and contributes a badge showing the
cumulative download count of the release binaries.

### Entry point

`MainConfigFile` scaffolds a `main.py` containing a `main` function and an
`if __name__ == "__main__"` guard — the target the executable is built from.
Validation only checks that a callable `main` and the guard are present, so your
own entry point is preserved.

### Icon

`IconConfigFile` copies the plugin's bundled default `icon.png` into the
project's resources package. The build passes it to `pyinstaller --icon`, which
converts it to the per-OS format (`.ico` on Windows, `.icns` on macOS; ignored
on Linux). It is created only when missing, so any icon you drop in is kept.

### Release workflow

The release workflow gains an `executable` matrix job that fans out across
Linux, Windows, and macOS — PyInstaller cannot cross-compile, so each binary is
built on its target platform. Every job builds and names the binary per OS so
the assets do not collide, and uploads it as a workflow artifact. The existing
`publish` job is gated on it, downloads every platform's binary, and attaches
them to the GitHub release alongside the changelog.

### Run command

`run` is a CLI command, invoked as `pyrig-executables run`, that executes your
project's `main.py` as the `__main__` module — the same way the built executable
runs it. It resolves and runs the entry point of whichever project invokes it,
so local runs mirror the shipped binary.

## API Reference

For class- and method-level details, see the [API](api.md) Reference, which is
generated automatically from the source.
