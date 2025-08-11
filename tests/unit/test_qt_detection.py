"""
Unit tests for Qt framework detection functionality.
Tests individual detection methods and error handling in isolation.
"""

import sys
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

from qt_theme_manager.qt.detection import (
    QtDetector,
    QtFrameworkNotFoundError,
    QtVersionError,
)


class TestQtDetector:
    """Unit tests for QtDetector class."""

    def test_init(self):
        """Test QtDetector initialization."""
        detector = QtDetector()

        assert detector._cached_framework is None
        assert detector._cached_modules is None
        assert detector._detection_attempted is False

    def test_min_versions_constants(self):
        """Test minimum version constants are defined correctly."""
        assert QtDetector.MIN_VERSIONS["PySide6"] == "6.0.0"
        assert QtDetector.MIN_VERSIONS["PyQt6"] == "6.2.0"
        assert QtDetector.MIN_VERSIONS["PyQt5"] == "5.15.0"

    def test_validate_version_valid(self):
        """Test version validation with valid versions."""
        detector = QtDetector()

        # These should not raise exceptions
        detector._validate_version("PySide6", "6.0.0", "6.0.0")  # Equal
        detector._validate_version("PySide6", "6.1.0", "6.0.0")  # Newer
        detector._validate_version("PyQt6", "6.2.1", "6.2.0")  # Patch version
        detector._validate_version(
            "PyQt5", "5.15.2", "5.15.0"
        )  # Patch version

    def test_validate_version_invalid(self):
        """Test version validation with invalid versions."""
        detector = QtDetector()

        with pytest.raises(QtVersionError) as exc_info:
            detector._validate_version("PySide6", "5.0.0", "6.0.0")

        error_msg = str(exc_info.value)
        assert "PySide6 version 5.0.0 is not supported" in error_msg
        assert "Minimum required version: 6.0.0" in error_msg

    def test_validate_version_malformed(self):
        """Test version validation with malformed version strings."""
        detector = QtDetector()

        # Should not raise exception for malformed versions (logged as warning)
        detector._validate_version("PySide6", "invalid.version", "6.0.0")
        detector._validate_version("PySide6", "", "6.0.0")
        detector._validate_version("PySide6", "6", "6.0.0")

    def test_cache_result(self):
        """Test caching of detection results."""
        detector = QtDetector()

        framework = "PySide6"
        modules = {"QObject": MagicMock(), "version": "6.0.0"}

        detector._cache_result(framework, modules)

        assert detector._cached_framework == framework
        assert detector._cached_modules == modules
        assert detector._detection_attempted is True

    def test_get_cached_framework(self):
        """Test getting cached framework name."""
        detector = QtDetector()

        # Initially None
        assert detector.get_cached_framework() is None

        # After caching
        detector._cached_framework = "PySide6"
        assert detector.get_cached_framework() == "PySide6"

    def test_get_cached_modules(self):
        """Test getting cached modules."""
        detector = QtDetector()

        # Initially None
        assert detector.get_cached_modules() is None

        # After caching
        modules = {"QObject": MagicMock()}
        detector._cached_modules = modules
        assert detector.get_cached_modules() == modules

    def test_clear_cache(self):
        """Test cache clearing."""
        detector = QtDetector()

        # Set cache
        detector._cached_framework = "PySide6"
        detector._cached_modules = {"test": "data"}
        detector._detection_attempted = True

        # Clear cache
        detector.clear_cache()

        assert detector._cached_framework is None
        assert detector._cached_modules is None
        assert detector._detection_attempted is False

    def test_try_pyside6_success(self, mock_qt_modules: Dict[str, Any]):
        """Test successful PySide6 detection."""
        detector = QtDetector()

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
            framework, modules = detector._try_pyside6()

            assert framework == "PySide6"
            assert modules["version"] == "6.0.0"
            assert "QObject" in modules
            assert "pyqtSignal" in modules
            assert "QApplication" in modules
            assert "QWidget" in modules

    def test_try_pyside6_import_error(self):
        """Test PySide6 detection with import error."""
        detector = QtDetector()

        def mock_import(name, *args, **kwargs):
            if name.startswith("PySide6"):
                raise ImportError(f"No module named '{name}'")
            return original_import(name, *args, **kwargs)

        original_import = __builtins__["__import__"]

        with patch("builtins.__import__", side_effect=mock_import):
            with pytest.raises(ImportError) as exc_info:
                detector._try_pyside6()

            assert "PySide6 not available" in str(exc_info.value)

    def test_try_pyqt6_success(self, mock_qt_modules: Dict[str, Any]):
        """Test successful PyQt6 detection."""
        detector = QtDetector()

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
            framework, modules = detector._try_pyqt6()

            assert framework == "PyQt6"
            assert modules["version"] == "6.2.0"
            assert "QObject" in modules
            assert "pyqtSignal" in modules

    def test_try_pyqt5_success(self, mock_qt_modules: Dict[str, Any]):
        """Test successful PyQt5 detection."""
        detector = QtDetector()

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
            framework, modules = detector._try_pyqt5()

            assert framework == "PyQt5"
            assert modules["version"] == "5.15.0"

    def test_is_qt_available_true(self, mock_pyside6):
        """Test is_qt_available returns True when Qt is available."""
        detector = QtDetector()
        assert detector.is_qt_available() is True

    def test_is_qt_available_false(self, no_qt_available):
        """Test is_qt_available returns False when Qt is not available."""
        detector = QtDetector()
        assert detector.is_qt_available() is False

    def test_detect_qt_framework_with_cache(self, mock_pyside6):
        """Test detection uses cache when available."""
        detector = QtDetector()

        # First detection
        framework1, modules1 = detector.detect_qt_framework()

        # Second detection should use cache
        framework2, modules2 = detector.detect_qt_framework()

        assert framework1 == framework2
        assert modules1 is modules2  # Same object reference (cached)

    def test_detect_qt_framework_force_redetect(self, mock_pyside6):
        """Test forced re-detection bypasses cache."""
        detector = QtDetector()

        # Initial detection
        framework1, modules1 = detector.detect_qt_framework()

        # Force re-detection
        framework2, modules2 = detector.detect_qt_framework(
            force_redetect=True
        )

        assert framework1 == framework2
        # Note: modules might be different objects due to re-import


class TestQtFrameworkNotFoundError:
    """Unit tests for QtFrameworkNotFoundError exception."""

    def test_default_message(self):
        """Test default error message."""
        error = QtFrameworkNotFoundError()
        message = str(error)

        assert "No Qt framework found" in message
        assert "pip install PySide6" in message
        assert "pip install PyQt6" in message
        assert "pip install PyQt5" in message

    def test_custom_message(self):
        """Test custom error message."""
        custom_message = "Custom Qt error message"
        error = QtFrameworkNotFoundError(custom_message)

        assert str(error) == custom_message

    def test_inheritance(self):
        """Test that error inherits from ImportError."""
        error = QtFrameworkNotFoundError()
        assert isinstance(error, ImportError)


class TestQtVersionError:
    """Unit tests for QtVersionError exception."""

    def test_error_message_format(self):
        """Test error message formatting."""
        error = QtVersionError("PySide6", "5.0.0", "6.0.0")
        message = str(error)

        assert "PySide6 version 5.0.0 is not supported" in message
        assert "Minimum required version: 6.0.0" in message

    def test_inheritance(self):
        """Test that error inherits from ImportError."""
        error = QtVersionError("PyQt6", "6.0.0", "6.2.0")
        assert isinstance(error, ImportError)

    def test_different_frameworks(self):
        """Test error message with different frameworks."""
        frameworks = [
            ("PySide6", "5.0.0", "6.0.0"),
            ("PyQt6", "6.0.0", "6.2.0"),
            ("PyQt5", "5.10.0", "5.15.0"),
        ]

        for framework, current, required in frameworks:
            error = QtVersionError(framework, current, required)
            message = str(error)

            assert framework in message
            assert current in message
            assert required in message


class TestModuleLevelFunctions:
    """Unit tests for module-level convenience functions."""

    @patch("qt_theme_manager.qt.detection._qt_detector")
    def test_detect_qt_framework_delegates(self, mock_detector):
        """Test that module-level detect_qt_framework delegates to detector."""
        from qt_theme_manager.qt.detection import detect_qt_framework

        expected_result = ("PySide6", {"version": "6.0.0"})
        mock_detector.detect_qt_framework.return_value = expected_result

        result = detect_qt_framework(force_redetect=True)

        assert result == expected_result
        mock_detector.detect_qt_framework.assert_called_once_with(True)

    @patch("qt_theme_manager.qt.detection._qt_detector")
    def test_is_qt_available_delegates(self, mock_detector):
        """Test that module-level is_qt_available delegates to detector."""
        from qt_theme_manager.qt.detection import is_qt_available

        mock_detector.is_qt_available.return_value = True

        result = is_qt_available()

        assert result is True
        mock_detector.is_qt_available.assert_called_once()

    @patch("qt_theme_manager.qt.detection._qt_detector")
    def test_get_qt_framework_info_success(self, mock_detector):
        """Test get_qt_framework_info with successful detection."""
        from qt_theme_manager.qt.detection import get_qt_framework_info

        mock_detector.detect_qt_framework.return_value = (
            "PySide6",
            {"version": "6.0.0", "QObject": MagicMock()},
        )

        info = get_qt_framework_info()

        assert info is not None
        assert info["framework"] == "PySide6"
        assert info["version"] == "6.0.0"

    @patch("qt_theme_manager.qt.detection._qt_detector")
    def test_get_qt_framework_info_failure(self, mock_detector):
        """Test get_qt_framework_info with detection failure."""
        from qt_theme_manager.qt.detection import get_qt_framework_info

        mock_detector.detect_qt_framework.side_effect = (
            QtFrameworkNotFoundError()
        )

        info = get_qt_framework_info()

        assert info is None

    @patch("qt_theme_manager.qt.detection._qt_detector")
    def test_clear_qt_cache_delegates(self, mock_detector):
        """Test that module-level clear_qt_cache delegates to detector."""
        from qt_theme_manager.qt.detection import clear_qt_cache

        clear_qt_cache()

        mock_detector.clear_cache.assert_called_once()


class TestVersionComparison:
    """Unit tests for version comparison logic."""

    def test_version_parsing_standard(self):
        """Test standard version parsing (major.minor.patch)."""
        detector = QtDetector()

        # Should not raise for valid versions
        detector._validate_version("Test", "6.0.0", "6.0.0")
        detector._validate_version("Test", "6.1.0", "6.0.0")
        detector._validate_version("Test", "6.0.1", "6.0.0")

    def test_version_parsing_different_lengths(self):
        """Test version parsing with different length version strings."""
        detector = QtDetector()

        # Should handle different version string lengths
        detector._validate_version("Test", "6.0", "6.0.0")
        detector._validate_version("Test", "6.0.0", "6.0")
        detector._validate_version("Test", "6", "6.0.0")

    def test_version_comparison_edge_cases(self):
        """Test version comparison edge cases."""
        detector = QtDetector()

        # Test various comparison scenarios
        test_cases = [
            ("6.0.0", "6.0.0", False),  # Equal - should not raise
            ("6.0.1", "6.0.0", False),  # Newer patch - should not raise
            ("6.1.0", "6.0.0", False),  # Newer minor - should not raise
            ("7.0.0", "6.0.0", False),  # Newer major - should not raise
            ("5.9.9", "6.0.0", True),  # Older major - should raise
            ("6.0.0", "6.0.1", True),  # Older patch - should raise
            ("6.0.0", "6.1.0", True),  # Older minor - should raise
        ]

        for current, required, should_raise in test_cases:
            if should_raise:
                with pytest.raises(QtVersionError):
                    detector._validate_version("Test", current, required)
            else:
                # Should not raise
                detector._validate_version("Test", current, required)
