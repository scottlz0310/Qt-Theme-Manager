"""
Unit tests for qt_theme_manager.cli.themectl.ThemeCLI methods
covering command behaviors and error handling to improve coverage.
"""

from pathlib import Path
from typing import Dict
from unittest.mock import MagicMock, patch

import pytest


def _make_themes() -> Dict[str, Dict[str, str]]:
    return {
        "light": {
            "display_name": "Light Theme",
            "description": "Light",
            "version": "1.0.0",
            "backgroundColor": "#ffffff",
            "textColor": "#000000",
            "primaryColor": "#111111",
            "secondaryColor": "#222222",
            "accentColor": "#333333",
            "borderColor": "#444444",
            "hoverColor": "#555555",
            "selectionColor": "#666666",
            "author": "A",
        },
        "dark": {
            "display_name": "Dark Theme",
            "description": "Dark",
            "version": "2.0.0",
        },
    }


def test_init_nonexistent_config_path_raises() -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    nonexistent = Path("/tmp/definitely_nonexistent_config.json")
    with pytest.raises(FileNotFoundError):
        ThemeCLI(str(nonexistent))


def _mock_cli_with_controller() -> MagicMock:
    # Patch ThemeController and ThemeLoader so __init__ succeeds
    # and provide a controller mock with desired behaviors.
    from qt_theme_manager.cli import themectl

    controller_mock = MagicMock()
    loader_mock = MagicMock()

    patcher_ctrl = patch.object(
        themectl, "ThemeController", return_value=controller_mock
    )
    patcher_load = patch.object(themectl, "ThemeLoader", return_value=loader_mock)
    patcher_ctrl.start()
    patcher_load.start()

    # Attach for teardown by caller
    controller_mock._patchers = (
        patcher_ctrl,
        patcher_load,
    )  # type: ignore[attr-defined]
    return controller_mock


def _stop_cli_patchers(controller_mock: MagicMock) -> None:
    patchers = controller_mock._patchers  # type: ignore[attr-defined]
    patcher_ctrl, patcher_load = patchers
    patcher_ctrl.stop()
    patcher_load.stop()


def test_list_themes_empty_prints_message(
    capsys: "pytest.CaptureFixture[str]",
) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {}
    controller.get_current_theme_name.return_value = ""

    cli = ThemeCLI()
    cli.list_themes()

    out = capsys.readouterr().out
    assert "No themes" in out

    _stop_cli_patchers(controller)


def test_list_themes_outputs_details(
    capsys: "pytest.CaptureFixture[str]",
) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    themes = _make_themes()
    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = themes
    controller.get_current_theme_name.return_value = "light"

    cli = ThemeCLI()
    cli.list_themes()

    out = capsys.readouterr().out
    assert "Available themes" in out
    assert "Light Theme" in out or "light" in out

    _stop_cli_patchers(controller)


def test_set_theme_input_validation_raises() -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    cli = ThemeCLI()

    with pytest.raises(SystemExit):
        cli.set_theme("")

    _stop_cli_patchers(controller)


def test_set_theme_not_found_raises() -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {"light": {}}

    cli = ThemeCLI()
    with pytest.raises(SystemExit):
        cli.set_theme("dark")

    _stop_cli_patchers(controller)


def test_set_theme_already_active(
    capsys: "pytest.CaptureFixture[str]",
) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {"light": {}}
    controller.get_current_theme_name.return_value = "light"

    cli = ThemeCLI()
    cli.set_theme("light")

    out = capsys.readouterr().out
    assert "already active" in out

    _stop_cli_patchers(controller)


def test_set_theme_success(capsys: "pytest.CaptureFixture[str]") -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {"dark": {}}
    controller.get_current_theme_name.return_value = "light"
    controller.set_theme.return_value = True

    cli = ThemeCLI()
    cli.set_theme("dark")

    out = capsys.readouterr().out
    assert "Theme set to" in out

    _stop_cli_patchers(controller)


def test_export_qss_validation_raises(tmp_path: Path) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    cli = ThemeCLI()

    with pytest.raises(SystemExit):
        cli.export_qss("", str(tmp_path / "a.qss"))
    with pytest.raises(SystemExit):
        cli.export_qss("dark", "")

    _stop_cli_patchers(controller)


def test_export_qss_success(
    tmp_path: Path,
    capsys: "pytest.CaptureFixture[str]",
) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {"dark": {}}
    controller.export_qss.return_value = True

    output = tmp_path / "out" / "file.qss"
    cli = ThemeCLI()
    cli.export_qss("dark", str(output))

    out = capsys.readouterr().out
    assert "QSS exported" in out

    _stop_cli_patchers(controller)


def test_export_qss_permission_error(tmp_path: Path) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {"dark": {}}

    output = tmp_path / "blocked" / "file.qss"

    def _raise_permission(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise PermissionError("denied")

    # Patch Path.mkdir globally for this test
    with patch.object(Path, "mkdir", side_effect=_raise_permission):
        cli = ThemeCLI()
        with pytest.raises(SystemExit):
            cli.export_qss("dark", str(output))

    _stop_cli_patchers(controller)


def test_show_current_no_current(
    capsys: "pytest.CaptureFixture[str]",
) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_current_theme_name.return_value = ""
    controller.get_available_themes.return_value = {}

    cli = ThemeCLI()
    cli.show_current()

    out = capsys.readouterr().out
    assert "No theme currently set" in out

    _stop_cli_patchers(controller)


def test_show_current_not_in_themes(
    capsys: "pytest.CaptureFixture[str]",
) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_current_theme_name.return_value = "dark"
    controller.get_available_themes.return_value = {"light": {}}

    cli = ThemeCLI()
    cli.show_current()

    out = capsys.readouterr().out
    assert "not found" in out or "Available themes" in out

    _stop_cli_patchers(controller)


def test_show_current_with_metadata(
    capsys: "pytest.CaptureFixture[str]",
) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    themes = _make_themes()
    controller = _mock_cli_with_controller()
    controller.get_current_theme_name.return_value = "light"
    controller.get_available_themes.return_value = themes

    cli = ThemeCLI()
    cli.show_current()

    out = capsys.readouterr().out
    assert "Current theme" in out
    assert "Color Palette" in out

    _stop_cli_patchers(controller)


def test_init_with_directory_path_raises(tmp_path: Path) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    dir_path = tmp_path / "confdir"
    dir_path.mkdir()
    with pytest.raises(ValueError):
        ThemeCLI(str(dir_path))


def test_init_import_error_is_propagated() -> None:
    from qt_theme_manager.cli import themectl

    with patch.object(themectl, "ThemeController", side_effect=ImportError("x")):
        with pytest.raises(ImportError):
            themectl.ThemeCLI()


def test_init_general_exception_is_propagated() -> None:
    from qt_theme_manager.cli import themectl

    with patch.object(themectl, "ThemeLoader", side_effect=RuntimeError("x")):
        with pytest.raises(RuntimeError):
            themectl.ThemeCLI()


def test_list_themes_exception_exits() -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.side_effect = RuntimeError("boom")

    cli = ThemeCLI()
    with pytest.raises(SystemExit):
        cli.list_themes()

    _stop_cli_patchers(controller)


def test_set_theme_no_themes_exits() -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {}

    cli = ThemeCLI()
    with pytest.raises(SystemExit):
        cli.set_theme("x")

    _stop_cli_patchers(controller)


def test_set_theme_failure_exits() -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {"x": {}}
    controller.get_current_theme_name.return_value = "y"
    controller.set_theme.return_value = False

    cli = ThemeCLI()
    with pytest.raises(SystemExit):
        cli.set_theme("x")

    _stop_cli_patchers(controller)


def test_set_theme_exception_exits() -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {"x": {}}
    controller.get_current_theme_name.return_value = "y"
    controller.set_theme.side_effect = RuntimeError("boom")

    cli = ThemeCLI()
    with pytest.raises(SystemExit):
        cli.set_theme("x")

    _stop_cli_patchers(controller)


def test_export_qss_no_themes_exits(tmp_path: Path) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {}

    cli = ThemeCLI()
    with pytest.raises(SystemExit):
        cli.export_qss("x", str(tmp_path / "a.qss"))

    _stop_cli_patchers(controller)


def test_export_qss_not_found_exits(tmp_path: Path) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {"y": {}}

    cli = ThemeCLI()
    with pytest.raises(SystemExit):
        cli.export_qss("x", str(tmp_path / "a.qss"))

    _stop_cli_patchers(controller)


def test_export_qss_failed_export_exits(tmp_path: Path) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_available_themes.return_value = {"x": {}}
    controller.export_qss.return_value = False

    cli = ThemeCLI()
    with pytest.raises(SystemExit):
        cli.export_qss("x", str(tmp_path / "a.qss"))

    _stop_cli_patchers(controller)


def test_show_current_no_themes_but_current_set(
    capsys: "pytest.CaptureFixture[str]",
) -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_current_theme_name.return_value = "light"
    controller.get_available_themes.return_value = {}

    cli = ThemeCLI()
    cli.show_current()
    out = capsys.readouterr().out
    assert "No themes available in configuration" in out

    _stop_cli_patchers(controller)


def test_show_current_exception_exits() -> None:
    from qt_theme_manager.cli.themectl import ThemeCLI

    controller = _mock_cli_with_controller()
    controller.get_current_theme_name.return_value = "light"
    controller.get_available_themes.side_effect = RuntimeError("boom")

    cli = ThemeCLI()
    with pytest.raises(SystemExit):
        cli.show_current()

    _stop_cli_patchers(controller)
