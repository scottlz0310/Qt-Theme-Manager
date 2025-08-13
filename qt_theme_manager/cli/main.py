#!/usr/bin/env python3
"""
ThemeManager CLI main entry point.

This module provides the main entry point for the theme manager CLI,
handling command-line operations for theme management without GUI dependencies.
Optimized for library-only architecture with clean separation of concerns
and minimal resource usage.
"""

import sys
from typing import Optional

from ..config.logging_config import get_logger, setup_logging
from .themectl import main as themectl_main

# Configure optimized logging for CLI operations
setup_logging(log_level="WARNING", enable_file_logging=False)

logger = get_logger(__name__)

# Ensure clean CLI-only exports
__all__ = ["main"]


def main() -> Optional[int]:
    """
    Main entry point for theme-manager CLI command.

    This function provides the primary CLI interface for theme management
    operations, ensuring clean error handling and proper exit codes.
    Optimized for library-only architecture with comprehensive error handling.

    Returns:
        Optional[int]: Exit code (0 for success, 1 for error, None for help)

    Raises:
        SystemExit: On critical errors requiring immediate termination
    """
    try:
        result = themectl_main()
        return result if result is not None else 0
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except ImportError as e:
        logger.error(f"Import error - missing dependency: {e}")
        logger.error(
            "Please install a Qt framework: "
            "pip install PySide6 (recommended) or PyQt6 or PyQt5"
        )
        return 1
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        return 1


if __name__ == "__main__":  # pragma: no cover
    exit_code = main()  # pragma: no cover
    if exit_code is not None:  # pragma: no cover
        sys.exit(exit_code)  # pragma: no cover
