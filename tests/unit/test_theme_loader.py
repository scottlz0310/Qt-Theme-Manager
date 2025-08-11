"""
Unit tests for ThemeLoader class.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from qt_theme_manager.qt.loader import ThemeLoader


class TestThemeLoader:
    """Unit tests for ThemeLoader class."""

    @pytest.fixture
    def sample_theme_settings(self):
        """Sample theme settings for testing."""
        return {
            "current_theme": "light",
            "last_selected_theme": "light",
            "available_themes": {
                "light": {
                    "name": "light",
                    "display_name": "Light Theme",
                    "backgroundColor": "#ffffff",
                    "textColor": "#000000",
                    "button": {
                        "background": "#f0f0f0",
                        "text": "#000000",
                        "hover": "#e0e0e0",
                    },
                },
                "dark": {
                    "name": "dark",
                    "display_name": "Dark Theme",
                    "backgroundColor": "#2d3748",
                    "textColor": "#ffffff",
                    "button": {
                        "background": "#4a5568",
                        "text": "#ffffff",
                        "hover": "#0078d4",
                    },
                },
            },
        }

    def test_init(self):
        """Test ThemeLoader initialization."""
        loader = ThemeLoader()

        assert loader is not None
        assert loader.config_path is not None
        assert loader._settings is None

    def test_init_with_custom_config_path(self):
        """Test ThemeLoader initialization with custom config path."""
        custom_path = "/custom/path/theme_settings.json"
        loader = ThemeLoader(custom_path)

        assert loader.config_path == Path(custom_path)

    @patch("builtins.open", new_callable=mock_open)
    def test_load_settings_success(self, mock_file, sample_theme_settings):
        """Test successful settings loading."""
        with patch("json.load", return_value=sample_theme_settings):
            loader = ThemeLoader()

            settings = loader.load_settings()

            assert settings == sample_theme_settings
            assert loader._settings == sample_theme_settings

    @patch("pathlib.Path.exists", return_value=False)
    def test_load_settings_file_not_found(self, mock_exists):
        """Test settings loading with missing file."""
        loader = ThemeLoader()

        with pytest.raises(
            FileNotFoundError, match="Theme configuration file not found"
        ):
            loader.load_settings()

    @patch("builtins.open", new_callable=mock_open)
    def test_load_settings_invalid_json(self, mock_file):
        """Test settings loading with invalid JSON."""
        with patch(
            "json.load",
            side_effect=json.JSONDecodeError("Invalid JSON", "", 0),
        ):
            loader = ThemeLoader()

            with pytest.raises(
                ValueError, match="Invalid JSON in theme configuration"
            ):
                loader.load_settings()

    @patch("builtins.open", new_callable=mock_open)
    def test_save_settings(self, mock_file, sample_theme_settings):
        """Test settings saving."""
        loader = ThemeLoader()

        with patch("json.dump") as mock_dump:
            loader.save_settings(sample_theme_settings)

            mock_dump.assert_called_once_with(
                sample_theme_settings,
                mock_file.return_value.__enter__.return_value,
                indent=2,
                ensure_ascii=False,
            )
            assert loader._settings == sample_theme_settings

    @patch("builtins.open", new_callable=mock_open)
    def test_get_current_theme_default(self, mock_file):
        """Test getting current theme with default value."""
        empty_settings = {}

        with patch("json.load", return_value=empty_settings):
            loader = ThemeLoader()

            current_theme = loader.get_current_theme()

            assert current_theme == "light"

    @patch("builtins.open", new_callable=mock_open)
    def test_get_current_theme_from_settings(
        self, mock_file, sample_theme_settings
    ):
        """Test getting current theme from settings."""
        with patch("json.load", return_value=sample_theme_settings):
            loader = ThemeLoader()

            current_theme = loader.get_current_theme()

            assert current_theme == "light"

    @patch("builtins.open", new_callable=mock_open)
    def test_get_available_themes_empty(self, mock_file):
        """Test getting available themes with empty settings."""
        empty_settings = {}

        with patch("json.load", return_value=empty_settings):
            loader = ThemeLoader()

            themes = loader.get_available_themes()

            assert themes == {}

    @patch("builtins.open", new_callable=mock_open)
    def test_get_available_themes_with_data(
        self, mock_file, sample_theme_settings
    ):
        """Test getting available themes with data."""
        with patch("json.load", return_value=sample_theme_settings):
            loader = ThemeLoader()

            themes = loader.get_available_themes()

            assert "light" in themes
            assert "dark" in themes
            assert themes["light"]["display_name"] == "Light Theme"

    @patch("builtins.open", new_callable=mock_open)
    def test_get_theme_config_success(self, mock_file, sample_theme_settings):
        """Test getting theme configuration successfully."""
        with patch("json.load", return_value=sample_theme_settings):
            loader = ThemeLoader()

            theme_config = loader.get_theme_config("light")

            assert theme_config is not None
            assert theme_config["name"] == "light"
            assert theme_config["display_name"] == "Light Theme"

    @patch("builtins.open", new_callable=mock_open)
    def test_get_theme_config_not_found(
        self, mock_file, sample_theme_settings
    ):
        """Test getting theme configuration for non-existent theme."""
        with patch("json.load", return_value=sample_theme_settings):
            loader = ThemeLoader()

            theme_config = loader.get_theme_config("nonexistent")

            assert theme_config is None

    @patch("builtins.open", new_callable=mock_open)
    def test_update_current_theme_success(
        self, mock_file, sample_theme_settings
    ):
        """Test updating current theme successfully."""
        with patch("json.load", return_value=sample_theme_settings):
            with patch("json.dump") as mock_dump:
                loader = ThemeLoader()

                loader.update_current_theme("dark")

                # Should have updated the settings
                assert loader._settings["current_theme"] == "dark"
                assert loader._settings["last_selected_theme"] == "dark"
                mock_dump.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_update_current_theme_invalid(
        self, mock_file, sample_theme_settings
    ):
        """Test updating current theme with invalid theme name."""
        with patch("json.load", return_value=sample_theme_settings):
            loader = ThemeLoader()

            with pytest.raises(ValueError, match="Theme 'invalid' not found"):
                loader.update_current_theme("invalid")


class TestThemeLoaderErrorHandling:
    """Error handling tests for ThemeLoader."""

    @pytest.fixture
    def sample_theme_settings(self):
        """Sample theme settings for testing."""
        return {
            "current_theme": "light",
            "available_themes": {
                "light": {
                    "name": "light",
                    "display_name": "Light Theme",
                    "backgroundColor": "#ffffff",
                    "textColor": "#000000",
                }
            },
        }

    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_load_settings_permission_error(self, mock_file):
        """Test settings loading with permission error."""
        loader = ThemeLoader()

        with pytest.raises(PermissionError):
            loader.load_settings()

    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_save_settings_permission_error(
        self, mock_file, sample_theme_settings
    ):
        """Test settings saving with permission error."""
        loader = ThemeLoader()

        with pytest.raises(IOError, match="Failed to save theme settings"):
            loader.save_settings(sample_theme_settings)

    @patch("builtins.open", new_callable=mock_open)
    def test_update_current_theme_save_failure(
        self, mock_file, sample_theme_settings
    ):
        """Test update current theme with save failure."""
        with patch("json.load", return_value=sample_theme_settings):
            with patch("json.dump", side_effect=IOError("Save failed")):
                loader = ThemeLoader()

                with pytest.raises(
                    IOError, match="Failed to save theme settings"
                ):
                    loader.update_current_theme("light")

    @patch("builtins.open", new_callable=mock_open)
    def test_load_settings_without_file_check(self, mock_file):
        """Test loading settings when file doesn't exist but open succeeds."""
        with patch("pathlib.Path.exists", return_value=False):
            loader = ThemeLoader()

            with pytest.raises(FileNotFoundError):
                loader.load_settings()


class TestThemeLoaderIntegration:
    """Integration tests for ThemeLoader."""

    @pytest.fixture
    def sample_theme_settings(self):
        """Sample theme settings for testing."""
        return {
            "current_theme": "light",
            "last_selected_theme": "light",
            "available_themes": {
                "light": {
                    "name": "light",
                    "display_name": "Light Theme",
                    "backgroundColor": "#ffffff",
                    "textColor": "#000000",
                    "button": {
                        "background": "#f0f0f0",
                        "text": "#000000",
                        "hover": "#e0e0e0",
                    },
                },
                "dark": {
                    "name": "dark",
                    "display_name": "Dark Theme",
                    "backgroundColor": "#2d3748",
                    "textColor": "#ffffff",
                    "button": {
                        "background": "#4a5568",
                        "text": "#ffffff",
                        "hover": "#0078d4",
                    },
                },
            },
        }

    @patch("builtins.open", new_callable=mock_open)
    def test_full_settings_workflow(self, mock_file, sample_theme_settings):
        """Test complete settings workflow."""
        with patch("json.load", return_value=sample_theme_settings):
            with patch("json.dump") as mock_dump:
                loader = ThemeLoader()

                # Load settings
                settings = loader.load_settings()
                assert settings == sample_theme_settings

                # Get current theme
                current = loader.get_current_theme()
                assert current == "light"

                # Get available themes
                themes = loader.get_available_themes()
                assert len(themes) == 2

                # Get specific theme config
                light_config = loader.get_theme_config("light")
                assert light_config["display_name"] == "Light Theme"

                # Update current theme
                loader.update_current_theme("dark")
                assert loader._settings["current_theme"] == "dark"
                mock_dump.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_theme_data_loading_workflow(
        self, mock_file, sample_theme_settings
    ):
        """Test theme data loading workflow."""
        with patch("json.load", return_value=sample_theme_settings):
            loader = ThemeLoader()

            # Test loading different themes
            light_theme = loader.get_theme_config("light")
            dark_theme = loader.get_theme_config("dark")

            assert light_theme is not None
            assert dark_theme is not None
            assert (
                light_theme["backgroundColor"] != dark_theme["backgroundColor"]
            )

            # Test non-existent theme
            missing_theme = loader.get_theme_config("missing")
            assert missing_theme is None

    @patch("builtins.open", new_callable=mock_open)
    def test_concurrent_access_handling(
        self, mock_file, sample_theme_settings
    ):
        """Test handling of concurrent access scenarios."""
        with patch("json.load", return_value=sample_theme_settings):
            # Create multiple loader instances
            loader1 = ThemeLoader()
            loader2 = ThemeLoader()

            # Both should be able to load settings independently
            settings1 = loader1.load_settings()
            settings2 = loader2.load_settings()

            assert settings1 == settings2
            # Settings content should be the same, but instances should be independent
            assert loader1 is not loader2  # Different loader instances


class TestThemeLoaderUtilities:
    """Utility function tests for ThemeLoader."""

    @pytest.fixture
    def sample_theme_settings(self):
        """Sample theme settings for testing."""
        return {
            "current_theme": "light",
            "available_themes": {
                "light": {
                    "name": "light",
                    "display_name": "Light Theme",
                    "backgroundColor": "#ffffff",
                    "textColor": "#000000",
                },
                "dark": {
                    "name": "dark",
                    "display_name": "Dark Theme",
                    "backgroundColor": "#2d3748",
                    "textColor": "#ffffff",
                },
            },
        }

    @patch("builtins.open", new_callable=mock_open)
    def test_theme_name_validation(self, mock_file, sample_theme_settings):
        """Test theme name validation logic."""
        with patch("json.load", return_value=sample_theme_settings):
            loader = ThemeLoader()

            # Valid theme names
            assert loader.get_theme_config("light") is not None
            assert loader.get_theme_config("dark") is not None

            # Invalid theme names
            assert loader.get_theme_config("") is None
            assert loader.get_theme_config("nonexistent") is None
            assert loader.get_theme_config(None) is None

    @patch("builtins.open", new_callable=mock_open)
    def test_settings_caching_behavior(self, mock_file, sample_theme_settings):
        """Test that settings are cached after first load."""
        with patch(
            "json.load", return_value=sample_theme_settings
        ) as mock_load:
            loader = ThemeLoader()

            # First call should load from file
            settings1 = loader.load_settings()
            assert mock_load.call_count == 1

            # Subsequent calls should use cached settings
            current_theme = loader.get_current_theme()
            themes = loader.get_available_themes()
            theme_config = loader.get_theme_config("light")

            # json.load should still only be called once
            assert mock_load.call_count == 1

            # But we can force reload
            settings2 = loader.load_settings()
            assert mock_load.call_count == 2

    @patch("builtins.open", new_callable=mock_open)
    def test_path_handling(self, mock_file, sample_theme_settings):
        """Test path handling for different input types."""
        with patch("json.load", return_value=sample_theme_settings):
            # Test with string path
            loader1 = ThemeLoader("/path/to/config.json")
            assert loader1.config_path == Path("/path/to/config.json")

            # Test with Path object
            path_obj = Path("/another/path/config.json")
            loader2 = ThemeLoader(path_obj)
            assert loader2.config_path == path_obj

            # Test with None (default)
            loader3 = ThemeLoader(None)
            assert loader3.config_path is not None
            assert "theme_settings.json" in str(loader3.config_path)
