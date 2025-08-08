"""
Qt Theme Manager - Pure Library Edition
=======================================

A comprehensive theme management library for PyQt5/PyQt6/PySide6 applications.
This library provides core theme management functionality without GUI dependencies,
following the principle of separation of concerns for better maintainability.

Core Features:
- Dynamic theme switching with 16+ built-in themes
- Automatic Qt framework detection (PySide6 → PyQt6 → PyQt5)
- QSS stylesheet generation and export
- Comprehensive API for theme management
- Zero GUI dependencies in core library

Library Architecture:
- Pure library design for maximum reusability
- Modular components with clear interfaces
- Backward compatibility with existing APIs
- Minimal dependencies for lightweight integration

Author: ThemeManager Team
Version: 0.2.4
License: MIT
"""

__version__ = "0.2.4"
__author__ = "ThemeManager Team"
__license__ = "MIT"

# Core theme management components
from .qt.controller import ThemeController, apply_theme_to_widget

# Qt framework detection utilities
from .qt.detection import (
    QtFrameworkNotFoundError,
    QtVersionError,
    detect_qt_framework,
    get_qt_framework_info,
    is_qt_available,
)
from .qt.loader import ThemeLoader
from .qt.stylesheet import StylesheetGenerator

# Public API exports
__all__ = [
    # Core Components
    "ThemeController",
    "ThemeLoader",
    "StylesheetGenerator",
    # Convenience Functions
    "apply_theme_to_widget",
    # Qt Detection
    "detect_qt_framework",
    "is_qt_available",
    "get_qt_framework_info",
    # Exceptions
    "QtFrameworkNotFoundError",
    "QtVersionError",
    # Metadata
    "__version__",
    "__author__",
    "__license__",
]
