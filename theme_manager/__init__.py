"""
ThemeManager for PyQt5/PyQt6/PySide6
====================================

A comprehensive theme management library for PyQt5/PyQt6/PySide6 applications.
Supports dynamic theme switching with advanced theme editor and 16+ built-in themes.

Author: ThemeManager Team
Version: 0.2.2
"""

__version__ = "0.2.2"
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
