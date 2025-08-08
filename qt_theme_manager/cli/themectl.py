"""
CLI module for theme management.

Provides command-line interface for theme operations without GUI dependencies.
Optimized for library-only architecture with comprehensive error handling,
type safety, and minimal resource usage.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Union

from ..config.logging_config import get_logger
from ..qt.controller import ThemeController
from ..qt.loader import ThemeLoader

# Configure optimized logger for CLI operations
logger = get_logger(__name__)

# Ensure clean CLI-only exports
__all__ = ["ThemeCLI", "main"]


class ThemeCLI:
    """
    Command-line interface for theme management.

    Provides a clean, library-focused interface for theme operations
    without any GUI dependencies.
    """

    def __init__(self, config_path: Optional[Union[str, Path]] = None) -> None:
        """
        Initialize ThemeCLI with theme controller and loader.

        Args:
            config_path: Optional path to theme configuration file

        Raises:
            ImportError: If Qt framework is not available
            FileNotFoundError: If config_path is specified but doesn't exist
            PermissionError: If config_path exists but is not readable
        """
        try:
            # Validate config path if provided
            if config_path is not None:
                config_file = Path(config_path)
                if not config_file.exists():
                    raise FileNotFoundError(
                        f"Configuration file not found: {config_path}"
                    )
                if not config_file.is_file():
                    raise ValueError(
                        f"Configuration path is not a file: {config_path}"
                    )

            self.controller = ThemeController(config_path)
            self.loader = ThemeLoader(config_path)

        except ImportError as e:
            logger.error(f"Qt framework not available: {e}")
            logger.error("Please install: pip install PySide6 (recommended)")
            raise
        except (FileNotFoundError, PermissionError, ValueError) as e:
            logger.error(f"Configuration error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize theme CLI: {e}")
            raise

    def list_themes(self) -> None:
        """
        List all available themes with detailed information.

        Displays theme names, display names, descriptions, and marks
        the currently active theme. Optimized for clean CLI output.

        Raises:
            SystemExit: On error with exit code 1
        """
        try:
            themes = self.controller.get_available_themes()
            current_theme = self.controller.get_current_theme_name()

            if not themes:
                print("No themes available.")
                logger.info("No themes found in configuration")
                return

            theme_count = len(themes)
            print(f"Available themes ({theme_count}):")
            print("-" * 50)

            # Sort themes alphabetically for consistent output
            for theme_name in sorted(themes.keys()):
                theme_config = themes[theme_name]
                display_name = theme_config.get("display_name", theme_name)
                description = theme_config.get(
                    "description", "No description available"
                )

                marker = " (current)" if theme_name == current_theme else ""
                print(f"  {theme_name}{marker}")
                print(f"    Display Name: {display_name}")
                print(f"    Description: {description}")
                print()

            logger.info(f"Listed {theme_count} available themes")

        except Exception as e:
            logger.error(f"Error listing themes: {e}")
            sys.exit(1)

    def set_theme(self, theme_name: str) -> None:
        """
        Set active theme by name with comprehensive validation.

        Args:
            theme_name: Name of theme to activate

        Raises:
            SystemExit: On error with exit code 1
        """
        # Input validation
        if not theme_name or not theme_name.strip():
            logger.error("Theme name cannot be empty")
            sys.exit(1)

        theme_name = theme_name.strip()

        try:
            # Validate theme exists
            available_themes = self.controller.get_available_themes()
            if not available_themes:
                logger.error("No themes available")
                sys.exit(1)

            if theme_name not in available_themes:
                available_list = sorted(available_themes.keys())
                logger.error(
                    f"Theme '{theme_name}' not found. "
                    f"Available themes: {', '.join(available_list)}"
                )
                sys.exit(1)

            # Check if already current theme
            current_theme = self.controller.get_current_theme_name()
            if theme_name == current_theme:
                print(f"Theme '{theme_name}' is already active")
                logger.info(f"Theme '{theme_name}' was already active")
                return

            success = self.controller.set_theme(theme_name)

            if success:
                print(f"Theme set to '{theme_name}'")
                logger.info(f"Successfully set theme to '{theme_name}'")
            else:
                logger.error(f"Failed to set theme to '{theme_name}'")
                sys.exit(1)

        except Exception as e:
            logger.error(f"Error setting theme: {e}")
            sys.exit(1)

    def export_qss(self, theme_name: str, output_path: str) -> None:
        """
        Export QSS stylesheet to file with comprehensive validation.

        Args:
            theme_name: Name of theme to export
            output_path: Path to output file

        Raises:
            SystemExit: On error with exit code 1
        """
        # Input validation
        if not theme_name or not theme_name.strip():
            logger.error("Theme name cannot be empty")
            sys.exit(1)

        if not output_path or not output_path.strip():
            logger.error("Output path cannot be empty")
            sys.exit(1)

        theme_name = theme_name.strip()
        output_path = output_path.strip()

        try:
            # Validate theme exists
            available_themes = self.controller.get_available_themes()
            if not available_themes:
                logger.error("No themes available")
                sys.exit(1)

            if theme_name not in available_themes:
                available_list = sorted(available_themes.keys())
                logger.error(
                    f"Theme '{theme_name}' not found. "
                    f"Available themes: {', '.join(available_list)}"
                )
                sys.exit(1)

            # Validate and prepare output path
            output_file = Path(output_path)
            output_dir = output_file.parent

            # Create output directory if it doesn't exist
            if not output_dir.exists():
                try:
                    output_dir.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Created output directory: {output_dir}")
                except PermissionError:
                    logger.error(
                        f"Permission denied creating directory: {output_dir}"
                    )
                    sys.exit(1)

            # Check if output file already exists
            if output_file.exists():
                logger.warning(f"Output file already exists: {output_path}")

            success = self.controller.export_qss(output_path, theme_name)

            if success:
                file_size = (
                    output_file.stat().st_size if output_file.exists() else 0
                )
                print(f"QSS exported to '{output_path}' ({file_size} bytes)")
                logger.info(
                    f"Successfully exported QSS to '{output_path}' "
                    f"({file_size} bytes)"
                )
            else:
                logger.error("Failed to export QSS")
                sys.exit(1)

        except Exception as e:
            logger.error(f"Error exporting QSS: {e}")
            sys.exit(1)

    def show_current(self) -> None:
        """
        Show current theme information with detailed color palette.
        Optimized for clean CLI output with comprehensive theme details.

        Raises:
            SystemExit: On error with exit code 1
        """
        try:
            current_theme = self.controller.get_current_theme_name()
            themes = self.controller.get_available_themes()

            if not current_theme:
                print("No theme currently set.")
                logger.info("No current theme configured")
                return

            if not themes:
                print("No themes available in configuration.")
                logger.warning("No themes found in configuration")
                return

            if current_theme in themes:
                theme_config = themes[current_theme]
                display_name = theme_config.get("display_name", current_theme)
                description = theme_config.get(
                    "description", "No description available"
                )
                version = theme_config.get("version", "Unknown")

                print(f"Current theme: {current_theme}")
                print(f"Display Name: {display_name}")
                print(f"Description: {description}")
                print(f"Version: {version}")

                # Show color palette with enhanced formatting
                print("\nColor Palette:")
                print("-" * 30)
                color_keys = [
                    ("Background", "backgroundColor"),
                    ("Text", "textColor"),
                    ("Primary", "primaryColor"),
                    ("Secondary", "secondaryColor"),
                    ("Accent", "accentColor"),
                    ("Border", "borderColor"),
                    ("Hover", "hoverColor"),
                    ("Selection", "selectionColor"),
                ]

                for display_key, config_key in color_keys:
                    color_value = theme_config.get(config_key, "N/A")
                    print(f"  {display_key:12}: {color_value}")

                # Show additional theme metadata if available
                metadata_keys = ["author", "license", "created", "modified"]
                metadata_found = False

                for key in metadata_keys:
                    if key in theme_config:
                        if not metadata_found:
                            print("\nMetadata:")
                            print("-" * 30)
                            metadata_found = True
                        print(f"  {key.title():12}: {theme_config[key]}")

                logger.info(f"Displayed current theme info: {current_theme}")

            else:
                available_list = sorted(themes.keys()) if themes else []
                print(
                    f"Current theme '{current_theme}' not found in "
                    f"configuration."
                )
                if available_list:
                    print(f"Available themes: {', '.join(available_list)}")
                logger.warning(
                    f"Current theme '{current_theme}' not found. "
                    f"Available: {available_list}"
                )

        except Exception as e:
            logger.error(f"Error showing current theme: {e}")
            sys.exit(1)


def main() -> Optional[int]:
    """
    Main CLI entry point with comprehensive argument parsing.

    Optimized for library-only architecture with clean error handling,
    comprehensive validation, and user-friendly output.

    Returns:
        Optional[int]: Exit code (0 for success, 1 for error, None for help)
    """
    parser = argparse.ArgumentParser(
        description=(
            "Qt Theme Manager CLI - Manage PyQt5/PyQt6/PySide6 application "
            "themes from the command line. Library-only architecture with "
            "zero GUI dependencies."
        ),
        prog="qt-theme-manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  qt-theme-manager list                      # List all available themes
  qt-theme-manager set dark                  # Set theme to 'dark'
  qt-theme-manager current                   # Show current theme info
  qt-theme-manager export dark theme.qss     # Export theme to QSS file
  qt-theme-manager --config custom.json list # Use custom config
  qt-theme-manager --verbose current         # Show detailed output
  qt-theme-manager version                   # Show version information

Supported Qt Frameworks:
  - PySide6 (recommended)
  - PyQt6
  - PyQt5
        """,
    )

    parser.add_argument(
        "--config",
        "-c",
        type=str,
        metavar="PATH",
        help="Path to theme configuration file",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Qt Theme Manager CLI v1.0.0",
        help="Show version information",
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Available commands", metavar="COMMAND"
    )

    # List command
    list_parser = subparsers.add_parser(
        "list", help="List all available themes"
    )

    # Set command
    set_parser = subparsers.add_parser("set", help="Set active theme")
    set_parser.add_argument("theme", help="Theme name to activate")

    # Export command
    export_parser = subparsers.add_parser(
        "export", help="Export theme QSS to file"
    )
    export_parser.add_argument("theme", help="Theme name to export")
    export_parser.add_argument("output", help="Output file path")

    # Current command
    current_parser = subparsers.add_parser(
        "current", help="Show current theme information"
    )

    # Version command
    version_parser = subparsers.add_parser(
        "version", help="Show version information"
    )

    args = parser.parse_args()

    # Configure logging based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    # Handle no command case
    if not args.command:
        parser.print_help()
        return None

    # Handle version command early (no CLI initialization needed)
    if args.command == "version":
        print("Qt Theme Manager CLI v1.0.0")
        print("A comprehensive theme management library for Qt applications")
        print("Library-only architecture with zero GUI dependencies")
        print("Supports: PySide6 (recommended), PyQt6, PyQt5")
        print("Homepage: https://github.com/5t111111/qt-theme-manager")
        return 0

    # Initialize CLI with config path and comprehensive error handling
    try:
        cli = ThemeCLI(args.config)
    except ImportError as e:
        logger.error(f"Qt framework not available: {e}")
        logger.error("Please install: pip install PySide6 (recommended)")
        return 1
    except (FileNotFoundError, PermissionError, ValueError) as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Failed to initialize CLI: {e}")
        logger.debug("Full traceback:", exc_info=True)
        return 1

    # Execute command with comprehensive error handling
    try:
        if args.command == "list":
            cli.list_themes()
        elif args.command == "set":
            cli.set_theme(args.theme)
        elif args.command == "export":
            cli.export_qss(args.theme, args.output)
        elif args.command == "current":
            cli.show_current()
        else:
            parser.print_help()
            return 1

        return 0

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except SystemExit:
        # Re-raise SystemExit to preserve exit codes from CLI methods
        raise
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        logger.debug("Full traceback:", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    if exit_code is not None:
        sys.exit(exit_code)
