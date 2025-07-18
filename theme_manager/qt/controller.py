"""
Theme controller module.
Handles theme switching, application, and state management.
"""

from typing import Dict, Any, Optional, Union, TYPE_CHECKING
from pathlib import Path

# Import handling for Qt libraries
qt_available = False
PYQT5_AVAILABLE = False
PYQT6_AVAILABLE = False
PYSIDE_AVAILABLE = False

try:
    from PyQt5.QtWidgets import QWidget, QApplication
    from PyQt5.QtCore import QObject, pyqtSignal
    qt_available = True
    PYQT5_AVAILABLE = True
    qt_framework = "PyQt5"
except ImportError:
    try:
        from PyQt6.QtWidgets import QWidget, QApplication
        from PyQt6.QtCore import QObject, pyqtSignal
        qt_available = True
        PYQT6_AVAILABLE = True
        qt_framework = "PyQt6"
    except ImportError:
        try:
            from PySide6.QtWidgets import QWidget, QApplication  
            from PySide6.QtCore import QObject, Signal as pyqtSignal
            qt_available = True
            PYSIDE_AVAILABLE = True
            qt_framework = "PySide6"
        except ImportError:
            # Create stub classes for when Qt is not available
            class QObject:
                def __init__(self): pass
            
            class QWidget:
                def setStyleSheet(self, stylesheet: str) -> None: pass
            
            class QApplication:
                @staticmethod
                def instance(): return None
                def setStyleSheet(self, stylesheet: str) -> None: pass
            
            qt_framework = "None"

from .loader import ThemeLoader
from .stylesheet import StylesheetGenerator


class ThemeController(QObject):
    """Main controller for theme management and application."""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize ThemeController.
        
        Args:
            config_path: Path to theme configuration file
        """
        super().__init__()
        
        self.loader = ThemeLoader(config_path)
        self.current_theme_name = ""
        self.current_stylesheet = ""
        
        # Load initial theme
        self._load_current_theme()
    
    def _load_current_theme(self) -> None:
        """Load the current theme from configuration."""
        try:
            self.current_theme_name = self.loader.get_current_theme()
            theme_config = self.loader.get_theme_config(self.current_theme_name)
            
            if theme_config:
                generator = StylesheetGenerator(theme_config)
                self.current_stylesheet = generator.generate_qss()
            else:
                raise ValueError(f"Theme configuration not found: {self.current_theme_name}")
                
        except Exception as e:
            print(f"Warning: Failed to load theme '{self.current_theme_name}': {e}")
            # Fallback to light theme
            self._load_fallback_theme()
    
    def _load_fallback_theme(self) -> None:
        """Load fallback theme when current theme fails."""
        fallback_config = {
            "name": "fallback",
            "display_name": "Fallback",
            "backgroundColor": "#ffffff",
            "textColor": "#000000",
            "button": {
                "background": "#f0f0f0",
                "text": "#000000",
                "hover": "#e0e0e0"
            }
        }
        
        generator = StylesheetGenerator(fallback_config)
        self.current_stylesheet = generator.generate_qss()
        self.current_theme_name = "fallback"
    
    def get_available_themes(self) -> Dict[str, Dict[str, Any]]:
        """
        Get dictionary of available themes.
        
        Returns:
            Dictionary mapping theme names to theme configurations
        """
        return self.loader.get_available_themes()
    
    def get_current_theme_name(self) -> str:
        """
        Get current theme name.
        
        Returns:
            Name of current active theme
        """
        return self.current_theme_name
    
    def get_current_stylesheet(self) -> str:
        """
        Get current QSS stylesheet.
        
        Returns:
            Current QSS stylesheet string
        """
        return self.current_stylesheet
    
    def set_theme(self, theme_name: str, save_settings: bool = True) -> bool:
        """
        Set active theme.
        
        Args:
            theme_name: Name of theme to activate
            save_settings: Whether to save theme selection to config file
            
        Returns:
            True if theme was successfully applied, False otherwise
        """
        try:
            # Get theme configuration
            theme_config = self.loader.get_theme_config(theme_name)
            if not theme_config:
                raise ValueError(f"Theme '{theme_name}' not found")
            
            # Validate theme configuration
            if not StylesheetGenerator.validate_theme_config(theme_config):
                raise ValueError(f"Invalid theme configuration for '{theme_name}'")
            
            # Generate new stylesheet
            generator = StylesheetGenerator(theme_config)
            new_stylesheet = generator.generate_qss()
            
            # Update current state
            old_theme = self.current_theme_name
            self.current_theme_name = theme_name
            self.current_stylesheet = new_stylesheet
            
            # Save settings if requested
            if save_settings:
                self.loader.update_current_theme(theme_name)
            
            # Emit signal if available
            if hasattr(self, 'theme_changed') and self.theme_changed is not None:
                self.theme_changed.emit(theme_name)
            
            print(f"Theme changed from '{old_theme}' to '{theme_name}'")
            return True
            
        except Exception as e:
            print(f"Failed to set theme '{theme_name}': {e}")
            return False
    
    def apply_theme_to_widget(self, widget: 'QWidget') -> bool:
        """
        Apply current theme to a specific widget.
        
        Args:
            widget: Qt widget to apply theme to
            
        Returns:
            True if theme was successfully applied, False otherwise
        """
        if not (PYQT5_AVAILABLE or PYQT6_AVAILABLE or PYSIDE_AVAILABLE):
            print("Warning: PyQt5/PyQt6/PySide6 not available, cannot apply theme to widget")
            return False
        
        if widget is None:
            print("Warning: Widget is None, cannot apply theme")
            return False
        
        try:
            widget.setStyleSheet(self.current_stylesheet)
            return True
        except Exception as e:
            print(f"Failed to apply theme to widget: {e}")
            return False
    
    def apply_theme_to_application(self, app: Optional['QApplication'] = None) -> bool:
        """
        Apply current theme to entire application.
        
        Args:
            app: QApplication instance. If None, uses QApplication.instance()
            
        Returns:
            True if theme was successfully applied, False otherwise
        """
        if not (PYQT5_AVAILABLE or PYQT6_AVAILABLE or PYSIDE_AVAILABLE):
            print("Warning: PyQt5/PyQt6/PySide6 not available, cannot apply theme to application")
            return False
        
        if app is None:
            app = QApplication.instance()
        
        if app is None:
            print("Warning: No QApplication instance found")
            return False
        
        try:
            app.setStyleSheet(self.current_stylesheet)
            return True
        except Exception as e:
            print(f"Failed to apply theme to application: {e}")
            return False
    
    def export_qss(self, output_path: Union[str, Path], theme_name: Optional[str] = None) -> bool:
        """
        Export QSS stylesheet to file.
        
        Args:
            output_path: Path to output QSS file
            theme_name: Theme to export (uses current theme if None)
            
        Returns:
            True if export was successful, False otherwise
        """
        try:
            if theme_name is None:
                stylesheet = self.current_stylesheet
                export_theme_name = self.current_theme_name
            else:
                theme_config = self.loader.get_theme_config(theme_name)
                if not theme_config:
                    raise ValueError(f"Theme '{theme_name}' not found")
                
                generator = StylesheetGenerator(theme_config)
                stylesheet = generator.generate_qss()
                export_theme_name = theme_name
            
            output_path = Path(output_path)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"/* QSS Stylesheet for theme: {export_theme_name} */\n")
                f.write(f"/* Generated by ThemeManager */\n\n")
                f.write(stylesheet)
            
            print(f"QSS exported to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Failed to export QSS: {e}")
            return False
    
    def reload_themes(self) -> bool:
        """
        Reload theme configurations from file.
        
        Returns:
            True if reload was successful, False otherwise
        """
        try:
            # Force reload of settings
            self.loader._settings = None
            self._load_current_theme()
            
            print("Theme configurations reloaded")
            return True
            
        except Exception as e:
            print(f"Failed to reload themes: {e}")
            return False


# Convenience function for easy theme application
def apply_theme_to_widget(widget: 'QWidget', theme_name: Optional[str] = None, 
                         config_path: Optional[Union[str, Path]] = None) -> bool:
    """
    Convenience function to apply theme to a widget.
    
    Args:
        widget: Qt widget to apply theme to
        theme_name: Name of theme to apply (uses current theme if None)
        config_path: Path to theme configuration file
        
    Returns:
        True if theme was successfully applied, False otherwise
    """
    try:
        controller = ThemeController(config_path)
        
        if theme_name is not None:
            if not controller.set_theme(theme_name, save_settings=False):
                return False
        
        return controller.apply_theme_to_widget(widget)
        
    except Exception as e:
        print(f"Failed to apply theme to widget: {e}")
        return False


def apply_theme_to_application(app: Optional['QApplication'] = None, theme_name: Optional[str] = None,
                              config_path: Optional[Union[str, Path]] = None) -> bool:
    """
    Convenience function to apply theme to entire application.
    
    Args:
        app: QApplication instance
        theme_name: Name of theme to apply (uses current theme if None)
        config_path: Path to theme configuration file
        
    Returns:
        True if theme was successfully applied, False otherwise
    """
    try:
        controller = ThemeController(config_path)
        
        if theme_name is not None:
            if not controller.set_theme(theme_name, save_settings=False):
                return False
        
        return controller.apply_theme_to_application(app)
        
    except Exception as e:
        print(f"Failed to apply theme to application: {e}")
        return False
