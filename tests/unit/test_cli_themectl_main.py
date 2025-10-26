"""
Additional unit tests for qt_theme_manager.cli.themectl.main
to improve coverage of CLI command parsing and error handling.
"""

import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


@patch("sys.argv", ["qt-theme-manager", "--version"])
def test_version_command_exit_0() -> None:
    from qt_theme_manager.cli import themectl

    with pytest.raises(SystemExit) as exc:
        themectl.main()
    assert exc.value.code == 0


@patch("sys.argv", ["qt-theme-manager"])  # no command
def test_no_command_returns_none(capsys: "pytest.CaptureFixture[str]") -> None:
    from qt_theme_manager.cli import themectl

    result = themectl.main()
    # None indicates help printed by parser
    assert result is None
    captured = capsys.readouterr()
    assert "Usage" in captured.out or "usage" in captured.out


def test_list_command_calls_list() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "list"]):
        with patch.object(themectl, "ThemeCLI") as MockCLI:
            instance = MockCLI.return_value
            instance.list_themes.return_value = None
            rc = themectl.main()
            assert rc == 0
            instance.list_themes.assert_called_once()


def test_set_command_calls_set() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "set", "dark"]):
        with patch.object(themectl, "ThemeCLI") as MockCLI:
            instance = MockCLI.return_value
            instance.set_theme.return_value = None
            rc = themectl.main()
            assert rc == 0
            instance.set_theme.assert_called_once_with("dark")


def test_export_command_calls_export(tmp_path: Path) -> None:
    from qt_theme_manager.cli import themectl

    output = tmp_path / "theme.qss"
    with patch(
        "sys.argv",
        ["qt-theme-manager", "export", "dark", str(output)],
    ):
        with patch.object(themectl, "ThemeCLI") as MockCLI:
            instance = MockCLI.return_value
            instance.export_qss.return_value = None
            rc = themectl.main()
            assert rc == 0
            instance.export_qss.assert_called_once_with(
                "dark",
                str(output),
            )


def test_current_command_calls_show_current() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "current"]):
        with patch.object(themectl, "ThemeCLI") as MockCLI:
            instance = MockCLI.return_value
            instance.show_current.return_value = None
            rc = themectl.main()
            assert rc == 0
            instance.show_current.assert_called_once()


def test_verbose_sets_logging_level() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "--verbose", "list"]):
        with patch.object(logging, "getLogger") as getLogger:
            # Create a dummy logger object with setLevel
            logger_obj = MagicMock()
            getLogger.return_value = logger_obj
            with patch.object(themectl, "ThemeCLI") as MockCLI:
                instance = MockCLI.return_value
                instance.list_themes.return_value = None
                rc = themectl.main()
                assert rc == 0
                # Root logger level should be set to INFO
                logger_obj.setLevel.assert_called()


def test_init_import_error_returns_1() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "list"]):
        with patch.object(themectl, "ThemeCLI", side_effect=ImportError("x")):
            rc = themectl.main()
            assert rc == 1


def test_keyboard_interrupt_returns_1() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "list"]):
        with patch.object(themectl, "ThemeCLI") as MockCLI:
            instance = MockCLI.return_value
            instance.list_themes.side_effect = KeyboardInterrupt()
            rc = themectl.main()
            assert rc == 1


def test_command_system_exit_propagates() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "list"]):
        with patch.object(themectl, "ThemeCLI") as MockCLI:
            instance = MockCLI.return_value
            instance.list_themes.side_effect = SystemExit(2)
            with pytest.raises(SystemExit) as exc:
                themectl.main()
            assert exc.value.code == 2


def test_command_exception_returns_1() -> None:
    from qt_theme_manager.cli import themectl

    with patch("sys.argv", ["qt-theme-manager", "set", "dark"]):
        with patch.object(themectl, "ThemeCLI") as MockCLI:
            instance = MockCLI.return_value
            instance.set_theme.side_effect = RuntimeError("boom")
            rc = themectl.main()
            assert rc == 1
