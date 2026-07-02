# pyrig-executables

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

pyrig-executables is a [pyrig](https://github.com/Winipedia/pyrig) plugin that
turns your project into standalone executables and attaches one per operating
system to every GitHub release — so anyone can run it without installing Python.

## What it adds

- **Standalone executables** — a single-file binary of your project for Linux,
  Windows, and macOS, built with PyInstaller.
- **Release integration** — a matrix build job that compiles and attaches a
  binary per OS to each release.
- **Entry point and icon** — a `main.py` and a default icon, both scaffolded and
  ready to replace with your own.
- **Bundled resources** — your project's resources are bundled into the binary.
- **Run command** — `pyrig-executables run` runs your entry point the same way
  the built binary does, so you can try it locally.
- **Downloads badge** — a badge showing the total downloads of your binaries.

## Usage

```bash
uv add pyrig-executables --dev
uv run pyrig sync
```

No tokens or secrets are required — the release workflow uses GitHub's automatic
token.

## Documentation

Full documentation, including the auto-generated API reference, is available on
the [documentation site](https://Winipedia.github.io/pyrig-executables).
