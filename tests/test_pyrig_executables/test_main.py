"""Test module."""

from pyrig_executables import main as main_module
from pyrig_executables.main import main as main_func


def test_main() -> None:
    """Test function."""
    assert main_func() is None

    assert main_func.__doc__ == """Run the project."""
    assert main_module.__doc__ == """Project entry point."""
