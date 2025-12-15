"""
Qt framework detection module.
Handles automatic detection of available Qt frameworks with
proper error handling.
"""

from __future__ import annotations

import importlib
from typing import cast

from ..config.logging_config import get_logger
from .types import (
    QtApplicationType,
    QtModuleMap,
    QtObjectType,
    QtSignalFactory,
    QtWidgetType,
)

logger = get_logger(__name__)


class QtFrameworkNotFoundError(ImportError):
    """Qt framework not found error with installation guidance."""

    def __init__(self, message: str | None = None):
        if message is None:
            message = (
                "No Qt framework found. Please install one of:\n"
                "  pip install PySide6  # Recommended\n"
                "  pip install PyQt6\n"
                "  pip install PyQt5"
            )
        super().__init__(message)


class QtVersionError(ImportError):
    """Qt framework version requirement error."""

    def __init__(self, framework: str, current_version: str, required_version: str):
        message = (
            f"{framework} version {current_version} is not supported. "
            f"Minimum required version: {required_version}"
        )
        super().__init__(message)


class QtDetector:
    """Qt framework detector with caching and version validation."""

    MIN_VERSIONS = {"PySide6": "6.0.0", "PyQt6": "6.2.0", "PyQt5": "5.15.0"}

    def __init__(self) -> None:
        self._cached_framework: str | None = None
        self._cached_modules: QtModuleMap | None = None
        self._detection_attempted = False

    def detect_qt_framework(
        self, force_redetect: bool = False
    ) -> tuple[str, QtModuleMap]:
        """
        Detect available Qt framework with caching.
        """
        if not force_redetect and self._cached_framework and self._cached_modules:
            logger.debug(f"Using cached Qt framework: {self._cached_framework}")
            return self._cached_framework, self._cached_modules

        logger.debug("Detecting Qt framework...")

        for detector in (self._try_pyside6, self._try_pyqt6, self._try_pyqt5):
            try:
                framework, modules = detector()
                self._cache_result(framework, modules)
                logger.info(f"Detected Qt framework: {framework}")
                return framework, modules
            except (ImportError, QtVersionError) as e:
                detector_name = getattr(detector, "__name__", type(detector).__name__)
                logger.debug(f"{detector_name} failed: {e}")

        self._detection_attempted = True
        logger.error("No compatible Qt framework found")
        raise QtFrameworkNotFoundError()

    def _try_pyside6(self) -> tuple[str, QtModuleMap]:
        """Try to import PySide6 and validate version."""
        try:
            qt_package = importlib.import_module("PySide6")
            qt_core = importlib.import_module("PySide6.QtCore")
            qt_widgets = importlib.import_module("PySide6.QtWidgets")

            version = str(getattr(qt_package, "__version__", "0.0.0"))
            self._validate_version("PySide6", version, self.MIN_VERSIONS["PySide6"])

            modules: QtModuleMap = {
                "QObject": cast(QtObjectType, qt_core.QObject),
                "pyqtSignal": cast(QtSignalFactory, qt_core.Signal),
                "QApplication": cast(QtApplicationType, qt_widgets.QApplication),
                "QWidget": cast(QtWidgetType, qt_widgets.QWidget),
                "version": version,
            }

            return "PySide6", modules

        except ImportError as e:
            raise ImportError(f"PySide6 not available: {e}") from e

    def _try_pyqt6(self) -> tuple[str, QtModuleMap]:
        """Try to import PyQt6 and validate version."""
        try:
            qt_core = importlib.import_module("PyQt6.QtCore")
            qt_widgets = importlib.import_module("PyQt6.QtWidgets")

            version = str(getattr(qt_core, "QT_VERSION_STR", "0.0.0"))
            self._validate_version("PyQt6", version, self.MIN_VERSIONS["PyQt6"])

            modules: QtModuleMap = {
                "QObject": cast(QtObjectType, qt_core.QObject),
                "pyqtSignal": cast(QtSignalFactory, qt_core.pyqtSignal),
                "QApplication": cast(QtApplicationType, qt_widgets.QApplication),
                "QWidget": cast(QtWidgetType, qt_widgets.QWidget),
                "version": version,
            }

            return "PyQt6", modules

        except ImportError as e:
            raise ImportError(f"PyQt6 not available: {e}") from e

    def _try_pyqt5(self) -> tuple[str, QtModuleMap]:
        """Try to import PyQt5 and validate version."""
        try:
            qt_core = importlib.import_module("PyQt5.QtCore")
            qt_widgets = importlib.import_module("PyQt5.QtWidgets")

            version = str(getattr(qt_core, "QT_VERSION_STR", "0.0.0"))
            self._validate_version("PyQt5", version, self.MIN_VERSIONS["PyQt5"])

            modules: QtModuleMap = {
                "QObject": cast(QtObjectType, qt_core.QObject),
                "pyqtSignal": cast(QtSignalFactory, qt_core.pyqtSignal),
                "QApplication": cast(QtApplicationType, qt_widgets.QApplication),
                "QWidget": cast(QtWidgetType, qt_widgets.QWidget),
                "version": version,
            }

            return "PyQt5", modules

        except ImportError as e:
            raise ImportError(f"PyQt5 not available: {e}") from e

    def _validate_version(
        self, framework: str, current_version: str, required_version: str
    ) -> None:
        """Validate Qt framework version meets minimum requirements."""
        try:
            current_parts = [int(x) for x in current_version.split(".")]
            required_parts = [int(x) for x in required_version.split(".")]

            max_len = max(len(current_parts), len(required_parts))
            current_parts.extend([0] * (max_len - len(current_parts)))
            required_parts.extend([0] * (max_len - len(required_parts)))

            if current_parts < required_parts:
                raise QtVersionError(framework, current_version, required_version)

        except ValueError as e:
            logger.warning(f"Could not parse version {current_version}: {e}")

    def _cache_result(self, framework: str, modules: QtModuleMap) -> None:
        """Cache detection result."""
        self._cached_framework = framework
        self._cached_modules = modules
        self._detection_attempted = True

    def get_cached_framework(self) -> str | None:
        """Get cached framework name without triggering detection."""
        return self._cached_framework

    def get_cached_modules(self) -> QtModuleMap | None:
        """Get cached modules without triggering detection."""
        return self._cached_modules

    def clear_cache(self) -> None:
        """Clear cached detection results."""
        self._cached_framework = None
        self._cached_modules = None
        self._detection_attempted = False

    def is_qt_available(self) -> bool:
        """Check if any Qt framework is available without raising exceptions."""
        try:
            self.detect_qt_framework()
            return True
        except (QtFrameworkNotFoundError, QtVersionError):
            return False


_qt_detector = QtDetector()


def detect_qt_framework(force_redetect: bool = False) -> tuple[str, QtModuleMap]:
    """Detect available Qt framework (module-level convenience function)."""
    return _qt_detector.detect_qt_framework(force_redetect)


def is_qt_available() -> bool:
    """Check if any Qt framework is available (module-level convenience function)."""
    return _qt_detector.is_qt_available()


def get_qt_framework_info() -> dict[str, str] | None:
    """Get information about the detected Qt framework."""
    try:
        framework, modules = _qt_detector.detect_qt_framework()
        return {
            "framework": framework,
            "version": modules.get("version", "unknown"),
        }
    except (QtFrameworkNotFoundError, QtVersionError):
        return None


def clear_qt_cache() -> None:
    """Clear Qt detection cache (module-level convenience function)."""
    _qt_detector.clear_cache()
