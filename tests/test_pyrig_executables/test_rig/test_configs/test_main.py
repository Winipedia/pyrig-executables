"""Test module."""

from pyrig_executables import main as main_module
from pyrig_executables.rig.configs.main import MainConfigFile


class TestMainConfigFile:
    """Test class."""

    def test_copy_module(self) -> None:
        """Test method."""
        assert MainConfigFile.I.copy_module() is main_module

    def test_is_correct(self) -> None:
        """Test method."""
        assert MainConfigFile.I.is_correct()

    def test_has_callable_main(self) -> None:
        """Test method."""
        assert MainConfigFile.I.has_callable_main()

    def test_has_main_guard(self) -> None:
        """Test method."""
        assert MainConfigFile.I.has_main_guard()

    def test_main_guard(self) -> None:
        """Test method."""
        assert (
            MainConfigFile.I.main_guard()
            == """if __name__ == "__main__":
    main()"""
        )
