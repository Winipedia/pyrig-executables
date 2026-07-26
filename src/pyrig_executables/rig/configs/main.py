"""Configuration for the project's `main` entry-point module.

Scaffolds a `main.py` containing a callable `main` function in every project
that installs this plugin. The module provides the entry point that the
executable builder bundles into a standalone binary, so this config guarantees
that a suitable build target always exists.
"""

from types import ModuleType

from pyrig.rig.configs.base.copy_module import CopyModuleConfigFile

from pyrig_executables import main as main_module
from pyrig_executables.main import main as main_func


class MainConfigFile(CopyModuleConfigFile):
    """Scaffolding for the project's `main.py` entry-point module.

    Copies this plugin's own entry-point module into the target project as
    `main.py`. Once the file exists, a project's own implementation stands
    rather than being overwritten, as long as it still satisfies the
    entry-point contract that `is_correct` checks for.
    """

    def copy_module(self) -> ModuleType:
        """Return the `pyrig_executables.main` module used as `main.py` scaffolding."""
        return main_module

    def is_correct(self) -> bool:
        """Return whether the project's `main.py` is valid.

        Overrides the inherited content check: `main.py` is correct once the
        target module exposes a callable `main` and contains a `__main__`
        execution guard, regardless of what the function body does. This lets
        a project's own entry-point implementation stand unmodified.

        Returns:
            `True` if the target module defines a callable `main` and the
            `__main__` guard is present.
        """
        return self.has_callable_main() and self.has_main_guard()

    def has_callable_main(self) -> bool:
        """Return whether the target module exposes a callable `main` attribute."""
        return callable(getattr(self.module(), main_func.__name__, None))

    def has_main_guard(self) -> bool:
        """Return whether the target module's file contains the `__main__` guard.

        Matched via plain substring search, so the guard text must appear
        exactly as returned by `main_guard`.

        Returns:
            `True` if the guard snippet is present in the file.
        """
        return self.main_guard() in self.read_content()

    def main_guard(self) -> str:
        """Return the canonical `__main__` execution guard snippet.

        Returns:
            The `if __name__ == "__main__"` block that calls `main`.
        """
        return f"""if __name__ == "__main__":
    {main_func.__name__}()"""
