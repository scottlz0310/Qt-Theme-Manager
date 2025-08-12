"""
Test module for Qt framework detection system.
"""

import unittest
from unittest.mock import MagicMock, patch

from .detection import (
    QtDetector,
    QtFrameworkNotFoundError,
    QtVersionError,
    clear_qt_cache,
    detect_qt_framework,
    get_qt_framework_info,
    is_qt_available,
)


class TestQtDetection(unittest.TestCase):
    """Test cases for Qt framework detection."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.detector = QtDetector()
        # Clear any cached results
        self.detector.clear_cache()

    def tearDown(self) -> None:
        """Clean up after tests."""
        clear_qt_cache()

    def test_pyside6_detection(self) -> None:
        """Test PySide6 detection."""
        with patch.dict(
            "sys.modules",
            {
                "PySide6": MagicMock(__version__="6.2.0"),
                "PySide6.QtCore": MagicMock(),
                "PySide6.QtWidgets": MagicMock(),
            },
        ):
            # Mock the imports
            mock_qobject = MagicMock()
            mock_signal = MagicMock()
            mock_qapp = MagicMock()
            mock_qwidget = MagicMock()

            with patch(
                "qt_theme_manager.qt.detection.QtDetector._try_pyside6"
            ) as mock_try:
                mock_try.return_value = (
                    "PySide6",
                    {
                        "QObject": mock_qobject,
                        "pyqtSignal": mock_signal,
                        "QApplication": mock_qapp,
                        "QWidget": mock_qwidget,
                        "version": "6.2.0",
                    },
                )

                framework, modules = self.detector.detect_qt_framework()

                self.assertEqual(framework, "PySide6")
                self.assertEqual(modules["version"], "6.2.0")
                self.assertIn("QObject", modules)
                self.assertIn("pyqtSignal", modules)

    def test_pyqt6_detection(self) -> None:
        """Test PyQt6 detection when PySide6 is not available."""
        with patch(
            "qt_theme_manager.qt.detection.QtDetector._try_pyside6"
        ) as mock_pyside6:
            mock_pyside6.side_effect = ImportError("PySide6 not available")

            with patch(
                "qt_theme_manager.qt.detection.QtDetector._try_pyqt6"
            ) as mock_pyqt6:
                mock_pyqt6.return_value = (
                    "PyQt6",
                    {
                        "QObject": MagicMock(),
                        "pyqtSignal": MagicMock(),
                        "QApplication": MagicMock(),
                        "QWidget": MagicMock(),
                        "version": "6.2.0",
                    },
                )

                framework, modules = self.detector.detect_qt_framework()

                self.assertEqual(framework, "PyQt6")
                self.assertEqual(modules["version"], "6.2.0")

    def test_pyqt5_detection(self) -> None:
        """Test PyQt5 detection when PySide6 and PyQt6 are not available."""
        with patch(
            "qt_theme_manager.qt.detection.QtDetector._try_pyside6"
        ) as mock_pyside6:
            mock_pyside6.side_effect = ImportError("PySide6 not available")

            with patch(
                "qt_theme_manager.qt.detection.QtDetector._try_pyqt6"
            ) as mock_pyqt6:
                mock_pyqt6.side_effect = ImportError("PyQt6 not available")

                with patch(
                    "qt_theme_manager.qt.detection.QtDetector._try_pyqt5"
                ) as mock_pyqt5:
                    mock_pyqt5.return_value = (
                        "PyQt5",
                        {
                            "QObject": MagicMock(),
                            "pyqtSignal": MagicMock(),
                            "QApplication": MagicMock(),
                            "QWidget": MagicMock(),
                            "version": "5.15.0",
                        },
                    )

                    framework, modules = self.detector.detect_qt_framework()

                    self.assertEqual(framework, "PyQt5")
                    self.assertEqual(modules["version"], "5.15.0")

    def test_no_qt_framework_found(self) -> None:
        """Test exception when no Qt framework is available."""
        with patch(
            "qt_theme_manager.qt.detection.QtDetector._try_pyside6"
        ) as mock_pyside6:
            mock_pyside6.side_effect = ImportError("PySide6 not available")

            with patch(
                "qt_theme_manager.qt.detection.QtDetector._try_pyqt6"
            ) as mock_pyqt6:
                mock_pyqt6.side_effect = ImportError("PyQt6 not available")

                with patch(
                    "qt_theme_manager.qt.detection.QtDetector._try_pyqt5"
                ) as mock_pyqt5:
                    mock_pyqt5.side_effect = ImportError("PyQt5 not available")

                    with self.assertRaises(
                        QtFrameworkNotFoundError
                    ) as context:
                        self.detector.detect_qt_framework()

                    self.assertIn(
                        "No Qt framework found", str(context.exception)
                    )
                    self.assertIn(
                        "pip install PySide6", str(context.exception)
                    )

    def test_version_validation(self) -> None:
        """Test Qt framework version validation."""
        # Test valid version
        self.detector._validate_version("PySide6", "6.2.0", "6.0.0")

        # Test invalid version
        with self.assertRaises(QtVersionError) as context:
            self.detector._validate_version("PySide6", "5.15.0", "6.0.0")

        self.assertIn(
            "version 5.15.0 is not supported", str(context.exception)
        )
        self.assertIn(
            "Minimum required version: 6.0.0", str(context.exception)
        )

    def test_version_parsing(self) -> None:
        """Test version string parsing."""
        # Test normal version parsing
        self.detector._validate_version("PyQt6", "6.2.1", "6.2.0")

        # Test version with different lengths
        self.detector._validate_version("PyQt5", "5.15", "5.15.0")

        # Test invalid version format (should not raise exception)
        try:
            self.detector._validate_version("PySide6", "invalid", "6.0.0")
        except QtVersionError:
            self.fail(
                "Version validation should not fail for unparseable versions"
            )

    def test_caching(self) -> None:
        """Test detection result caching."""
        with patch(
            "qt_theme_manager.qt.detection.QtDetector._try_pyside6"
        ) as mock_try:
            mock_result = (
                "PySide6",
                {
                    "QObject": MagicMock(),
                    "pyqtSignal": MagicMock(),
                    "QApplication": MagicMock(),
                    "QWidget": MagicMock(),
                    "version": "6.2.0",
                },
            )
            mock_try.return_value = mock_result

            # First call should trigger detection
            framework1, modules1 = self.detector.detect_qt_framework()

            # Second call should use cache
            framework2, modules2 = self.detector.detect_qt_framework()

            # Should only be called once due to caching
            self.assertEqual(mock_try.call_count, 1)
            self.assertEqual(framework1, framework2)
            self.assertEqual(modules1, modules2)

    def test_force_redetect(self) -> None:
        """Test forcing re-detection bypasses cache."""
        with patch(
            "qt_theme_manager.qt.detection.QtDetector._try_pyside6"
        ) as mock_try:
            mock_result = (
                "PySide6",
                {
                    "QObject": MagicMock(),
                    "pyqtSignal": MagicMock(),
                    "QApplication": MagicMock(),
                    "QWidget": MagicMock(),
                    "version": "6.2.0",
                },
            )
            mock_try.return_value = mock_result

            # First call
            self.detector.detect_qt_framework()

            # Force re-detection
            self.detector.detect_qt_framework(force_redetect=True)

            # Should be called twice
            self.assertEqual(mock_try.call_count, 2)

    def test_is_qt_available(self) -> None:
        """Test is_qt_available function."""
        # Create a fresh detector for this test
        detector = QtDetector()

        with patch(
            "qt_theme_manager.qt.detection.QtDetector._try_pyside6"
        ) as mock_try:
            mock_try.return_value = ("PySide6", {"version": "6.2.0"})

            self.assertTrue(detector.is_qt_available())

        # Create another fresh detector for the negative test
        detector2 = QtDetector()

        with patch(
            "qt_theme_manager.qt.detection.QtDetector._try_pyside6"
        ) as mock_pyside6:
            mock_pyside6.side_effect = ImportError("Not available")

            with patch(
                "qt_theme_manager.qt.detection.QtDetector._try_pyqt6"
            ) as mock_pyqt6:
                mock_pyqt6.side_effect = ImportError("Not available")

                with patch(
                    "qt_theme_manager.qt.detection.QtDetector._try_pyqt5"
                ) as mock_pyqt5:
                    mock_pyqt5.side_effect = ImportError("Not available")

                    self.assertFalse(detector2.is_qt_available())

    def test_module_level_functions(self) -> None:
        """Test module-level convenience functions."""
        with patch(
            "qt_theme_manager.qt.detection._qt_detector"
        ) as mock_detector:
            mock_detector.detect_qt_framework.return_value = (
                "PySide6",
                {"version": "6.2.0"},
            )
            mock_detector.is_qt_available.return_value = True

            # Test detect_qt_framework
            framework, modules = detect_qt_framework()
            self.assertEqual(framework, "PySide6")

            # Test is_qt_available
            self.assertTrue(is_qt_available())

            # Test get_qt_framework_info
            info = get_qt_framework_info()
            if info is not None:
                self.assertEqual(info["framework"], "PySide6")
                self.assertEqual(info["version"], "6.2.0")

    def test_clear_cache(self) -> None:
        """Test cache clearing functionality."""
        with patch(
            "qt_theme_manager.qt.detection.QtDetector._try_pyside6"
        ) as mock_try:
            mock_try.return_value = ("PySide6", {"version": "6.2.0"})

            # Populate cache
            self.detector.detect_qt_framework()
            self.assertIsNotNone(self.detector.get_cached_framework())

            # Clear cache
            self.detector.clear_cache()
            self.assertIsNone(self.detector.get_cached_framework())
            self.assertIsNone(self.detector.get_cached_modules())


if __name__ == "__main__":
    unittest.main()
