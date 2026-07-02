"""Pyrig plugin that builds and publishes standalone project executables.

Installing this package as a dependency extends a pyrig-built project with an
entry-point and icon to build from, a PyInstaller-based executable builder, a
release workflow job that compiles and attaches one binary per operating
system to each GitHub release, and a CLI command to run the entry point
locally the same way the built executable does.
"""
