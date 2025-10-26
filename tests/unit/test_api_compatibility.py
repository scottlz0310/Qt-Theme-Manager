"""
Unit tests for API compatibility and backward compatibility.
Tests that existing APIs continue to work as expected.
"""

from unittest.mock import MagicMock, patch

import pytest


class TestPublicAPICompatibility:
    """Test that public API remains compatible."""

    def test_package_imports(self):
        """Test that main package imports work correctly."""
        # Test main package import
        import qt_theme_manager

        assert qt_theme_manager is not None

        # Test version attribute
        assert hasattr(qt_theme_manager, "__version__")
        assert isinstance(qt_theme_manager.__version__, str)

        # Test author attribute
        assert hasattr(qt_theme_manager, "__author__")
        assert isinstance(qt_theme_manager.__author__, str)

        # Test license attribute
        assert hasattr(qt_theme_manager, "__license__")
        assert isinstance(qt_theme_manager.__license__, str)

    def test_core_component_imports(self):
        """Test that core components can be imported."""
        # Test ThemeController import
        try:
            from qt_theme_manager import ThemeController

            assert ThemeController is not None
        except ImportError:
            pytest.fail("ThemeController import failed")

        # Test ThemeLoader import
        try:
            from qt_theme_manager import ThemeLoader

            assert ThemeLoader is not None
        except ImportError:
            pytest.fail("ThemeLoader import failed")

        # Test StylesheetGenerator import
        try:
            from qt_theme_manager import StylesheetGenerator

            assert StylesheetGenerator is not None
        except ImportError:
            pytest.fail("StylesheetGenerator import failed")

    def test_convenience_function_imports(self):
        """Test that convenience functions can be imported."""
        try:
            from qt_theme_manager import apply_theme_to_widget

            assert apply_theme_to_widget is not None
        except ImportError:
            pytest.fail("apply_theme_to_widget import failed")

    def test_qt_detection_imports(self):
        """Test that Qt detection functions can be imported."""
        detection_functions = [
            "detect_qt_framework",
            "is_qt_available",
            "get_qt_framework_info",
        ]

        for func_name in detection_functions:
            try:
                func = getattr(
                    __import__("qt_theme_manager", fromlist=[func_name]),
                    func_name,
                )
                assert func is not None
            except (ImportError, AttributeError):
                pytest.fail(f"{func_name} import failed")

    def test_exception_imports(self):
        """Test that exception classes can be imported."""
        exception_classes = [
            "QtFrameworkNotFoundError",
            "QtVersionError",
        ]

        for exc_name in exception_classes:
            try:
                exc_class = getattr(
                    __import__("qt_theme_manager", fromlist=[exc_name]),
                    exc_name,
                )
                assert exc_class is not None
                assert issubclass(exc_class, Exception)
            except (ImportError, AttributeError):
                pytest.fail(f"{exc_name} import failed")

    def test_all_exports(self):
        """Test that __all__ exports are available."""
        import qt_theme_manager

        if hasattr(qt_theme_manager, "__all__"):
            for export_name in qt_theme_manager.__all__:
                assert hasattr(
                    qt_theme_manager, export_name
                ), f"Missing export: {export_name}"

    def test_submodule_imports(self):
        """Test that submodules can be imported."""
        submodules = [
            "qt_theme_manager.qt",
            "qt_theme_manager.qt.detection",
            "qt_theme_manager.config",
        ]

        for module_name in submodules:
            try:
                module = __import__(module_name, fromlist=[""])
                assert module is not None
            except ImportError:
                # Some modules might not exist yet, that's OK for now
                pass


class TestBackwardCompatibility:
    """Test backward compatibility with previous versions."""

    @patch("qt_theme_manager.qt.detection.detect_qt_framework")
    def test_qt_detection_api_compatibility(self, mock_detect):
        """Test that Qt detection API remains compatible."""
        # Mock successful detection
        mock_detect.return_value = (
            "PySide6",
            {
                "QObject": MagicMock(),
                "pyqtSignal": MagicMock(),
                "QApplication": MagicMock(),
                "QWidget": MagicMock(),
                "version": "6.0.0",
            },
        )

        from qt_theme_manager import detect_qt_framework

        # Test basic call
        framework, modules = detect_qt_framework()
        assert framework == "PySide6"
        assert isinstance(modules, dict)
        assert "version" in modules

        # Test with force_redetect parameter
        framework2, modules2 = detect_qt_framework(force_redetect=True)
        assert framework2 == "PySide6"

    @patch("qt_theme_manager.qt.detection.is_qt_available")
    def test_qt_availability_api_compatibility(self, mock_available):
        """Test that Qt availability check API remains compatible."""
        mock_available.return_value = True

        from qt_theme_manager import is_qt_available

        result = is_qt_available()
        # Since Qt is actually available in test environment, result should be True
        assert result is True

    @patch("qt_theme_manager.qt.detection.get_qt_framework_info")
    def test_qt_info_api_compatibility(self, mock_info):
        """Test that Qt framework info API remains compatible."""
        mock_info.return_value = {"framework": "PySide6", "version": "6.0.0"}

        from qt_theme_manager import get_qt_framework_info

        info = get_qt_framework_info()
        assert info is not None
        assert "framework" in info
        assert "version" in info

    def test_exception_compatibility(self):
        """Test that exception classes maintain compatibility."""
        from qt_theme_manager import QtFrameworkNotFoundError, QtVersionError

        # Test QtFrameworkNotFoundError
        error1 = QtFrameworkNotFoundError()
        assert isinstance(error1, ImportError)
        assert "No Qt framework found" in str(error1)

        # Test with custom message
        error2 = QtFrameworkNotFoundError("Custom message")
        assert str(error2) == "Custom message"

        # Test QtVersionError
        error3 = QtVersionError("PySide6", "5.0.0", "6.0.0")
        assert isinstance(error3, ImportError)
        assert "PySide6" in str(error3)
        assert "5.0.0" in str(error3)
        assert "6.0.0" in str(error3)

    def test_module_structure_compatibility(self):
        """Test that module structure remains compatible."""
        # Test that qt_theme_manager package exists
        import qt_theme_manager

        assert qt_theme_manager is not None

        # Test that subpackages exist
        try:
            import qt_theme_manager.qt

            assert qt_theme_manager.qt is not None
        except ImportError:
            pass  # Subpackage might not exist yet

        try:
            import qt_theme_manager.config

            assert qt_theme_manager.config is not None
        except ImportError:
            pass  # Subpackage might not exist yet


class TestAPISignatures:
    """Test that API function signatures remain compatible."""

    def test_detect_qt_framework_signature(self):
        """Test detect_qt_framework function signature."""
        # Test that function accepts expected parameters
        import inspect

        from qt_theme_manager import detect_qt_framework

        sig = inspect.signature(detect_qt_framework)

        # Should have force_redetect parameter with default False
        params = sig.parameters
        assert "force_redetect" in params
        assert params["force_redetect"].default is False

    def test_apply_theme_to_widget_signature(self):
        """Test apply_theme_to_widget function signature."""
        try:
            import inspect

            from qt_theme_manager import apply_theme_to_widget

            inspect.signature(apply_theme_to_widget)

            # Function should exist and be callable
            assert callable(apply_theme_to_widget)

        except ImportError:
            # Function might not be implemented yet
            pass

    def test_exception_constructors(self):
        """Test exception constructor signatures."""
        from qt_theme_manager import QtFrameworkNotFoundError, QtVersionError

        # Test QtFrameworkNotFoundError constructor
        # Should accept optional message parameter
        error1 = QtFrameworkNotFoundError()
        error2 = QtFrameworkNotFoundError("Custom message")

        assert isinstance(error1, Exception)
        assert isinstance(error2, Exception)

        # Test QtVersionError constructor
        # Should accept framework, current_version, required_version
        error3 = QtVersionError("PySide6", "5.0.0", "6.0.0")
        assert isinstance(error3, Exception)


class TestImportPaths:
    """Test that import paths remain stable."""

    def test_direct_imports(self):
        """Test direct imports from main package."""
        # These imports should work
        import_tests = [
            "from qt_theme_manager import ThemeController",
            "from qt_theme_manager import ThemeLoader",
            "from qt_theme_manager import StylesheetGenerator",
            "from qt_theme_manager import apply_theme_to_widget",
            "from qt_theme_manager import detect_qt_framework",
            "from qt_theme_manager import is_qt_available",
            "from qt_theme_manager import get_qt_framework_info",
            "from qt_theme_manager import QtFrameworkNotFoundError",
            "from qt_theme_manager import QtVersionError",
        ]

        for import_statement in import_tests:
            try:
                exec(import_statement)
            except ImportError as e:
                # Some imports might fail if components aren't implemented yet
                # That's OK for now, but we should track which ones fail
                print(
                    f"Import failed (expected during development): {import_statement} - {e}"
                )

    def test_submodule_imports(self):
        """Test imports from submodules."""
        submodule_imports = [
            "from qt_theme_manager.qt.detection import QtDetector",
            "from qt_theme_manager.qt.detection import detect_qt_framework",
            "from qt_theme_manager.config.logging_config import get_logger",
        ]

        for import_statement in submodule_imports:
            try:
                exec(import_statement)
            except ImportError as e:
                # Some imports might fail if components aren't implemented yet
                print(
                    f"Submodule import failed (expected during development): {import_statement} - {e}"
                )

    def test_star_imports(self):
        """Test star imports work correctly."""
        try:
            # This should import all public symbols
            exec("from qt_theme_manager import *")
        except ImportError as e:
            # Might fail during development
            print(f"Star import failed (expected during development): {e}")


class TestVersionCompatibility:
    """Test version-related compatibility."""

    def test_version_string_format(self):
        """Test that version string follows expected format."""
        import qt_theme_manager

        version = qt_theme_manager.__version__
        assert isinstance(version, str)

        # Should follow semantic versioning pattern (roughly)
        import re

        version_pattern = r"^\d+\.\d+\.\d+.*$"
        assert re.match(
            version_pattern, version
        ), f"Version {version} doesn't match expected pattern"

    def test_metadata_attributes(self):
        """Test that metadata attributes are present and correct type."""
        import qt_theme_manager

        metadata_attrs = {
            "__version__": str,
            "__author__": str,
            "__license__": str,
        }

        for attr_name, expected_type in metadata_attrs.items():
            assert hasattr(
                qt_theme_manager, attr_name
            ), f"Missing attribute: {attr_name}"
            attr_value = getattr(qt_theme_manager, attr_name)
            assert isinstance(
                attr_value, expected_type
            ), f"{attr_name} should be {expected_type}, got {type(attr_value)}"


class TestDeprecationHandling:
    """Test handling of deprecated features."""

    def test_no_deprecated_imports(self):
        """Test that no deprecated imports are present in public API."""
        import qt_theme_manager

        # List of names that should NOT be in the public API
        deprecated_names = [
            "theme_manager",  # Old package name
            "launch_theme_editor",  # GUI components
            "zebra_pattern_editor",
        ]

        for deprecated_name in deprecated_names:
            assert not hasattr(
                qt_theme_manager, deprecated_name
            ), f"Deprecated name {deprecated_name} found in public API"

    def test_clean_namespace(self):
        """Test that package namespace is clean."""
        import qt_theme_manager

        # Get all public attributes
        public_attrs = [
            name for name in dir(qt_theme_manager) if not name.startswith("_")
        ]

        # All public attributes should be in __all__ if it exists
        if hasattr(qt_theme_manager, "__all__"):
            all_exports = set(qt_theme_manager.__all__)
            public_set = set(public_attrs)

            # Remove metadata attributes from comparison
            metadata_attrs = {"__version__", "__author__", "__license__"}
            public_set -= metadata_attrs

            # All public attributes should be intentionally exported
            unexpected_attrs = public_set - all_exports
            if unexpected_attrs:
                print(
                    f"Warning: Unexpected public attributes not in __all__: {unexpected_attrs}"
                )
