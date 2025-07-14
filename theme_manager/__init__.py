"""
ThemeManager for PyQt5/PySide6
================================

A theme management library for PyQt5/PySide6 applications.
Supports dynamic theme switching with dark, light, and high contrast themes.

Author: ThemeManager Team
Version: 0.0.1
"""

__version__ = "0.0.1"
__author__ = "ThemeManager Team"

from .qt.controller import ThemeController, apply_theme_to_widget
from .qt.loader import ThemeLoader
from .qt.stylesheet import StylesheetGenerator

__all__ = [
    "ThemeController",
    "apply_theme_to_widget", 
    "ThemeLoader",
    "StylesheetGenerator",
]
