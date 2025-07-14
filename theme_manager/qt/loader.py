"""
Theme configuration loader module.
Handles loading and parsing of theme_settings.json file.
"""

import json
from typing import Dict, Any, Optional, Union
from pathlib import Path


class ThemeLoader:
    """Theme configuration loader for managing theme settings."""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize ThemeLoader with configuration file path.
        
        Args:
            config_path: Path to theme_settings.json file. 
                        If None, uses default config/theme_settings.json
        """
        if config_path is None:
            # Default to config/theme_settings.json relative to this module
            current_dir = Path(__file__).parent.parent
            self.config_path = current_dir / "config" / "theme_settings.json"
        else:
            self.config_path = Path(config_path)
        self._settings: Optional[Dict[str, Any]] = None
    
    def load_settings(self) -> Dict[str, Any]:
        """
        Load theme settings from JSON file.
        
        Returns:
            Dictionary containing theme settings
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Theme configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._settings = json.load(f)
                return self._settings
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in theme configuration: {e}")
    
    def get_available_themes(self) -> Dict[str, Dict[str, Any]]:
        """
        Get list of available themes.
        
        Returns:
            Dictionary of available themes
        """
        if self._settings is None:
            self.load_settings()
        
        if self._settings is not None:
            return self._settings.get("available_themes", {})
        return {}
    
    def get_current_theme(self) -> str:
        """
        Get current active theme name.
        
        Returns:
            Name of current theme
        """
        if self._settings is None:
            self.load_settings()
        
        if self._settings is not None:
            return self._settings.get("current_theme", "light")
        return "light"
    
    def get_theme_config(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for specific theme.
        
        Args:
            theme_name: Name of the theme
            
        Returns:
            Theme configuration dictionary or None if not found
        """
        available_themes = self.get_available_themes()
        return available_themes.get(theme_name)
    
    def save_settings(self, settings: Dict[str, Any]) -> None:
        """
        Save theme settings to JSON file.
        
        Args:
            settings: Settings dictionary to save
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            self._settings = settings
        except Exception as e:
            raise IOError(f"Failed to save theme settings: {e}")
    
    def update_current_theme(self, theme_name: str) -> None:
        """
        Update current theme in settings.
        
        Args:
            theme_name: Name of theme to set as current
        """
        if self._settings is None:
            self.load_settings()
        
        if self._settings is None:
            raise RuntimeError("Failed to load theme settings")
        
        available_themes = self.get_available_themes()
        if theme_name not in available_themes:
            raise ValueError(f"Theme '{theme_name}' not found in available themes")
        
        self._settings["current_theme"] = theme_name
        self._settings["last_selected_theme"] = theme_name
        self.save_settings(self._settings)
