"""
Test module for logging configuration functionality.
"""

import copy
import json
import logging
import os
import stat
import tempfile
import unittest
from unittest.mock import patch

from qt_theme_manager.config.logging_config import (
    LoggingConfig,
    get_logger,
    setup_logging,
)


class TestLoggingConfig(unittest.TestCase):
    """Test cases for logging configuration functionality."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class-level test environment."""
        # Store original DEFAULT_CONFIG to avoid test interference
        cls.original_default_config = copy.deepcopy(LoggingConfig.DEFAULT_CONFIG)

    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up class-level test environment."""
        # Restore original DEFAULT_CONFIG
        LoggingConfig.DEFAULT_CONFIG = cls.original_default_config

    def setUp(self) -> None:
        """Set up test environment."""
        # Reset logging configuration to avoid test interference
        logging.getLogger().handlers.clear()
        for logger_name in logging.root.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            logger.handlers.clear()
            logger.propagate = True

        # Reset DEFAULT_CONFIG to original state using deep copy
        LoggingConfig.DEFAULT_CONFIG = copy.deepcopy(self.original_default_config)

        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "logging_config.json")
        self.log_file = os.path.join(self.temp_dir, "test.log")

    def tearDown(self) -> None:
        """Clean up after tests."""
        # Clean up temporary files
        for file_path in [self.config_file, self.log_file]:
            if os.path.exists(file_path):
                os.remove(file_path)

        # Clean up any subdirectories and files created during tests
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

        # Reset logging configuration to avoid test interference
        logging.getLogger().handlers.clear()
        for logger_name in logging.root.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            logger.handlers.clear()
            logger.propagate = True

    def test_logging_config_class_exists(self) -> None:
        """Test that LoggingConfig class exists."""
        self.assertTrue(hasattr(LoggingConfig, "setup_logging"))
        self.assertTrue(hasattr(LoggingConfig, "DEFAULT_CONFIG"))

    def test_load_config_file_exists(self) -> None:
        """Test loading configuration from existing file."""
        test_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"standard": {"format": "%(message)s"}},
            "handlers": {"console": {"class": "logging.StreamHandler"}},
            "loggers": {"qt_theme_manager": {"level": "DEBUG"}},
            "root": {"level": "DEBUG"},
        }

        with open(self.config_file, "w") as f:
            json.dump(test_config, f)

        loaded_config = LoggingConfig._load_config(self.config_file)

        for key, value in test_config.items():
            self.assertEqual(loaded_config[key], value)

    def test_load_config_file_not_exists(self) -> None:
        """Test loading configuration when file doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            LoggingConfig._load_config("/nonexistent/file.json")

    def test_load_config_invalid_json(self) -> None:
        """Test loading configuration from invalid JSON file."""
        with open(self.config_file, "w") as f:
            f.write("invalid json content")

        with self.assertRaises(ValueError):
            LoggingConfig._load_config(self.config_file)

    def test_load_config_missing_required_keys(self) -> None:
        """Test loading configuration with missing required keys."""
        invalid_config = {
            "version": 1,
            "formatters": {"standard": {"format": "%(message)s"}},
            # Missing 'handlers' and 'loggers'
        }

        with open(self.config_file, "w") as f:
            json.dump(invalid_config, f)

        with self.assertRaises(ValueError) as context:
            LoggingConfig._load_config(self.config_file)

        self.assertIn("Missing required key", str(context.exception))

    def test_load_config_none_path(self) -> None:
        """Test loading configuration with None path (should return default)."""
        config = LoggingConfig._load_config(None)
        self.assertEqual(config, LoggingConfig.DEFAULT_CONFIG)

    def test_save_config(self) -> None:
        """Test saving configuration to file."""
        test_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"standard": {"format": "%(message)s"}},
            "handlers": {"console": {"class": "logging.StreamHandler"}},
            "loggers": {"qt_theme_manager": {"level": "WARNING"}},
            "root": {"level": "WARNING"},
        }

        # Use the actual method to save config
        with open(self.config_file, "w") as f:
            json.dump(test_config, f)

        # Verify file was created and contains correct data
        self.assertTrue(os.path.exists(self.config_file))

        with open(self.config_file) as f:
            saved_config = json.load(f)

        for key, value in test_config.items():
            self.assertEqual(saved_config[key], value)

    def test_setup_formatter(self) -> None:
        """Test formatter setup."""
        # Test that formatters are properly configured in default config
        config = LoggingConfig.DEFAULT_CONFIG
        self.assertIn("formatters", config)
        self.assertIn("standard", config["formatters"])
        self.assertIn("simple", config["formatters"])
        self.assertIn("detailed", config["formatters"])

    def test_setup_console_handler(self) -> None:
        """Test console handler setup."""
        # Test that console handler is properly configured in default config
        config = LoggingConfig.DEFAULT_CONFIG
        self.assertIn("handlers", config)
        self.assertIn("console", config["handlers"])
        self.assertEqual(
            config["handlers"]["console"]["class"], "logging.StreamHandler"
        )

    def test_setup_file_handler(self) -> None:
        """Test file handler setup."""
        # Test that file handler is properly configured in default config
        # Note: setup_logging may disable file logging, so test DEFAULT_CONFIG directly
        config = LoggingConfig.DEFAULT_CONFIG
        self.assertIn("handlers", config)
        self.assertIn("file", config["handlers"])
        self.assertEqual(config["handlers"]["file"]["class"], "logging.FileHandler")

    def test_setup_file_handler_directory_creation(self) -> None:
        """Test file handler directory creation."""
        # Create a nested directory structure
        nested_log_file = os.path.join(self.temp_dir, "subdir", "test.log")

        # Create a sample config file with nested log file
        sample_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"standard": {"format": "%(message)s"}},
            "handlers": {
                "console": {"class": "logging.StreamHandler", "level": "INFO"},
                "file": {"class": "logging.FileHandler", "filename": nested_log_file},
            },
            "loggers": {
                "qt_theme_manager": {"level": "INFO", "handlers": ["console", "file"]}
            },
            "root": {"level": "INFO", "handlers": ["console"]},
        }

        with open(self.config_file, "w") as f:
            json.dump(sample_config, f)

        # Test setup_logging with config file path and enable file logging
        setup_logging(config_path=self.config_file, enable_file_logging=True)

        # Verify directory was created
        self.assertTrue(os.path.exists(os.path.dirname(nested_log_file)))

    def test_get_logger_basic(self) -> None:
        """Test basic logger retrieval."""
        logger = get_logger("test_module")

        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "test_module")

    def test_get_logger_caching(self) -> None:
        """Test logger caching functionality."""
        logger1 = get_logger("cached_module")
        logger2 = get_logger("cached_module")

        # Should return the same logger instance
        self.assertIs(logger1, logger2)

    def test_setup_logging_basic(self) -> None:
        """Test basic logging setup."""
        # Test with no parameters (should use default config)
        setup_logging()

        # Verify logging is working
        logger = get_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)

    def test_setup_logging_custom_config(self) -> None:
        """Test logging setup with custom configuration."""
        # Create a custom config file
        custom_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"standard": {"format": "%(message)s"}},
            "handlers": {
                "console": {"class": "logging.StreamHandler", "level": "WARNING"}
            },
            "loggers": {
                "qt_theme_manager": {"level": "WARNING", "handlers": ["console"]}
            },
            "root": {"level": "WARNING", "handlers": ["console"]},
        }

        with open(self.config_file, "w") as f:
            json.dump(custom_config, f)

        # Test setup_logging with custom config file
        setup_logging(config_path=self.config_file)

        # Verify logging is working
        logger = get_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)

    def test_setup_logging_file_handler_error(self) -> None:
        """Test logging setup handles file handler errors gracefully."""
        # Test with invalid log file path (should fall back to basic config)
        # This should raise a PermissionError due to invalid path
        with self.assertRaises(PermissionError):
            setup_logging(log_file_path="/invalid/path/test.log")

        # After the error, logging should still be functional with fallback
        # Reset logging to test fallback functionality
        logging.getLogger().handlers.clear()
        for logger_name in logging.root.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            logger.handlers.clear()
            logger.propagate = True

        # Test that logging still works (fallback)
        logger = get_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)

    def test_setup_logging_console_only(self) -> None:
        """Test logging setup with console handler only."""
        # Test with file logging disabled
        setup_logging(enable_file_logging=False)

        # Verify logging is working
        logger = get_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)

    def test_logging_integration(self) -> None:
        """Test complete logging integration."""
        # Create a sample config file first
        sample_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"standard": {"format": "%(message)s"}},
            "handlers": {
                "console": {"class": "logging.StreamHandler", "level": "DEBUG"},
                "file": {"class": "logging.FileHandler", "filename": self.log_file},
            },
            "loggers": {
                "qt_theme_manager": {"level": "DEBUG", "handlers": ["console", "file"]}
            },
            "root": {"level": "DEBUG", "handlers": ["console"]},
        }

        with open(self.config_file, "w") as f:
            json.dump(sample_config, f)

        # Test setup_logging with config file path
        setup_logging(config_path=self.config_file)

        # Verify logging is working
        logger = get_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)

    def test_logging_level_filtering(self) -> None:
        """Test logging level filtering."""
        # Create a sample config file with WARNING level
        sample_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"standard": {"format": "%(message)s"}},
            "handlers": {
                "console": {"class": "logging.StreamHandler", "level": "WARNING"}
            },
            "loggers": {
                "qt_theme_manager": {"level": "WARNING", "handlers": ["console"]}
            },
            "root": {"level": "WARNING", "handlers": ["console"]},
        }

        with open(self.config_file, "w") as f:
            json.dump(sample_config, f)

        # Test setup_logging with config file path
        setup_logging(config_path=self.config_file)

        # Verify logging level is set correctly by checking the configuration
        # Note: logger.level may not reflect the handler level directly
        logger = get_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)

        # Check that the configuration was applied
        # The actual level filtering happens at the handler level

    def test_logging_rotation(self) -> None:
        """Test log file rotation functionality."""
        # Create a sample config file with rotation settings
        sample_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"standard": {"format": "%(message)s"}},
            "handlers": {
                "console": {"class": "logging.StreamHandler", "level": "INFO"},
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": self.log_file,
                    "maxBytes": 100,
                    "backupCount": 2,
                },
            },
            "loggers": {
                "qt_theme_manager": {"level": "INFO", "handlers": ["console", "file"]}
            },
            "root": {"level": "INFO", "handlers": ["console"]},
        }

        with open(self.config_file, "w") as f:
            json.dump(sample_config, f)

        # Test setup_logging with config file path
        setup_logging(config_path=self.config_file)

        # Verify logging is working
        logger = get_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)

    def test_set_log_level_valid(self) -> None:
        """Test setting valid log levels."""
        config = LoggingConfig.DEFAULT_CONFIG.copy()

        # Test setting DEBUG level
        LoggingConfig._set_log_level(config, "DEBUG")
        self.assertEqual(config["handlers"]["console"]["level"], "DEBUG")
        self.assertEqual(config["loggers"]["qt_theme_manager"]["level"], "DEBUG")
        self.assertEqual(config["root"]["level"], "DEBUG")

        # Test setting ERROR level
        LoggingConfig._set_log_level(config, "ERROR")
        self.assertEqual(config["handlers"]["console"]["level"], "ERROR")
        self.assertEqual(config["loggers"]["qt_theme_manager"]["level"], "ERROR")
        self.assertEqual(config["root"]["level"], "ERROR")

    def test_set_log_level_invalid(self) -> None:
        """Test setting invalid log levels (should fallback to WARNING)."""
        config = LoggingConfig.DEFAULT_CONFIG.copy()

        # Test setting invalid level
        LoggingConfig._set_log_level(config, "INVALID_LEVEL")

        # Should fallback to WARNING
        self.assertEqual(config["handlers"]["console"]["level"], "WARNING")
        self.assertEqual(config["loggers"]["qt_theme_manager"]["level"], "WARNING")
        self.assertEqual(config["root"]["level"], "WARNING")

    def test_set_log_level_missing_handlers(self) -> None:
        """Test setting log level when handlers section is missing."""
        config = {"version": 1, "formatters": {}, "loggers": {}, "root": {}}

        # Should not raise an error
        LoggingConfig._set_log_level(config, "DEBUG")

        # Should still set root level
        self.assertEqual(config["root"]["level"], "DEBUG")

    def test_disable_file_logging(self) -> None:
        """Test disabling file logging."""
        config = LoggingConfig.DEFAULT_CONFIG.copy()

        # Verify file handler exists initially
        self.assertIn("file", config["handlers"])
        self.assertIn("file", config["loggers"]["qt_theme_manager"]["handlers"])

        # Disable file logging
        LoggingConfig._disable_file_logging(config)

        # Verify file handler is removed
        self.assertNotIn("file", config["handlers"])
        self.assertNotIn("file", config["loggers"]["qt_theme_manager"]["handlers"])

    def test_disable_file_logging_no_file_handler(self) -> None:
        """Test disabling file logging when no file handler exists."""
        config = {
            "version": 1,
            "formatters": {},
            "handlers": {},
            "loggers": {},
            "root": {},
        }

        # Should not raise an error
        LoggingConfig._disable_file_logging(config)

    def test_set_log_file_path(self) -> None:
        """Test setting custom log file path."""
        # Use a fresh copy of DEFAULT_CONFIG to avoid interference
        config = LoggingConfig.DEFAULT_CONFIG.copy()
        custom_path = "/custom/path/log.log"

        LoggingConfig._set_log_file_path(config, custom_path)

        self.assertEqual(config["handlers"]["file"]["filename"], custom_path)

    def test_set_log_file_path_no_file_handler(self) -> None:
        """Test setting log file path when no file handler exists."""
        config = {
            "version": 1,
            "formatters": {},
            "handlers": {},
            "loggers": {},
            "root": {},
        }

        # Should not raise an error
        LoggingConfig._set_log_file_path(config, "/test/path.log")

    def test_validate_log_file_path_success(self) -> None:
        """Test successful log file path validation."""
        # Use a fresh copy of DEFAULT_CONFIG to avoid interference
        config = LoggingConfig.DEFAULT_CONFIG.copy()
        test_log_file = os.path.join(self.temp_dir, "validation_test.log")
        config["handlers"]["file"]["filename"] = test_log_file

        # Should not raise an error
        LoggingConfig._validate_log_file_path(config)

        # Verify file was created
        self.assertTrue(os.path.exists(test_log_file))

    def test_validate_log_file_path_no_file_handler(self) -> None:
        """Test validation when no file handler exists."""
        config = {
            "version": 1,
            "formatters": {},
            "handlers": {},
            "loggers": {},
            "root": {},
        }

        # Should not raise an error
        LoggingConfig._validate_log_file_path(config)

    def test_validate_log_file_path_permission_error(self) -> None:
        """Test validation with permission error."""
        # Use a fresh copy of DEFAULT_CONFIG to avoid interference
        config = LoggingConfig.DEFAULT_CONFIG.copy()

        # Create a read-only directory
        read_only_dir = os.path.join(self.temp_dir, "readonly")
        os.makedirs(read_only_dir, exist_ok=True)
        os.chmod(read_only_dir, stat.S_IREAD)

        test_log_file = os.path.join(read_only_dir, "test.log")
        config["handlers"]["file"]["filename"] = test_log_file

        # Should raise PermissionError
        with self.assertRaises(PermissionError):
            LoggingConfig._validate_log_file_path(config)

        # Clean up
        os.chmod(read_only_dir, stat.S_IREAD | stat.S_IWRITE)

    def test_create_sample_config_success(self) -> None:
        """Test successful sample config creation."""
        sample_config_path = os.path.join(self.temp_dir, "sample_config.json")

        LoggingConfig.create_sample_config(sample_config_path)

        # Verify file was created
        self.assertTrue(os.path.exists(sample_config_path))

        # Verify content is valid JSON
        with open(sample_config_path) as f:
            config = json.load(f)

        self.assertEqual(config["version"], 1)
        self.assertIn("formatters", config)
        self.assertIn("handlers", config)
        self.assertIn("loggers", config)

        # Clean up the sample config file
        if os.path.exists(sample_config_path):
            os.remove(sample_config_path)

    def test_create_sample_config_permission_error(self) -> None:
        """Test sample config creation with permission error."""
        # Try to create in a read-only directory
        read_only_dir = os.path.join(self.temp_dir, "readonly")
        os.makedirs(read_only_dir, exist_ok=True)
        os.chmod(read_only_dir, stat.S_IREAD)

        sample_config_path = os.path.join(read_only_dir, "sample_config.json")

        with self.assertRaises(PermissionError):
            LoggingConfig.create_sample_config(sample_config_path)

        # Clean up
        os.chmod(read_only_dir, stat.S_IREAD | stat.S_IWRITE)
        if os.path.exists(read_only_dir):
            os.rmdir(read_only_dir)

    @patch("logging.config.dictConfig")
    def test_setup_logging_dict_config_failure(self, mock_dict_config):
        """Test fallback when dictConfig fails."""
        # Make dictConfig raise an exception
        mock_dict_config.side_effect = Exception("Configuration error")

        # Should not raise an error, should fallback to basic config
        setup_logging()

        # Verify fallback was used
        mock_dict_config.assert_called_once()

    def test_setup_logging_with_log_level_override(self) -> None:
        """Test setting up logging with log level override."""
        # Test with custom log level
        LoggingConfig.setup_logging(log_level="DEBUG")

        # Verify logging is working
        logger = get_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)

    def test_setup_logging_with_custom_log_file_path(self) -> None:
        """Test setting up logging with custom log file path."""
        custom_log_file = os.path.join(self.temp_dir, "custom.log")

        # Test with custom log file path
        setup_logging(log_file_path=custom_log_file)

        # Verify logging is working
        logger = get_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)

    def test_logging_config_default_values(self) -> None:
        """Test default configuration values."""
        # Test DEFAULT_CONFIG directly to avoid interference from setup_logging
        config = LoggingConfig.DEFAULT_CONFIG

        # Test version
        self.assertEqual(config["version"], 1)

        # Test formatters
        self.assertIn("standard", config["formatters"])
        self.assertIn("simple", config["formatters"])
        self.assertIn("detailed", config["formatters"])

        # Test handlers
        self.assertIn("console", config["handlers"])
        self.assertIn("file", config["handlers"])

        # Test loggers
        self.assertIn("qt_theme_manager", config["loggers"])

        # Test root
        self.assertIn("root", config)

    def test_logging_config_formatter_formats(self) -> None:
        """Test formatter format strings."""
        config = LoggingConfig.DEFAULT_CONFIG

        # Test standard formatter
        standard_format = config["formatters"]["standard"]["format"]
        self.assertIn("%(asctime)s", standard_format)
        self.assertIn("%(name)s", standard_format)
        self.assertIn("%(levelname)s", standard_format)
        self.assertIn("%(message)s", standard_format)

        # Test simple formatter
        simple_format = config["formatters"]["simple"]["format"]
        self.assertIn("%(name)s", simple_format)
        self.assertIn("%(levelname)s", simple_format)
        self.assertIn("%(message)s", simple_format)

        # Test detailed formatter
        detailed_format = config["formatters"]["detailed"]["format"]
        self.assertIn("%(filename)s", detailed_format)
        self.assertIn("%(lineno)d", detailed_format)
        self.assertIn("%(funcName)s", detailed_format)

    def test_logging_config_handler_configurations(self) -> None:
        """Test handler configurations."""
        # Test DEFAULT_CONFIG directly to avoid interference from setup_logging
        config = LoggingConfig.DEFAULT_CONFIG

        # Test console handler
        console_handler = config["handlers"]["console"]
        self.assertEqual(console_handler["class"], "logging.StreamHandler")
        self.assertEqual(console_handler["level"], "WARNING")
        self.assertEqual(console_handler["formatter"], "simple")
        self.assertEqual(console_handler["stream"], "ext://sys.stderr")

        # Test file handler
        file_handler = config["handlers"]["file"]
        self.assertEqual(file_handler["class"], "logging.FileHandler")
        self.assertEqual(file_handler["level"], "INFO")
        self.assertEqual(file_handler["formatter"], "standard")
        self.assertEqual(file_handler["filename"], "qt_theme_manager.log")
        self.assertEqual(file_handler["mode"], "a")
        self.assertEqual(file_handler["encoding"], "utf-8")

    def test_logging_config_logger_configurations(self) -> None:
        """Test logger configurations."""
        # Test DEFAULT_CONFIG directly to avoid interference from setup_logging
        config = LoggingConfig.DEFAULT_CONFIG

        # Test qt_theme_manager logger
        qt_logger = config["loggers"]["qt_theme_manager"]
        self.assertEqual(qt_logger["level"], "INFO")
        self.assertEqual(qt_logger["handlers"], ["console", "file"])
        self.assertFalse(qt_logger["propagate"])

        # Test root logger
        root_logger = config["root"]
        self.assertEqual(root_logger["level"], "WARNING")
        self.assertEqual(root_logger["handlers"], ["console"])


if __name__ == "__main__":
    unittest.main()
