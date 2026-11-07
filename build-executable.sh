#!/usr/bin/env bash
set -euo pipefail

uv \
  run \
  pyinstaller \
  --onefile \
  --name=pyrig-executables-"${OSTYPE}" \
  --icon=src/pyrig_executables/rig/resources/icon.png \
  --collect-data=pyrig_executables.rig.resources \
  src/pyrig_executables/main.py
