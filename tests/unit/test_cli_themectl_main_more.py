"""
Additional coverage for qt_theme_manager.cli.themectl main() branches.
"""

from unittest.mock import patch
import pytest


def test_no_command_prints_help_returns_none() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager"]):
        # Spy on print_help via parser by patching print_help
        with patch(
            "argparse.ArgumentParser.print_help"
        ) as mock_help:
            result = themectl.main()
            assert result is None
            mock_help.assert_called()


def test_version_command_prints_and_exits_zero() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "version"]):
        rc = themectl.main()
        assert rc == 0


def test_cli_init_config_error_returns_1() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "-c", "bad.json", "list"]):
        with patch.object(
            themectl, "ThemeCLI", side_effect=FileNotFoundError("x")
        ):
            rc = themectl.main()
            assert rc == 1


def test_command_unknown_returns_1() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "unknown"]):
        with patch("argparse.ArgumentParser.print_help") as mock_help:
            with pytest.raises(SystemExit) as exc:
                themectl.main()
            assert exc.value.code == 2
            mock_help.assert_not_called()


def test_command_keyboard_interrupt_returns_1() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "list"]):
        with patch.object(themectl, "ThemeCLI") as MockCLI:
            inst = MockCLI.return_value
            inst.list_themes.side_effect = KeyboardInterrupt()
            rc = themectl.main()
            assert rc == 1


def test_command_exception_returns_1() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "set", "dark"]):
        with patch.object(themectl, "ThemeCLI") as MockCLI:
            inst = MockCLI.return_value
            inst.set_theme.side_effect = RuntimeError("boom")
            rc = themectl.main()
            assert rc == 1


