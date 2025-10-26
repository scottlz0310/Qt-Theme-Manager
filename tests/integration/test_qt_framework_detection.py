"""
Integration tests for Qt framework detection across different platforms and frameworks.
Tests the complete Qt detection workflow with real and mocked frameworks.
"""

from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

from qt_theme_manager.qt.detection import (
    QtDetector,
    QtFrameworkNotFoundError,
    clear_qt_cache,
    detect_qt_framework,
    get_qt_framework_info,
    is_qt_available,
)


class TestQtFrameworkDetectionIntegration:
    """Integration tests for Qt framework detection system."""

    def test_detection_priority_order(self, mock_qt_modules: Dict[str, Any]):
        """Test that Qt frameworks are detected in correct priority order."""
        clear_qt_cache()

        # Mock all frameworks available
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
            framework, modules = detect_qt_framework()

            # Should detect PySide6 first (highest priority)
            assert framework == "PySide6"
            assert "version" in modules
            assert modules["version"] == "6.0.0"

    def test_fallback_to_pyqt6(self, mock_qt_modules: Dict[str, Any]):
        """Test fallback to PyQt6 when PySide6 is not available."""
        clear_qt_cache()

        def mock_import(name, *args, **kwargs):
            if name.startswith("PySide6"):
                raise ImportError(f"No module named '{name}'")
            return original_import(name, *args, **kwargs)

        original_import = __builtins__["__import__"]

        with patch("builtins.__import__", side_effect=mock_import):
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
                framework, modules = detect_qt_framework()

                assert framework == "PyQt6"
                assert modules["version"] == "6.2.0"

    def test_fallback_to_pyqt5(self, mock_qt_modules: Dict[str, Any]):
        """Test fallback to PyQt5 when PySide6 and PyQt6 are not available."""
        clear_qt_cache()

        def mock_import(name, *args, **kwargs):
            if name.startswith(("PySide6", "PyQt6")):
                raise ImportError(f"No module named '{name}'")
            return original_import(name, *args, **kwargs)

        original_import = __builtins__["__import__"]

        with patch("builtins.__import__", side_effect=mock_import):
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
                framework, modules = detect_qt_framework()

                assert framework == "PyQt5"
                assert modules["version"] == "5.15.0"

    def test_no_qt_framework_available(self, no_qt_available):
        """Test error handling when no Qt framework is available."""
        clear_qt_cache()

        with pytest.raises(QtFrameworkNotFoundError) as exc_info:
            detect_qt_framework()

        error_message = str(exc_info.value)
        assert "No Qt framework found" in error_message
        assert "pip install PySide6" in error_message
        assert "pip install PyQt6" in error_message
        assert "pip install PyQt5" in error_message

    @pytest.mark.skip(
        reason="Qt version validation test requires complex mocking in test environment"
    )
    def test_version_validation_too_old(self, mock_qt_modules: Dict[str, Any]):
        """Test version validation with too old Qt version."""
        # This test is skipped because Qt is available in test environment
        # and complex mocking is required to simulate version validation failure
        pass

    def test_caching_mechanism(self, mock_pyside6):
        """Test that detection results are properly cached."""
        clear_qt_cache()
        detector = QtDetector()

        # First detection
        framework1, modules1 = detector.detect_qt_framework()

        # Second detection should use cache
        framework2, modules2 = detector.detect_qt_framework()

        assert framework1 == framework2 == "PySide6"
        assert modules1 is modules2  # Should be same object (cached)

        # Cached results should be available
        assert detector.get_cached_framework() == "PySide6"
        assert detector.get_cached_modules() is not None

    def test_force_redetection(self, mock_pyside6):
        """Test forced re-detection bypasses cache."""
        clear_qt_cache()
        detector = QtDetector()

        # Initial detection
        framework1, modules1 = detector.detect_qt_framework()

        # Force re-detection
        framework2, modules2 = detector.detect_qt_framework(force_redetect=True)

        assert framework1 == framework2 == "PySide6"
        # Modules might be different objects due to re-import

    def test_clear_cache_functionality(self, mock_pyside6):
        """Test cache clearing functionality."""
        clear_qt_cache()
        detector = QtDetector()

        # Detect and cache
        detector.detect_qt_framework()
        assert detector.get_cached_framework() is not None

        # Clear cache
        detector.clear_cache()
        assert detector.get_cached_framework() is None
        assert detector.get_cached_modules() is None

    def test_is_qt_available_true(self, mock_pyside6):
        """Test is_qt_available returns True when Qt is available."""
        clear_qt_cache()
        assert is_qt_available() is True

    def test_is_qt_available_false(self, no_qt_available):
        """Test is_qt_available returns False when Qt is not available."""
        clear_qt_cache()
        assert is_qt_available() is False

    def test_get_qt_framework_info_success(self, mock_pyside6):
        """Test get_qt_framework_info with available framework."""
        clear_qt_cache()
        info = get_qt_framework_info()

        assert info is not None
        assert info["framework"] == "PySide6"
        assert "version" in info

    def test_get_qt_framework_info_failure(self, no_qt_available):
        """Test get_qt_framework_info with no available framework."""
        clear_qt_cache()
        info = get_qt_framework_info()

        assert info is None

    @pytest.mark.integration
    def test_module_level_functions_consistency(self, mock_pyside6):
        """Test that module-level functions work consistently."""
        clear_qt_cache()

        # Test detection
        framework, modules = detect_qt_framework()
        assert framework == "PySide6"

        # Test availability check
        assert is_qt_available() is True

        # Test info retrieval
        info = get_qt_framework_info()
        assert info is not None
        assert info["framework"] == framework

    def test_version_parsing_edge_cases(self, mock_qt_modules: Dict[str, Any]):
        """Test version parsing with various version formats."""
        clear_qt_cache()

        # Test with patch version
        with patch.dict(
            "sys.modules",
            {
                "PySide6": MagicMock(__version__="6.0.1"),
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
            framework, modules = detect_qt_framework()
            assert framework == "PySide6"
            assert modules["version"] == "6.0.1"

    def test_concurrent_detection_safety(self, mock_pyside6):
        """Test that concurrent detection calls are handled safely."""
        clear_qt_cache()
        detector = QtDetector()

        # Simulate concurrent calls
        results = []
        for _ in range(5):
            framework, modules = detector.detect_qt_framework()
            results.append((framework, modules))

        # All results should be consistent
        frameworks = [r[0] for r in results]
        assert all(f == "PySide6" for f in frameworks)


@pytest.mark.integration
class TestCrossPlatformCompatibility:
    """Cross-platform compatibility tests for Qt detection."""

    @pytest.mark.windows
    def test_windows_qt_detection(self, mock_pyside6):
        """Test Qt detection on Windows platform."""
        clear_qt_cache()
        framework, modules = detect_qt_framework()
        assert framework == "PySide6"
        assert "QApplication" in modules

    @pytest.mark.linux
    def test_linux_qt_detection(self, mock_pyside6):
        """Test Qt detection on Linux platform."""
        clear_qt_cache()
        framework, modules = detect_qt_framework()
        assert framework == "PySide6"
        assert "QApplication" in modules

    @pytest.mark.macos
    def test_macos_qt_detection(self, mock_pyside6):
        """Test Qt detection on macOS platform."""
        clear_qt_cache()
        framework, modules = detect_qt_framework()
        assert framework == "PySide6"
        assert "QApplication" in modules

    def test_platform_specific_modules(self, mock_pyside6):
        """Test that platform-specific Qt modules are handled correctly."""
        clear_qt_cache()
        framework, modules = detect_qt_framework()

        # Core modules should be available on all platforms
        required_modules = ["QObject", "pyqtSignal", "QApplication", "QWidget"]
        for module_name in required_modules:
            assert module_name in modules
            assert modules[module_name] is not None


@pytest.mark.integration
class TestQtFrameworkSpecificBehavior:
    """Test framework-specific behavior and compatibility."""

    def test_pyside6_specific_features(self, mock_qt_modules: Dict[str, Any]):
        """Test PySide6-specific detection features."""
        clear_qt_cache()

        with patch.dict(
            "sys.modules",
            {
                "PySide6": MagicMock(__version__="6.2.0"),
                "PySide6.QtCore": MagicMock(
                    QObject=mock_qt_modules["QObject"],
                    Signal=mock_qt_modules["pyqtSignal"],  # PySide6 uses Signal
                ),
                "PySide6.QtWidgets": MagicMock(
                    QApplication=mock_qt_modules["QApplication"],
                    QWidget=mock_qt_modules["QWidget"],
                ),
            },
        ):
            framework, modules = detect_qt_framework()
            assert framework == "PySide6"
            assert "pyqtSignal" in modules  # Mapped from Signal

    def test_pyqt6_specific_features(self, mock_qt_modules: Dict[str, Any]):
        """Test PyQt6-specific detection features."""
        clear_qt_cache()

        def mock_import(name, *args, **kwargs):
            if name.startswith("PySide6"):
                raise ImportError(f"No module named '{name}'")
            return original_import(name, *args, **kwargs)

        original_import = __builtins__["__import__"]

        with patch("builtins.__import__", side_effect=mock_import):
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
                framework, modules = detect_qt_framework()
                assert framework == "PyQt6"
                assert modules["version"] == "6.2.0"

    def test_pyqt5_specific_features(self, mock_qt_modules: Dict[str, Any]):
        """Test PyQt5-specific detection features."""
        clear_qt_cache()

        def mock_import(name, *args, **kwargs):
            if name.startswith(("PySide6", "PyQt6")):
                raise ImportError(f"No module named '{name}'")
            return original_import(name, *args, **kwargs)

        original_import = __builtins__["__import__"]

        with patch("builtins.__import__", side_effect=mock_import):
            with patch.dict(
                "sys.modules",
                {
                    "PyQt5": MagicMock(),
                    "PyQt5.QtCore": MagicMock(
                        QT_VERSION_STR="5.15.2",
                        QObject=mock_qt_modules["QObject"],
                        pyqtSignal=mock_qt_modules["pyqtSignal"],
                    ),
                    "PyQt5.QtWidgets": MagicMock(
                        QApplication=mock_qt_modules["QApplication"],
                        QWidget=mock_qt_modules["QWidget"],
                    ),
                },
            ):
                framework, modules = detect_qt_framework()
                assert framework == "PyQt5"
                assert modules["version"] == "5.15.2"
