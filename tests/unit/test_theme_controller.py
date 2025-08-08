"""
Unit tests for ThemeController class.
"""

import pytest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path

from qt_theme_manager.qt.controller import ThemeController, apply_theme_to_widget, apply_theme_to_application


class TestThemeController:
    """Unit tests for ThemeController class."""

    @pytest.fixture
    def mock_theme_settings(self):
        """Mock theme settings data."""
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
                        "hover": "#e0e0e0"
                    }
                },
                "dark": {
                    "name": "dark",
                    "display_name": "Dark Theme",
                    "backgroundColor": "#2d3748",
                    "textColor": "#ffffff",
                    "button": {
                        "background": "#4a5568",
                        "text": "#ffffff",
                        "hover": "#0078d4"
                    }
                }
            }
        }

    @patch("qt_theme_manager.qt.controller.detect_qt_framework")
    @patch("builtins.open", new_callable=mock_open)
    def test_init_with_qt_available(self, mock_file, mock_detect, mock_theme_settings):
        """Test ThemeController initialization with Qt available."""
        mock_detect.return_value = ("PySide6", {
            "QObject": MagicMock,
            "pyqtSignal": MagicMock,
            "QApplication": MagicMock,
            "QWidget": MagicMock,
            "version": "6.0.0"
        })
        mock_file.return_value.read.return_value = str(mock_theme_settings)
        
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
        
        assert controller is not None
        assert controller.loader is not None
        assert controller.current_theme_name == "light"
        assert len(controller.current_stylesheet) > 0

    @patch("qt_theme_manager.qt.controller.detect_qt_framework")
    @patch("builtins.open", new_callable=mock_open)
    def test_init_with_qt_unavailable(self, mock_file, mock_detect, mock_theme_settings):
        """Test ThemeController initialization with Qt unavailable."""
        from qt_theme_manager.qt.detection import QtFrameworkNotFoundError
        mock_detect.side_effect = QtFrameworkNotFoundError()
        
        with patch("json.load", return_value=mock_theme_settings):
            # Should not raise exception, should use fallback
            controller = ThemeController()
            assert controller is not None

    @patch("builtins.open", new_callable=mock_open)
    def test_get_available_themes(self, mock_file, mock_theme_settings):
        """Test getting available themes."""
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            themes = controller.get_available_themes()
            
            assert isinstance(themes, dict)
            assert "light" in themes
            assert "dark" in themes
            assert themes["light"]["display_name"] == "Light Theme"

    @patch("builtins.open", new_callable=mock_open)
    def test_get_current_theme_name(self, mock_file, mock_theme_settings):
        """Test getting current theme name."""
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            current_theme = controller.get_current_theme_name()
            
            assert current_theme == "light"

    @patch("builtins.open", new_callable=mock_open)
    def test_get_current_stylesheet(self, mock_file, mock_theme_settings):
        """Test getting current stylesheet."""
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            stylesheet = controller.get_current_stylesheet()
            
            assert isinstance(stylesheet, str)
            assert len(stylesheet) > 0

    @patch("builtins.open", new_callable=mock_open)
    def test_set_theme_success(self, mock_file, mock_theme_settings):
        """Test successful theme setting."""
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            result = controller.set_theme("dark")
            
            assert result is True
            assert controller.get_current_theme_name() == "dark"

    @patch("builtins.open", new_callable=mock_open)
    def test_set_theme_failure(self, mock_file, mock_theme_settings):
        """Test theme setting failure with nonexistent theme."""
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            result = controller.set_theme("nonexistent")
            
            assert result is False
            assert controller.get_current_theme_name() == "light"  # Should remain unchanged

    @patch("builtins.open", new_callable=mock_open)
    def test_export_qss(self, mock_file, mock_theme_settings):
        """Test QSS export functionality."""
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            with patch("builtins.open", mock_open()) as mock_export_file:
                result = controller.export_qss("test.qss")
                
                assert result is True
                mock_export_file.assert_called_once()

    @patch("qt_theme_manager.qt.controller.detect_qt_framework")
    @patch("builtins.open", new_callable=mock_open)
    def test_apply_theme_to_widget_success(self, mock_file, mock_detect, mock_theme_settings):
        """Test successful theme application to widget."""
        mock_widget = MagicMock()
        mock_detect.return_value = ("PySide6", {
            "QObject": MagicMock,
            "pyqtSignal": MagicMock,
            "QApplication": MagicMock,
            "QWidget": MagicMock,
            "version": "6.0.0"
        })
        
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            result = controller.apply_theme_to_widget(mock_widget)
            
            assert result is True
            mock_widget.setStyleSheet.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_apply_theme_to_widget_qt_unavailable(self, mock_file, mock_theme_settings):
        """Test theme application to widget when Qt is unavailable."""
        mock_widget = MagicMock()
        
        with patch("json.load", return_value=mock_theme_settings):
            with patch("qt_theme_manager.qt.controller.qt_available", False):
                controller = ThemeController()
                
                result = controller.apply_theme_to_widget(mock_widget)
                
                assert result is False

    @patch("qt_theme_manager.qt.controller.detect_qt_framework")
    @patch("builtins.open", new_callable=mock_open)
    def test_apply_theme_to_application_success(self, mock_file, mock_detect, mock_theme_settings):
        """Test successful theme application to application."""
        mock_app = MagicMock()
        mock_detect.return_value = ("PySide6", {
            "QObject": MagicMock,
            "pyqtSignal": MagicMock,
            "QApplication": MagicMock,
            "QWidget": MagicMock,
            "version": "6.0.0"
        })
        
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            result = controller.apply_theme_to_application(mock_app)
            
            assert result is True
            mock_app.setStyleSheet.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_reload_themes(self, mock_file, mock_theme_settings):
        """Test theme reload functionality."""
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            result = controller.reload_themes()
            
            assert result is True


class TestApplyThemeToWidget:
    """Test convenience functions for theme application."""

    @pytest.fixture
    def mock_theme_settings(self):
        """Mock theme settings data."""
        return {
            "current_theme": "light",
            "available_themes": {
                "light": {
                    "name": "light",
                    "display_name": "Light Theme",
                    "backgroundColor": "#ffffff",
                    "textColor": "#000000"
                }
            }
        }

    @patch("qt_theme_manager.qt.controller.detect_qt_framework")
    @patch("builtins.open", new_callable=mock_open)
    def test_apply_theme_to_widget_success(self, mock_file, mock_detect, mock_theme_settings):
        """Test successful theme application to widget via convenience function."""
        mock_widget = MagicMock()
        mock_detect.return_value = ("PySide6", {
            "QObject": MagicMock,
            "pyqtSignal": MagicMock,
            "QApplication": MagicMock,
            "QWidget": MagicMock,
            "version": "6.0.0"
        })
        
        with patch("json.load", return_value=mock_theme_settings):
            result = apply_theme_to_widget(mock_widget)
            
            assert result is True

    @patch("qt_theme_manager.qt.controller.detect_qt_framework")
    @patch("builtins.open", new_callable=mock_open)
    def test_apply_theme_to_widget_with_theme_name(self, mock_file, mock_detect, mock_theme_settings):
        """Test theme application to widget with specific theme name."""
        mock_widget = MagicMock()
        mock_detect.return_value = ("PySide6", {
            "QObject": MagicMock,
            "pyqtSignal": MagicMock,
            "QApplication": MagicMock,
            "QWidget": MagicMock,
            "version": "6.0.0"
        })
        
        with patch("json.load", return_value=mock_theme_settings):
            result = apply_theme_to_widget(mock_widget, "light")
            
            assert result is True

    @patch("builtins.open", new_callable=mock_open)
    def test_apply_theme_to_widget_failure(self, mock_file, mock_theme_settings):
        """Test theme application failure."""
        mock_widget = MagicMock()
        
        with patch("json.load", return_value=mock_theme_settings):
            with patch("qt_theme_manager.qt.controller.qt_available", False):
                result = apply_theme_to_widget(mock_widget)
                
                assert result is False

    def test_apply_theme_to_widget_exception(self):
        """Test theme application with exception handling."""
        mock_widget = MagicMock()
        
        with patch("qt_theme_manager.qt.controller.ThemeController", side_effect=Exception("Test error")):
            result = apply_theme_to_widget(mock_widget)
            
            assert result is False


class TestThemeControllerErrorHandling:
    """Error handling tests for ThemeController."""

    @pytest.fixture
    def mock_theme_settings(self):
        """Mock theme settings data."""
        return {
            "current_theme": "light",
            "available_themes": {
                "light": {
                    "name": "light",
                    "display_name": "Light Theme",
                    "backgroundColor": "#ffffff",
                    "textColor": "#000000"
                }
            }
        }

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_missing_theme(self, mock_file, mock_theme_settings):
        """Test handling of missing theme."""
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            result = controller.set_theme("missing_theme")
            
            assert result is False

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_invalid_theme_data(self, mock_file):
        """Test handling of invalid theme data."""
        invalid_settings = {
            "current_theme": "invalid",
            "available_themes": {
                "invalid": {
                    "name": "invalid"
                    # Missing required fields
                }
            }
        }
        
        with patch("json.load", return_value=invalid_settings):
            controller = ThemeController()
            
            result = controller.set_theme("invalid")
            
            assert result is False

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_widget_application_error(self, mock_file, mock_theme_settings):
        """Test handling of widget application error."""
        mock_widget = MagicMock()
        mock_widget.setStyleSheet.side_effect = Exception("Widget error")
        
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            result = controller.apply_theme_to_widget(mock_widget)
            
            assert result is False

    @patch("builtins.open", new_callable=mock_open)
    def test_handle_export_error(self, mock_file, mock_theme_settings):
        """Test handling of QSS export error."""
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            with patch("builtins.open", side_effect=IOError("Export error")):
                result = controller.export_qss("test.qss")
                
                assert result is False


class TestThemeControllerIntegration:
    """Integration tests for ThemeController."""

    @pytest.fixture
    def mock_theme_settings(self):
        """Mock theme settings data."""
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
                        "hover": "#e0e0e0"
                    }
                },
                "dark": {
                    "name": "dark",
                    "display_name": "Dark Theme",
                    "backgroundColor": "#2d3748",
                    "textColor": "#ffffff",
                    "button": {
                        "background": "#4a5568",
                        "text": "#ffffff",
                        "hover": "#0078d4"
                    }
                }
            }
        }

    @patch("qt_theme_manager.qt.controller.detect_qt_framework")
    @patch("builtins.open", new_callable=mock_open)
    def test_full_theme_application_workflow(self, mock_file, mock_detect, mock_theme_settings):
        """Test complete theme application workflow."""
        mock_widget = MagicMock()
        mock_detect.return_value = ("PySide6", {
            "QObject": MagicMock,
            "pyqtSignal": MagicMock,
            "QApplication": MagicMock,
            "QWidget": MagicMock,
            "version": "6.0.0"
        })
        
        with patch("json.load", return_value=mock_theme_settings):
            # Initialize controller
            controller = ThemeController()
            assert controller.get_current_theme_name() == "light"
            
            # Get available themes
            themes = controller.get_available_themes()
            assert "dark" in themes
            
            # Switch theme
            result = controller.set_theme("dark")
            assert result is True
            assert controller.get_current_theme_name() == "dark"
            
            # Apply to widget
            result = controller.apply_theme_to_widget(mock_widget)
            assert result is True
            mock_widget.setStyleSheet.assert_called()
            
            # Export QSS
            with patch("builtins.open", mock_open()) as mock_export:
                result = controller.export_qss("dark_theme.qss")
                assert result is True
                mock_export.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_theme_switching_workflow(self, mock_file, mock_theme_settings):
        """Test theme switching workflow."""
        with patch("json.load", return_value=mock_theme_settings):
            controller = ThemeController()
            
            # Start with light theme
            assert controller.get_current_theme_name() == "light"
            light_stylesheet = controller.get_current_stylesheet()
            
            # Switch to dark theme
            result = controller.set_theme("dark")
            assert result is True
            assert controller.get_current_theme_name() == "dark"
            dark_stylesheet = controller.get_current_stylesheet()
            
            # Stylesheets should be different
            assert light_stylesheet != dark_stylesheet
            
            # Switch back to light theme
            result = controller.set_theme("light")
            assert result is True
            assert controller.get_current_theme_name() == "light"
            
            # Should be back to original stylesheet
            current_stylesheet = controller.get_current_stylesheet()
            assert current_stylesheet == light_stylesheet