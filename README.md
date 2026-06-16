# pyrig-executables

<!-- security -->
[![DependencyAuditor](https://img.shields.io/badge/security-pip--audit-blue?logo=python)](https://github.com/pypa/pip-audit)
[![SecurityChecker](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
<!-- ci/cd -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-executables/health_check.yml?label=CI&logo=github)](https://github.com/Winipedia/pyrig-executables/actions/workflows/health_check.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-executables/deploy.yml?label=CD&logo=github)](https://github.com/Winipedia/pyrig-executables/actions/workflows/deploy.yml)
<!-- code-quality -->
[![MarkdownLinter](https://img.shields.io/badge/markdown-rumdl-darkgreen)](https://github.com/rvben/rumdl)
[![PythonLinter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![TypeChecker](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![VersionControlHookManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
<!-- testing -->
[![CoverageTester](https://codecov.io/gh/Winipedia/pyrig-executables/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/pyrig-executables)
[![ProjectTester](https://img.shields.io/badge/tested%20with-pytest-46a2f1.svg?logo=pytest)](https://pytest.org)
<!-- tooling -->
[![PackageManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Pyrigger](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![RemoteVersionController](https://img.shields.io/github/stars/Winipedia/pyrig-executables?style=social)](https://github.com/Winipedia/pyrig-executables)
[![VersionController](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)](https://git-scm.com)
<!-- documentation -->
[![DocsBuilder](https://img.shields.io/badge/MkDocs-Documentation-326CE5?logo=mkdocs&logoColor=white)](https://www.mkdocs.org)
[![Documentation](https://img.shields.io/badge/Docs-GitHub%20Pages-black?style=for-the-badge&logo=github&logoColor=white)](https://Winipedia.github.io/pyrig-executables)
<!-- project-info -->
[![ExecutableBuilder](https://img.shields.io/github/downloads/Winipedia/pyrig-executables/total?logo=github&label=downloads)](https://github.com/Winipedia/pyrig-executables/releases)
[![PackageIndex](https://img.shields.io/pypi/v/pyrig-executables?logo=pypi&logoColor=white)](https://pypi.org/project/pyrig-executables)
[![ProgrammingLanguage](https://img.shields.io/pypi/pyversions/pyrig-executables)](https://www.python.org)
[![License](https://img.shields.io/github/license/Winipedia/pyrig-executables)](https://github.com/Winipedia/pyrig-executables/blob/main/LICENSE)

---

> A pyrig plugin to build executables.

---

## What is pyrig-executables

pyrig-executables is a plugin for [pyrig](https://github.com/Winipedia/pyrig)
that turns your project into standalone, downloadable executables and publishes
them with every GitHub release — one self-contained binary per operating system.

## Features

### Standalone executables

Builds a single-file executable of your project for Linux, Windows, and macOS
and attaches each one to the GitHub release, so anyone can download and run it
without installing Python.

### Release workflow integration

Extends pyrig's release workflow with a build job that compiles the binaries
with PyInstaller across all three operating systems and uploads them after a
successful release.

### Entry point and icon scaffolding

Scaffolds a `main.py` entry point to build from and a default `icon.png`
rendered from your project name to brand it — both ready to replace with your
own.

### Bundled resources

Bundles your project's resources into the executable, so its data files ship
inside the binary.

### Downloads badge

Adds a badge showing the total download count of your release binaries.

### Run command

Adds a `pyrig-executables run` command that runs your project's entry point the
same way the built executable does, so you can try it locally before releasing.

## Usage

Add pyrig-executables as a development dependency and run `pyrig mkroot` to
scaffold everything. No tokens or secrets are required — the release workflow
uses GitHub's automatic token.

```bash
uv add --group dev pyrig-executables
uv run pyrig mkroot
```

## Documentation

Full documentation, including the auto-generated API reference, is available on
the [documentation site](https://Winipedia.github.io/pyrig-executables).
