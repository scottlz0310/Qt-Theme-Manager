"""
Theme controller module.
Handles theme switching, application, and state management.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

from ..config.logging_config import get_logger
from .detection import (
    QtFrameworkNotFoundError,
    QtVersionError,
    detect_qt_framework,
)
from .loader import ThemeLoader
from .stylesheet import StylesheetGenerator
from .types import (
    QApplicationProtocol,
    QtApplicationType,
    QtModuleMap,
    QtObjectType,
    QtSignalFactory,
    QtWidgetType,
    QWidgetProtocol,
)

logger = get_logger(__name__)


class _MockQObject:
    def __init__(self) -> None:
        pass


class _MockQWidget(_MockQObject):
    def setStyleSheet(self, stylesheet: str) -> None:
        pass


class _MockQApplication:
    @staticmethod
    def instance() -> Optional["_MockQApplication"]:
        return None

    def setStyleSheet(self, stylesheet: str) -> None:
        pass


class _MockSignal:
    def connect(
        self,
        __slot: Any,
        *,
        type: int | None = None,  # noqa: A003 - Qt naming
    ) -> None:
        return None

    def emit(self, *args: Any, **kwargs: Any) -> None:
        return None


def _mock_signal(*args: Any, **kwargs: Any) -> _MockSignal:
    return _MockSignal()


qt_available = False
qt_framework = "None"
qt_modules: QtModuleMap | None = None

QObject: QtObjectType = _MockQObject
QWidget: QtWidgetType = _MockQWidget
QApplication: QtApplicationType = _MockQApplication
pyqtSignal: QtSignalFactory = _mock_signal

try:
    qt_framework, qt_modules = detect_qt_framework()
    qt_available = True

    QObject = qt_modules["QObject"]
    QWidget = qt_modules["QWidget"]
    QApplication = qt_modules["QApplication"]
    pyqtSignal = qt_modules["pyqtSignal"]

    logger.info(f"Qt framework detected: {qt_framework} v{qt_modules['version']}")
except (QtFrameworkNotFoundError, QtVersionError) as e:
    logger.warning(f"Qt framework not available: {e}")


class _ThemeControllerCore:
    loader: ThemeLoader
    current_theme_name: str
    current_stylesheet: str

    def _init_core(self, config_path: str | Path | None = None) -> None:
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
                raise ValueError(
                    f"Theme configuration not found: {self.current_theme_name}"
                )

        except Exception as e:
            logger.warning(f"Failed to load current theme: {e}")
            self._load_fallback_theme()

    def _load_fallback_theme(self) -> None:
        """Load fallback theme when current theme fails."""
        try:
            # Create minimal fallback
            self.current_theme_name = "fallback"
            self.current_stylesheet = ""
        except Exception as e:
            logger.error(f"Failed to load fallback theme: {e}")
            self.current_theme_name = "error"
            self.current_stylesheet = ""

    def get_available_themes(self) -> dict[str, dict[str, Any]]:
        """Get all available themes."""
        return self.loader.get_available_themes()

    def get_current_theme_name(self) -> str:
        """Get current theme name."""
        return self.current_theme_name

    def get_current_stylesheet(self) -> str:
        """Get current stylesheet."""
        return self.current_stylesheet

    def set_theme(self, theme_name: str, save_settings: bool = True) -> bool:
        """
        Set and apply a theme.

        Args:
            theme_name: Name of the theme to set
            save_settings: Whether to save the setting

        Returns:
            True if theme was set successfully, False otherwise
        """
        try:
            # Validate theme configuration
            theme_config = self.loader.get_theme_config(theme_name)
            if not theme_config:
                logger.error(f"Theme not found: {theme_name}")
                return False

            # Validate theme configuration
            if not StylesheetGenerator.validate_theme_config(theme_config):
                logger.error(f"Invalid theme configuration: {theme_name}")
                return False

            # Generate stylesheet
            generator = StylesheetGenerator(theme_config)
            self.current_stylesheet = generator.generate_qss()
            self.current_theme_name = theme_name

            # Save settings if requested
            if save_settings:
                self.loader.update_current_theme(theme_name)

            logger.info(f"Theme set successfully: {theme_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to set theme {theme_name}: {e}")
            return False

    def apply_theme_to_widget(self, widget: QWidgetProtocol) -> bool:
        """
        Apply current theme to a specific widget.

        Args:
            widget: Widget to apply theme to

        Returns:
            True if theme was applied successfully, False otherwise
        """
        try:
            if not qt_available:
                logger.warning("Qt framework not available")
                return False

            if not self.current_stylesheet:
                logger.warning("No current stylesheet to apply")
                return False

            widget.setStyleSheet(self.current_stylesheet)
            logger.debug(f"Theme applied to widget: {type(widget).__name__}")
            return True

        except Exception as e:
            logger.error(f"Failed to apply theme to widget: {e}")
            return False

    def apply_theme_to_application(
        self, app: QApplicationProtocol | None = None
    ) -> bool:
        """
        Apply current theme to the entire application.

        Args:
            app: QApplication instance (auto-detected if None)

        Returns:
            True if theme was applied successfully, False otherwise
        """
        try:
            if not self.current_stylesheet:
                logger.warning("No current stylesheet to apply")
                return False

            if app is None:
                app = QApplication.instance()

            if app is None:
                logger.error("No QApplication instance found")
                return False

            app.setStyleSheet(self.current_stylesheet)
            logger.info("Theme applied to application")
            return True

        except Exception as e:
            logger.error(f"Failed to apply theme to application: {e}")
            return False

    def export_qss(
        self, output_path: str | Path, theme_name: str | None = None
    ) -> bool:
        """
        Export current theme as QSS file.

        Args:
            output_path: Path to output QSS file
            theme_name: Theme name to export (current if None)

        Returns:
            True if export was successful, False otherwise
        """
        try:
            if theme_name is None:
                theme_name = self.current_theme_name

            theme_config = self.loader.get_theme_config(theme_name)
            if not theme_config:
                logger.error(f"Theme not found: {theme_name}")
                return False

            generator = StylesheetGenerator(theme_config)
            qss_content = generator.generate_qss()

            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(qss_content)

            logger.info(f"Theme exported to: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export theme: {e}")
            return False

    def reload_themes(self) -> bool:
        """
        Reload all themes from configuration.

        Returns:
            True if reload was successful, False otherwise
        """
        try:
            self.loader.reload_themes()
            self._load_current_theme()
            logger.info("Themes reloaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to reload themes: {e}")
            return False


if TYPE_CHECKING:

    class ThemeController(_ThemeControllerCore):
        """Main controller for theme management and application."""

        def __init__(self, config_path: str | Path | None = None) -> None:
            self._init_core(config_path)

else:

    class ThemeController(QObject, _ThemeControllerCore):
        """Main controller for theme management and application."""

        def __init__(self, config_path: str | Path | None = None) -> None:
            # Initialize Qt parent class if available
            try:
                super().__init__()  # type: ignore[misc]
            except AttributeError:
                pass
            except Exception:  # nosec B110
                # Handle case where Qt is not properly initialized
                # This is intentional - we want to continue even if Qt init fails
                pass

            self._init_core(config_path)


def apply_theme_to_widget(
    widget: QWidgetProtocol,
    theme_name: str | None = None,
    config_path: str | Path | None = None,
) -> bool:
    """
    Standalone function to apply theme to a widget.

    Args:
        widget: Widget to apply theme to
        theme_name: Theme name to apply (auto-detected if None)
        config_path: Path to theme configuration file

    Returns:
        True if theme was applied successfully, False otherwise
    """
    try:
        if not qt_available:
            logger.warning("Qt framework not available")
            return False

        controller = ThemeController(config_path)
        if theme_name:
            controller.set_theme(theme_name, save_settings=False)
        return controller.apply_theme_to_widget(widget)
    except Exception as e:
        logger.error(f"Failed to apply theme to widget: {e}")
        return False


def apply_theme_to_application(
    app: QApplicationProtocol | None = None,
    theme_name: str | None = None,
    config_path: str | Path | None = None,
) -> bool:
    """
    Standalone function to apply theme to application.

    Args:
        app: QApplication instance (auto-detected if None)
        theme_name: Theme name to apply (auto-detected if None)
        config_path: Path to theme configuration file

    Returns:
        True if theme was applied successfully, False otherwise
    """
    try:
        controller = ThemeController(config_path)
        if theme_name:
            controller.set_theme(theme_name, save_settings=False)
        return controller.apply_theme_to_application(app)
    except Exception as e:
        logger.error(f"Failed to apply theme to application: {e}")
        return False
