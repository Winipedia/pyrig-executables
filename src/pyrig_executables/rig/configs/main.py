"""Configuration for the project's ``main`` entry-point module.

Scaffolds a ``main.py`` containing a callable ``main`` function in every
project that installs this plugin. The module provides the entry point that the
executable builder bundles into a standalone binary, so this config guarantees
that a suitable build target always exists.
"""

from types import ModuleType

from pyrig.rig.configs.base.copy_module import CopyModuleConfigFile

from pyrig_executables import main as main_module
from pyrig_executables.main import main as main_func


class MainConfigFile(CopyModuleConfigFile):
    """Manages the project's ``main.py`` entry-point module.

    Copies this plugin's :mod:`pyrig_executables.main` scaffolding into the
    target project (with the package prefix rewritten to the project's package
    name), producing a ``main.py`` with a ``main`` entry point. Once the file
    exists, validation only requires that a callable ``main`` is present, so any
    user-implemented entry point is preserved and never overwritten.
    """

    def copy_module(self) -> ModuleType:
        """Return the source module whose content is copied into the project.

        Returns:
            The :mod:`pyrig_executables.main` module used as the entry-point
            scaffolding.
        """
        return main_module

    def is_correct(self) -> bool:
        """Return whether the project's ``main.py`` is valid.

        Overrides the base :meth:`is_correct` to assert that ``main.py`` is only
        correct when the target module both exposes a callable named ``main``
        and contains an ``if __name__ == "__main__"`` execution guard. The
        function body is deliberately ignored so that a project's own
        entry-point implementation is treated as valid and is never overwritten.

        Returns:
            ``True`` if the target module defines a callable ``main`` and a
            ``__main__`` guard is present.
        """
        return self.has_callable_main() and self.has_main_guard()

    def has_callable_main(self) -> bool:
        """Return whether the target module exposes a callable ``main``.

        Returns:
            ``True`` if the module defines an attribute named ``main`` that is
            callable.
        """
        return callable(getattr(self.module(), main_func.__name__, None))

    def has_main_guard(self) -> bool:
        """Return whether the target module has a ``__main__`` execution guard.

        Checks that the file's content contains the :meth:`main_guard` snippet,
        the conventional guard that runs ``main`` when the module is executed
        directly.

        Returns:
            ``True`` if the ``__main__`` guard snippet is present in the file.
        """
        return self.main_guard() in self.read_content()

    def main_guard(self) -> str:
        """Return the canonical ``__main__`` execution guard snippet.

        Returns:
            The ``if __name__ == "__main__"`` block that calls ``main``, used to
            check for and scaffold the guard in the target module.
        """
        return f"""if __name__ == "__main__":
    {main_func.__name__}()"""
