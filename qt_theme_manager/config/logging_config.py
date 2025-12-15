"""
Logging configuration module for qt_theme_manager.

Provides centralized logging configuration with external configuration support.
Follows PEP 8 standards with 79-character line limit and comprehensive
type hints and docstrings.
"""

import copy
import json
import logging
import logging.config
import sys
from pathlib import Path
from typing import Any


class LoggingConfig:
    """
    Centralized logging configuration manager.

    Provides methods to configure logging with external configuration files
    and sensible defaults for library usage.
    """

    # Default logging configuration
    DEFAULT_CONFIG: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": ("%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {"format": "%(name)s - %(levelname)s: %(message)s"},
            "detailed": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - "
                    "%(filename)s:%(lineno)d - %(funcName)s - %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "WARNING",
                "formatter": "simple",
                "stream": "ext://sys.stderr",
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "INFO",
                "formatter": "standard",
                "filename": "qt_theme_manager.log",
                "mode": "a",
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "qt_theme_manager": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            }
        },
        "root": {"level": "WARNING", "handlers": ["console"]},
    }

    @classmethod
    def setup_logging(
        cls,
        config_path: str | Path | None = None,
        log_level: str | None = None,
        enable_file_logging: bool = True,
        log_file_path: str | Path | None = None,
    ) -> None:
        """
        Setup logging configuration.

        Args:
            config_path: Path to external logging configuration file (JSON)
            log_level: Override log level (DEBUG, INFO, WARNING, ERROR)
            enable_file_logging: Whether to enable file logging
            log_file_path: Custom path for log file

        Raises:
            FileNotFoundError: If config_path is specified but doesn't exist
            ValueError: If config_path contains invalid JSON
            PermissionError: If log file cannot be created
        """
        config = cls._load_config(config_path)

        # Apply overrides
        if log_level:
            cls._set_log_level(config, log_level.upper())

        if not enable_file_logging:
            cls._disable_file_logging(config)

        if log_file_path:
            cls._set_log_file_path(config, log_file_path)

        # Validate log file path before applying configuration
        if enable_file_logging:
            cls._validate_log_file_path(config)

        # Apply configuration
        try:
            logging.config.dictConfig(config)
        except Exception as e:
            # Fallback to basic configuration if dictConfig fails
            logging.basicConfig(
                level=logging.WARNING,
                format="%(name)s - %(levelname)s: %(message)s",
                stream=sys.stderr,
            )
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to apply logging configuration: {e}")
            logger.info("Using fallback basic logging configuration")

    @classmethod
    def _load_config(cls, config_path: str | Path | None) -> dict[str, Any]:
        """
        Load logging configuration from file or use default.

        Args:
            config_path: Path to configuration file

        Returns:
            Logging configuration dictionary

        Raises:
            FileNotFoundError: If config_path doesn't exist
            ValueError: If config_path contains invalid JSON
        """
        if config_path is None:
            # Use deep copy to avoid mutating DEFAULT_CONFIG via nested dicts
            return copy.deepcopy(cls.DEFAULT_CONFIG)

        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(
                f"Logging configuration file not found: {config_path}"
            )

        try:
            with open(config_file, encoding="utf-8") as f:
                config: dict[str, Any] = json.load(f)

            # Validate required keys
            required_keys = ["version", "formatters", "handlers", "loggers"]
            for key in required_keys:
                if key not in config:
                    raise ValueError(f"Missing required key '{key}' in logging config")

            return config

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in logging configuration: {e}") from e

    @classmethod
    def _set_log_level(cls, config: dict[str, Any], level: str) -> None:
        """
        Set log level in configuration.

        Args:
            config: Logging configuration dictionary
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level not in valid_levels:
            level = "WARNING"

        # Update console handler level
        if "handlers" in config and "console" in config["handlers"]:
            config["handlers"]["console"]["level"] = level

        # Update qt_theme_manager logger level
        if "loggers" in config and "qt_theme_manager" in config["loggers"]:
            config["loggers"]["qt_theme_manager"]["level"] = level

        # Update root logger level
        if "root" in config:
            config["root"]["level"] = level

    @classmethod
    def _disable_file_logging(cls, config: dict[str, Any]) -> None:
        """
        Disable file logging in configuration.

        Args:
            config: Logging configuration dictionary
        """
        # Remove file handler from qt_theme_manager logger
        if (
            "loggers" in config
            and "qt_theme_manager" in config["loggers"]
            and "handlers" in config["loggers"]["qt_theme_manager"]
        ):
            handlers = config["loggers"]["qt_theme_manager"]["handlers"]
            if "file" in handlers:
                handlers.remove("file")

        # Remove file handler definition
        if "handlers" in config and "file" in config["handlers"]:
            del config["handlers"]["file"]

    @classmethod
    def _set_log_file_path(
        cls, config: dict[str, Any], log_file_path: str | Path
    ) -> None:
        """
        Set log file path in configuration.

        Args:
            config: Logging configuration dictionary
            log_file_path: Path to log file
        """
        if (
            "handlers" in config
            and "file" in config["handlers"]
            and "filename" in config["handlers"]["file"]
        ):
            config["handlers"]["file"]["filename"] = str(log_file_path)

    @classmethod
    def _validate_log_file_path(cls, config: dict[str, Any]) -> None:
        """
        Validate that log file can be created.

        Args:
            config: Logging configuration dictionary

        Raises:
            PermissionError: If log file cannot be created
        """
        if (
            "handlers" not in config
            or "file" not in config["handlers"]
            or "filename" not in config["handlers"]["file"]
        ):
            return

        log_file_path = Path(config["handlers"]["file"]["filename"])
        log_dir = log_file_path.parent

        # Create directory if it doesn't exist
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise PermissionError(f"Cannot create log directory: {log_dir}") from e

        # Test if we can write to the log file
        try:
            # Try to create/touch the log file
            log_file_path.touch(exist_ok=True)

            # Test write permission
            with open(log_file_path, "a", encoding="utf-8") as f:
                f.write("")  # Just test if we can write

        except PermissionError as e:
            raise PermissionError(f"Cannot write to log file: {log_file_path}") from e

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get logger instance with proper configuration.

        Args:
            name: Logger name (typically __name__)

        Returns:
            Configured logger instance
        """
        return logging.getLogger(name)

    @classmethod
    def create_sample_config(cls, output_path: str | Path) -> None:
        """
        Create sample logging configuration file.

        Args:
            output_path: Path where to create sample configuration

        Raises:
            PermissionError: If cannot write to output_path
        """
        config_file = Path(output_path)

        try:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(cls.DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)

        except PermissionError as e:
            raise PermissionError(
                f"Cannot write sample config to: {output_path}"
            ) from e


# Convenience function for quick setup
def setup_logging(
    config_path: str | Path | None = None,
    log_level: str | None = None,
    enable_file_logging: bool = True,
    log_file_path: str | Path | None = None,
) -> None:
    """
    Convenience function to setup logging.

    Args:
        config_path: Path to external logging configuration file (JSON)
        log_level: Override log level (DEBUG, INFO, WARNING, ERROR)
        enable_file_logging: Whether to enable file logging
        log_file_path: Custom path for log file
    """
    LoggingConfig.setup_logging(
        config_path=config_path,
        log_level=log_level,
        enable_file_logging=enable_file_logging,
        log_file_path=log_file_path,
    )


# Convenience function to get logger
def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get logger.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return LoggingConfig.get_logger(name)
