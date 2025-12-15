"""
Pytest configuration and shared fixtures for qt_theme_manager tests.
"""

import importlib
import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def qt_theme_manager_path(project_root: Path) -> Path:
    """Get the qt_theme_manager package path."""
    return project_root / "qt_theme_manager"


@pytest.fixture
def mock_qt_modules() -> dict[str, Any]:
    """Create mock Qt modules for testing without Qt dependencies."""
    mock_qobject = MagicMock()
    mock_qobject.__name__ = "QObject"

    mock_qapplication = MagicMock()
    mock_qapplication.__name__ = "QApplication"

    mock_qwidget = MagicMock()
    mock_qwidget.__name__ = "QWidget"

    mock_signal = MagicMock()
    mock_signal.__name__ = "pyqtSignal"

    return {
        "QObject": mock_qobject,
        "pyqtSignal": mock_signal,
        "QApplication": mock_qapplication,
        "QWidget": mock_qwidget,
        "version": "6.0.0",
    }


@pytest.fixture
def mock_pyside6(
    mock_qt_modules: dict[str, Any],
) -> Generator[None, None, None]:
    """Mock PySide6 modules for testing."""
    with patch.dict(
        "sys.modules",
        {
            "PySide6": MagicMock(__version__="6.0.0"),
            "PySide6.QtCore": MagicMock(
                QObject=mock_qt_modules["QObject"],
                Signal=mock_qt_modules["pyqtSignal"],
            ),
            "PySide6.QtWidgets": MagicMock(
                QApplication=mock_qt_modules["QApplication"],
                QWidget=mock_qt_modules["QWidget"],
            ),
        },
    ):
        yield


@pytest.fixture
def mock_pyqt6(mock_qt_modules: dict[str, Any]) -> Generator[None, None, None]:
    """Mock PyQt6 modules for testing."""
    with patch.dict(
        "sys.modules",
        {
            "PyQt6": MagicMock(),
            "PyQt6.QtCore": MagicMock(
                QT_VERSION_STR="6.2.0",
                QObject=mock_qt_modules["QObject"],
                pyqtSignal=mock_qt_modules["pyqtSignal"],
            ),
            "PyQt6.QtWidgets": MagicMock(
                QApplication=mock_qt_modules["QApplication"],
                QWidget=mock_qt_modules["QWidget"],
            ),
        },
    ):
        yield


@pytest.fixture
def mock_pyqt5(mock_qt_modules: dict[str, Any]) -> Generator[None, None, None]:
    """Mock PyQt5 modules for testing."""
    with patch.dict(
        "sys.modules",
        {
            "PyQt5": MagicMock(),
            "PyQt5.QtCore": MagicMock(
                QT_VERSION_STR="5.15.0",
                QObject=mock_qt_modules["QObject"],
                pyqtSignal=mock_qt_modules["pyqtSignal"],
            ),
            "PyQt5.QtWidgets": MagicMock(
                QApplication=mock_qt_modules["QApplication"],
                QWidget=mock_qt_modules["QWidget"],
            ),
        },
    ):
        yield


@pytest.fixture
def no_qt_available() -> Generator[None, None, None]:
    """Mock environment with no Qt frameworks available."""
    modules_to_remove = [
        "PySide6",
        "PySide6.QtCore",
        "PySide6.QtWidgets",
        "PyQt6",
        "PyQt6.QtCore",
        "PyQt6.QtWidgets",
        "PyQt5",
        "PyQt5.QtCore",
        "PyQt5.QtWidgets",
    ]

    # Store original modules
    original_modules = {}
    for module in modules_to_remove:
        if module in sys.modules:
            original_modules[module] = sys.modules[module]
            del sys.modules[module]

    def mock_import_module(name: str, *args: Any, **kwargs: Any) -> Any:
        if name.startswith(("PySide6", "PyQt6", "PyQt5")):
            raise ImportError(f"No module named '{name}'")
        return original_import_module(name, *args, **kwargs)

    original_import_module = importlib.import_module

    # Patch the import mechanism used by qt_theme_manager.qt.detection (importlib.import_module).
    with patch("importlib.import_module", side_effect=mock_import_module):
        yield

    # Restore original modules
    for module, original in original_modules.items():
        sys.modules[module] = original


@pytest.fixture
def temp_config_dir(tmp_path: Path) -> Path:
    """Create a temporary configuration directory."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def sample_theme_config() -> dict[str, Any]:
    """Sample theme configuration for testing."""
    return {
        "name": "test_theme",
        "version": "1.0.0",
        "colors": {
            "primary": "#3498db",
            "secondary": "#2ecc71",
            "background": "#ecf0f1",
            "text": "#2c3e50",
        },
        "fonts": {
            "default": "Arial, sans-serif",
            "monospace": "Consolas, monospace",
        },
        "styles": {
            "button": "QPushButton { background-color: {primary}; }",
            "label": "QLabel { color: {text}; }",
        },
        "metadata": {
            "author": "Test Author",
            "description": "Test theme for unit testing",
        },
    }


@pytest.fixture(autouse=True)
def clear_qt_cache():
    """Clear Qt detection cache before each test."""
    # Import here to avoid circular imports
    from qt_theme_manager.qt.detection import clear_qt_cache

    clear_qt_cache()
    yield
    clear_qt_cache()


@pytest.fixture
def mock_logger():
    """Mock logger for testing log output."""
    with patch("qt_theme_manager.config.logging_config.get_logger") as mock:
        logger_mock = MagicMock()
        mock.return_value = logger_mock
        yield logger_mock


# Platform detection fixtures
@pytest.fixture
def is_windows() -> bool:
    """Check if running on Windows."""
    return sys.platform.startswith("win")


@pytest.fixture
def is_linux() -> bool:
    """Check if running on Linux."""
    return sys.platform.startswith("linux")


@pytest.fixture
def is_macos() -> bool:
    """Check if running on macOS."""
    return sys.platform == "darwin"


# Skip markers for platform-specific tests
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "windows: mark test to run only on Windows")
    config.addinivalue_line("markers", "linux: mark test to run only on Linux")
    config.addinivalue_line("markers", "macos: mark test to run only on macOS")
    config.addinivalue_line(
        "markers", "qt_required: mark test as requiring Qt framework"
    )
    config.addinivalue_line("markers", "integration: mark test as integration test")


def pytest_runtest_setup(item):
    """Setup for individual test runs."""
    # Skip platform-specific tests
    if item.get_closest_marker("windows") and not sys.platform.startswith("win"):
        pytest.skip("Windows-only test")
    if item.get_closest_marker("linux") and not sys.platform.startswith("linux"):
        pytest.skip("Linux-only test")
    if item.get_closest_marker("macos") and sys.platform != "darwin":
        pytest.skip("macOS-only test")
