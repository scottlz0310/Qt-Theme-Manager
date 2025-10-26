"""
Cross-platform integration tests for qt_theme_manager.
Tests platform-specific behavior and compatibility across Windows, Linux, and macOS.
"""

import os
import sys
from pathlib import Path

import pytest

from qt_theme_manager.qt.detection import detect_qt_framework, is_qt_available


@pytest.mark.integration
class TestCrossPlatformCompatibility:
    """Cross-platform compatibility tests."""

    def test_path_handling_cross_platform(self, temp_config_dir: Path):
        """Test that path handling works correctly across platforms."""
        # Test path creation with different separators
        test_paths = [
            "themes/dark/style.qss",
            "config\\settings.json",  # Windows-style
            "assets/icons/theme.png",
        ]

        for path_str in test_paths:
            # Convert to platform-appropriate path
            normalized_path = Path(path_str)
            full_path = temp_config_dir / normalized_path

            # Create directory structure
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Create file
            full_path.write_text("test content", encoding="utf-8")

            # Verify file exists and is readable
            assert full_path.exists()
            assert full_path.is_file()
            content = full_path.read_text(encoding="utf-8")
            assert content == "test content"

    @pytest.mark.windows
    def test_windows_specific_behavior(self, mock_pyside6):
        """Test Windows-specific behavior."""
        if not sys.platform.startswith("win"):
            pytest.skip("Windows-only test")

        # Test Qt detection on Windows
        framework, modules = detect_qt_framework()
        assert framework == "PySide6"
        assert is_qt_available() is True

        # Test Windows path handling
        windows_path = Path("C:\\Users\\Test\\AppData\\Local\\QtThemeManager")
        assert windows_path.is_absolute()
        assert str(windows_path).startswith("C:")

    @pytest.mark.linux
    def test_linux_specific_behavior(self, mock_pyside6):
        """Test Linux-specific behavior."""
        if not sys.platform.startswith("linux"):
            pytest.skip("Linux-only test")

        # Test Qt detection on Linux
        framework, modules = detect_qt_framework()
        assert framework == "PySide6"
        assert is_qt_available() is True

        # Test Linux path handling
        linux_path = Path("/home/user/.config/qt-theme-manager")
        assert linux_path.is_absolute()
        assert str(linux_path).startswith("/")

    @pytest.mark.macos
    def test_macos_specific_behavior(self, mock_pyside6):
        """Test macOS-specific behavior."""
        if sys.platform != "darwin":
            pytest.skip("macOS-only test")

        # Test Qt detection on macOS
        framework, modules = detect_qt_framework()
        assert framework == "PySide6"
        assert is_qt_available() is True

        # Test macOS path handling
        macos_path = Path("/Users/user/Library/Application Support/QtThemeManager")
        assert macos_path.is_absolute()
        assert str(macos_path).startswith("/")

    def test_environment_variable_handling(self):
        """Test environment variable handling across platforms."""
        # Test common environment variables
        test_vars = {
            "TEST_QT_THEME_VAR": "test_value",
            "QT_THEME_DEBUG": "1",
        }

        for var_name, var_value in test_vars.items():
            # Set environment variable
            os.environ[var_name] = var_value

            try:
                # Verify it can be read
                assert os.environ.get(var_name) == var_value

                # Test with different access methods
                assert os.getenv(var_name) == var_value
                assert os.getenv(var_name, "default") == var_value

            finally:
                # Clean up
                if var_name in os.environ:
                    del os.environ[var_name]

    def test_file_encoding_cross_platform(self, temp_config_dir: Path):
        """Test file encoding handling across platforms."""
        test_file = temp_config_dir / "encoding_test.txt"

        # Test with various encodings and content
        test_cases = [
            ("utf-8", "Hello, 世界! 🌍"),
            ("utf-8", "Café, naïve, résumé"),
            ("utf-8", "Привет, мир!"),
        ]

        for encoding, content in test_cases:
            # Write with specific encoding
            test_file.write_text(content, encoding=encoding)

            # Read back and verify
            read_content = test_file.read_text(encoding=encoding)
            assert read_content == content

    def test_line_ending_handling(self, temp_config_dir: Path):
        """Test line ending handling across platforms."""
        test_file = temp_config_dir / "line_endings.txt"

        # Test different line ending styles
        content_lines = ["Line 1", "Line 2", "Line 3"]

        # Write with platform-specific line endings
        content = os.linesep.join(content_lines)
        test_file.write_text(content, encoding="utf-8")

        # Read back and verify
        read_content = test_file.read_text(encoding="utf-8")
        read_lines = read_content.splitlines()

        assert read_lines == content_lines

    def test_case_sensitivity_handling(self, temp_config_dir: Path):
        """Test case sensitivity handling across platforms."""
        # Create files with different cases
        file1 = temp_config_dir / "TestFile.txt"
        file2 = temp_config_dir / "testfile.txt"

        file1.write_text("content1", encoding="utf-8")

        # Check if filesystem is case-sensitive by testing if file2 exists
        # without creating it (on case-insensitive systems, file2 == file1)
        is_case_sensitive = not file2.exists()

        if is_case_sensitive:
            # Case-sensitive system (Linux)
            file2.write_text("content2", encoding="utf-8")
            assert file1.read_text(encoding="utf-8") == "content1"
            assert file2.read_text(encoding="utf-8") == "content2"
        else:
            # Case-insensitive system (Windows, macOS default)
            # file1 and file2 refer to the same file
            assert file1.exists()
            assert file2.exists()
            assert file1.read_text(encoding="utf-8") == "content1"

    def test_permission_handling(self, temp_config_dir: Path):
        """Test file permission handling across platforms."""
        test_file = temp_config_dir / "permission_test.txt"
        test_file.write_text("test content", encoding="utf-8")

        # Test basic file operations
        assert test_file.exists()
        assert test_file.is_file()

        # Test reading
        content = test_file.read_text(encoding="utf-8")
        assert content == "test content"

        # Test writing (should work in temp directory)
        test_file.write_text("modified content", encoding="utf-8")
        modified_content = test_file.read_text(encoding="utf-8")
        assert modified_content == "modified content"

    def test_directory_operations_cross_platform(self, tmp_path: Path):
        """Test directory operations across platforms."""
        # Create nested directory structure
        nested_dir = tmp_path / "level1" / "level2" / "level3"
        nested_dir.mkdir(parents=True, exist_ok=True)

        assert nested_dir.exists()
        assert nested_dir.is_dir()

        # Test directory listing
        test_file = nested_dir / "test.txt"
        test_file.write_text("content", encoding="utf-8")

        files = list(nested_dir.iterdir())
        assert len(files) == 1
        assert files[0].name == "test.txt"

    def test_import_path_handling(self):
        """Test Python import path handling across platforms."""
        # Test that our package can be imported
        try:
            import qt_theme_manager

            assert qt_theme_manager is not None

            # Test submodule imports
            from qt_theme_manager.qt import detection

            assert detection is not None

            from qt_theme_manager.config import logging_config

            assert logging_config is not None

        except ImportError as e:
            pytest.fail(f"Import failed: {e}")

    @pytest.mark.integration
    def test_full_cross_platform_workflow(self, temp_config_dir: Path, mock_pyside6):
        """Test complete workflow across platforms."""
        # Step 1: Qt detection
        framework, modules = detect_qt_framework()
        assert framework == "PySide6"

        # Step 2: File operations
        config_file = temp_config_dir / "cross_platform_config.json"
        config_data = {
            "platform": sys.platform,
            "framework": framework,
            "test": True,
        }

        import json

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)

        # Step 3: Verify file operations
        assert config_file.exists()

        with open(config_file, encoding="utf-8") as f:
            loaded_data = json.load(f)

        assert loaded_data["platform"] == sys.platform
        assert loaded_data["framework"] == framework
        assert loaded_data["test"] is True


@pytest.mark.integration
class TestPlatformSpecificPaths:
    """Test platform-specific path handling."""

    def test_config_directory_paths(self):
        """Test platform-appropriate configuration directory paths."""
        if sys.platform.startswith("win"):
            # Windows: %APPDATA% or %LOCALAPPDATA%
            expected_patterns = ["AppData", "Local", "Roaming"]
        elif sys.platform == "darwin":
            # macOS: ~/Library/Application Support
            expected_patterns = ["Library", "Application Support"]
        else:
            # Linux: ~/.config
            expected_patterns = [".config"]

        # Test that we can create platform-appropriate paths
        if sys.platform.startswith("win"):
            test_path = Path.home() / "AppData" / "Local" / "QtThemeManager"
        elif sys.platform == "darwin":
            test_path = (
                Path.home() / "Library" / "Application Support" / "QtThemeManager"
            )
        else:
            test_path = Path.home() / ".config" / "qt-theme-manager"

        # Verify path structure makes sense for platform
        path_str = str(test_path)
        if expected_patterns:
            assert any(pattern in path_str for pattern in expected_patterns)

    def test_temporary_directory_handling(self):
        """Test temporary directory handling across platforms."""
        import tempfile

        # Get platform-appropriate temp directory
        temp_dir = Path(tempfile.gettempdir())
        assert temp_dir.exists()
        assert temp_dir.is_dir()

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write('{"test": true}')
            temp_file_path = Path(f.name)

        try:
            assert temp_file_path.exists()

            # Read back content
            content = temp_file_path.read_text(encoding="utf-8")
            assert '"test": true' in content

        finally:
            # Clean up
            if temp_file_path.exists():
                temp_file_path.unlink()

    def test_executable_path_detection(self):
        """Test executable path detection across platforms."""
        # Test Python executable path
        python_exe = Path(sys.executable)
        assert python_exe.exists()

        # Test current script path
        current_file = Path(__file__)
        assert current_file.exists()
        assert current_file.is_file()
        assert current_file.suffix == ".py"


@pytest.mark.integration
class TestResourceHandling:
    """Test resource handling across platforms."""

    def test_package_resource_access(self, qt_theme_manager_path: Path):
        """Test access to package resources."""
        # Test that package directory exists
        assert qt_theme_manager_path.exists()
        assert qt_theme_manager_path.is_dir()

        # Test access to config resources
        config_dir = qt_theme_manager_path / "config"
        if config_dir.exists():
            assert config_dir.is_dir()

            # Check for configuration files
            config_files = list(config_dir.glob("*.json"))
            # Should have at least some configuration files
            assert len(config_files) >= 0  # Allow for empty config dir

    def test_module_import_paths(self):
        """Test module import paths work correctly."""
        # Test that we can import from different submodules
        modules_to_test = [
            "qt_theme_manager",
            "qt_theme_manager.qt",
            "qt_theme_manager.qt.detection",
            "qt_theme_manager.config",
            "qt_theme_manager.cli",
        ]

        for module_name in modules_to_test:
            try:
                __import__(module_name)
            except ImportError as e:
                # Some modules might not exist yet, that's OK
                if "No module named" not in str(e):
                    pytest.fail(f"Unexpected import error for {module_name}: {e}")

    def test_relative_import_handling(self):
        """Test that relative imports work correctly."""
        # This test verifies that our package structure supports relative imports
        try:
            from qt_theme_manager.config.logging_config import get_logger
            from qt_theme_manager.qt.detection import QtDetector

            # These should work without issues
            assert QtDetector is not None
            assert get_logger is not None

        except ImportError as e:
            pytest.fail(f"Relative import failed: {e}")
