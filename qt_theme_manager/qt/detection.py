"""
Qt framework detection module.
Handles automatic detection of available Qt frameworks with proper error handling.
"""

from typing import Any, Dict, Optional, Tuple

from ..config.logging_config import get_logger

logger = get_logger(__name__)


class QtFrameworkNotFoundError(ImportError):
    """Qt framework not found error with installation guidance."""

    def __init__(self, message: Optional[str] = None):
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

    def __init__(
        self, framework: str, current_version: str, required_version: str
    ):
        message = (
            f"{framework} version {current_version} is not supported. "
            f"Minimum required version: {required_version}"
        )
        super().__init__(message)


class QtDetector:
    """Qt framework detector with caching and version validation."""

    # Minimum version requirements for each framework
    MIN_VERSIONS = {"PySide6": "6.0.0", "PyQt6": "6.2.0", "PyQt5": "5.15.0"}

    def __init__(self):
        self._cached_framework: Optional[str] = None
        self._cached_modules: Optional[Dict[str, Any]] = None
        self._detection_attempted = False

    def detect_qt_framework(
        self, force_redetect: bool = False
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Detect available Qt framework with caching.

        Args:
            force_redetect: Force re-detection even if cached result exists

        Returns:
            Tuple of (framework_name, modules_dict)

        Raises:
            QtFrameworkNotFoundError: If no Qt framework is available
            QtVersionError: If Qt framework version is too old
        """
        if (
            not force_redetect
            and self._cached_framework
            and self._cached_modules
        ):
            logger.debug(
                f"Using cached Qt framework: {self._cached_framework}"
            )
            return self._cached_framework, self._cached_modules

        logger.debug("Detecting Qt framework...")

        # Try PySide6 first (recommended)
        try:
            framework, modules = self._try_pyside6()
            self._cache_result(framework, modules)
            logger.info(f"Detected Qt framework: {framework}")
            return framework, modules
        except (ImportError, QtVersionError) as e:
            logger.debug(f"PySide6 detection failed: {e}")

        # Try PyQt6 second
        try:
            framework, modules = self._try_pyqt6()
            self._cache_result(framework, modules)
            logger.info(f"Detected Qt framework: {framework}")
            return framework, modules
        except (ImportError, QtVersionError) as e:
            logger.debug(f"PyQt6 detection failed: {e}")

        # Try PyQt5 last
        try:
            framework, modules = self._try_pyqt5()
            self._cache_result(framework, modules)
            logger.info(f"Detected Qt framework: {framework}")
            return framework, modules
        except (ImportError, QtVersionError) as e:
            logger.debug(f"PyQt5 detection failed: {e}")

        # No framework found
        self._detection_attempted = True
        logger.error("No compatible Qt framework found")
        raise QtFrameworkNotFoundError()

    def _try_pyside6(self) -> Tuple[str, Dict[str, Any]]:
        """Try to import PySide6 and validate version."""
        try:
            from PySide6 import __version__ as pyside6_version
            from PySide6.QtCore import QObject
            from PySide6.QtCore import Signal as pyqtSignal
            from PySide6.QtWidgets import QApplication, QWidget

            # Validate version
            self._validate_version(
                "PySide6", pyside6_version, self.MIN_VERSIONS["PySide6"]
            )

            modules = {
                "QObject": QObject,
                "pyqtSignal": pyqtSignal,
                "QApplication": QApplication,
                "QWidget": QWidget,
                "version": pyside6_version,
            }

            return "PySide6", modules

        except ImportError as e:
            raise ImportError(f"PySide6 not available: {e}")

    def _try_pyqt6(self) -> Tuple[str, Dict[str, Any]]:
        """Try to import PyQt6 and validate version."""
        try:
            from PyQt6.QtCore import QT_VERSION_STR, QObject, pyqtSignal
            from PyQt6.QtWidgets import QApplication, QWidget

            # Validate version
            self._validate_version(
                "PyQt6", QT_VERSION_STR, self.MIN_VERSIONS["PyQt6"]
            )

            modules = {
                "QObject": QObject,
                "pyqtSignal": pyqtSignal,
                "QApplication": QApplication,
                "QWidget": QWidget,
                "version": QT_VERSION_STR,
            }

            return "PyQt6", modules

        except ImportError as e:
            raise ImportError(f"PyQt6 not available: {e}")

    def _try_pyqt5(self) -> Tuple[str, Dict[str, Any]]:
        """Try to import PyQt5 and validate version."""
        try:
            from PyQt5.QtCore import QT_VERSION_STR, QObject, pyqtSignal
            from PyQt5.QtWidgets import QApplication, QWidget

            # Validate version
            self._validate_version(
                "PyQt5", QT_VERSION_STR, self.MIN_VERSIONS["PyQt5"]
            )

            modules = {
                "QObject": QObject,
                "pyqtSignal": pyqtSignal,
                "QApplication": QApplication,
                "QWidget": QWidget,
                "version": QT_VERSION_STR,
            }

            return "PyQt5", modules

        except ImportError as e:
            raise ImportError(f"PyQt5 not available: {e}")

    def _validate_version(
        self, framework: str, current_version: str, required_version: str
    ) -> None:
        """
        Validate Qt framework version meets minimum requirements.

        Args:
            framework: Framework name
            current_version: Current installed version
            required_version: Minimum required version

        Raises:
            QtVersionError: If version is too old
        """
        try:
            current_parts = [int(x) for x in current_version.split(".")]
            required_parts = [int(x) for x in required_version.split(".")]

            # Pad shorter version with zeros
            max_len = max(len(current_parts), len(required_parts))
            current_parts.extend([0] * (max_len - len(current_parts)))
            required_parts.extend([0] * (max_len - len(required_parts)))

            if current_parts < required_parts:
                raise QtVersionError(
                    framework, current_version, required_version
                )

        except ValueError as e:
            logger.warning(f"Could not parse version {current_version}: {e}")
            # If we can't parse version, assume it's OK

    def _cache_result(self, framework: str, modules: Dict[str, Any]) -> None:
        """Cache detection result."""
        self._cached_framework = framework
        self._cached_modules = modules
        self._detection_attempted = True

    def get_cached_framework(self) -> Optional[str]:
        """Get cached framework name without triggering detection."""
        return self._cached_framework

    def get_cached_modules(self) -> Optional[Dict[str, Any]]:
        """Get cached modules without triggering detection."""
        return self._cached_modules

    def clear_cache(self) -> None:
        """Clear cached detection results."""
        self._cached_framework = None
        self._cached_modules = None
        self._detection_attempted = False

    def is_qt_available(self) -> bool:
        """
        Check if any Qt framework is available without raising exceptions.

        Returns:
            True if Qt framework is available, False otherwise
        """
        try:
            self.detect_qt_framework()
            return True
        except (QtFrameworkNotFoundError, QtVersionError):
            return False


# Global detector instance for caching across the module
_qt_detector = QtDetector()


def detect_qt_framework(
    force_redetect: bool = False,
) -> Tuple[str, Dict[str, Any]]:
    """
    Detect available Qt framework (module-level convenience function).

    Args:
        force_redetect: Force re-detection even if cached result exists

    Returns:
        Tuple of (framework_name, modules_dict)

    Raises:
        QtFrameworkNotFoundError: If no Qt framework is available
        QtVersionError: If Qt framework version is too old
    """
    return _qt_detector.detect_qt_framework(force_redetect)


def is_qt_available() -> bool:
    """
    Check if any Qt framework is available (module-level convenience function).

    Returns:
        True if Qt framework is available, False otherwise
    """
    return _qt_detector.is_qt_available()


def get_qt_framework_info() -> Optional[Dict[str, str]]:
    """
    Get information about the detected Qt framework.

    Returns:
        Dictionary with framework info or None if not detected
    """
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
