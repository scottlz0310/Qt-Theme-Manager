"""
Extra tests for qt_theme_manager.cli.main to cover exception branches.
"""

from unittest.mock import patch


def test_cli_main_keyboard_interrupt() -> None:
    from qt_theme_manager.cli.main import main as cli_main

    with patch(
        "qt_theme_manager.cli.main.themectl_main",
        side_effect=KeyboardInterrupt(),
    ):
        rc = cli_main()
        assert rc == 1


def test_cli_main_import_error() -> None:
    from qt_theme_manager.cli.main import main as cli_main

    with patch(
        "qt_theme_manager.cli.main.themectl_main",
        side_effect=ImportError("x"),
    ):
        rc = cli_main()
        assert rc == 1


def test_cli_main_file_not_found_error() -> None:
    from qt_theme_manager.cli.main import main as cli_main

    with patch(
        "qt_theme_manager.cli.main.themectl_main",
        side_effect=FileNotFoundError("missing"),
    ):
        rc = cli_main()
        assert rc == 1


def test_cli_main_permission_error() -> None:
    from qt_theme_manager.cli.main import main as cli_main

    with patch(
        "qt_theme_manager.cli.main.themectl_main",
        side_effect=PermissionError("denied"),
    ):
        rc = cli_main()
        assert rc == 1


def test_cli_main_unexpected_error() -> None:
    from qt_theme_manager.cli.main import main as cli_main

    with patch(
        "qt_theme_manager.cli.main.themectl_main",
        side_effect=RuntimeError("boom"),
    ):
        rc = cli_main()
        assert rc == 1
