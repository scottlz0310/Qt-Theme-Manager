#!/usr/bin/env python3
"""
Main entry point for the theme manager CLI.

This module provides the main entry point for CLI operations only,
ensuring complete separation from GUI functionality. Optimized for
library-only architecture with minimal dependencies and clean error handling.
"""

import sys
from typing import Optional

from .cli.themectl import main as cli_main
from .config.logging_config import get_logger, setup_logging

# Setup logging configuration
setup_logging(log_level="WARNING", enable_file_logging=False)

# Configure optimized logging for main entry point
logger = get_logger(__name__)

# Ensure clean CLI-only operation
__all__ = ["main"]


def main() -> Optional[int]:
    """
    Main entry point for CLI operations only.

    This function serves as the primary entry point for the qt-theme-manager
    command-line interface, providing theme management capabilities without
    any GUI dependencies. Optimized for library-only architecture.

    Returns:
        Optional[int]: Exit code (0 for success, 1 for error, None for help)

    Raises:
        SystemExit: On critical errors or user interruption
    """
    try:
        result = cli_main()
        return result if result is not None else 0
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except ImportError as e:
        logger.error(f"Import error - missing dependency: {e}")
        logger.error(
            "Please ensure Qt framework is installed: "
            "pip install PySide6 (recommended) or PyQt6 or PyQt5"
        )
        return 1
    except Exception as e:
        logger.error(f"Unexpected error in main entry point: {e}")
        logger.debug("Full traceback:", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    if exit_code is not None:
        sys.exit(exit_code)
