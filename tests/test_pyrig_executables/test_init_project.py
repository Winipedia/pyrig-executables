"""Tests that pyrig init works correctly."""


def test_init_pyrig_project(init_pyrig_project: tuple[bool, str]) -> None:
    """Test function."""
    success, message = init_pyrig_project
    assert success, message
