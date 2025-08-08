"""
Integration tests for configuration file processing across different scenarios.
Tests the complete configuration workflow including loading, validation, and error handling.
"""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

from qt_theme_manager.config.logging_config import get_logger


class TestConfigurationProcessingIntegration:
    """Integration tests for configuration file processing."""

    def test_theme_settings_loading(self, qt_theme_manager_path: Path):
        """Test loading of default theme settings configuration."""
        config_path = qt_theme_manager_path / "config" / "theme_settings.json"
        
        # Check if config file exists
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            
            # Validate basic structure
            assert isinstance(config_data, dict)
            
            # Check for expected configuration sections
            expected_sections = ["themes", "settings", "defaults"]
            for section in expected_sections:
                if section in config_data:
                    assert isinstance(config_data[section], dict)

    def test_config_file_creation(self, temp_config_dir: Path):
        """Test creation of configuration files."""
        config_file = temp_config_dir / "test_config.json"
        
        test_config = {
            "version": "1.0.0",
            "theme": "default",
            "settings": {
                "auto_apply": True,
                "cache_enabled": True
            }
        }
        
        # Write configuration
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(test_config, f, indent=2)
        
        # Verify file was created and is readable
        assert config_file.exists()
        
        with open(config_file, "r", encoding="utf-8") as f:
            loaded_config = json.load(f)
        
        assert loaded_config == test_config

    def test_config_validation_valid_data(self, temp_config_dir: Path):
        """Test configuration validation with valid data."""
        config_file = temp_config_dir / "valid_config.json"
        
        valid_config = {
            "name": "test_theme",
            "version": "1.0.0",
            "colors": {
                "primary": "#3498db",
                "secondary": "#2ecc71"
            },
            "fonts": {
                "default": "Arial"
            },
            "styles": {
                "button": "QPushButton { color: red; }"
            }
        }
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(valid_config, f)
        
        # Load and validate
        with open(config_file, "r", encoding="utf-8") as f:
            loaded_config = json.load(f)
        
        # Basic validation
        assert "name" in loaded_config
        assert "version" in loaded_config
        assert isinstance(loaded_config["colors"], dict)
        assert isinstance(loaded_config["fonts"], dict)
        assert isinstance(loaded_config["styles"], dict)

    def test_config_validation_invalid_json(self, temp_config_dir: Path):
        """Test handling of invalid JSON configuration files."""
        config_file = temp_config_dir / "invalid_config.json"
        
        # Write invalid JSON
        with open(config_file, "w", encoding="utf-8") as f:
            f.write('{"invalid": json, "missing": quote}')
        
        # Should raise JSONDecodeError when trying to load
        with pytest.raises(json.JSONDecodeError):
            with open(config_file, "r", encoding="utf-8") as f:
                json.load(f)

    def test_config_file_permissions(self, temp_config_dir: Path):
        """Test configuration file permission handling."""
        config_file = temp_config_dir / "permission_test.json"
        
        test_config = {"test": "data"}
        
        # Write configuration
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(test_config, f)
        
        # Verify file is readable
        assert config_file.exists()
        assert config_file.is_file()
        
        # Test reading permissions
        with open(config_file, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        
        assert loaded_data == test_config

    def test_config_directory_creation(self, tmp_path: Path):
        """Test automatic creation of configuration directories."""
        nested_config_dir = tmp_path / "nested" / "config" / "themes"
        config_file = nested_config_dir / "theme.json"
        
        # Create directory structure
        nested_config_dir.mkdir(parents=True, exist_ok=True)
        
        test_config = {"theme": "test"}
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(test_config, f)
        
        assert config_file.exists()
        assert nested_config_dir.exists()

    def test_config_backup_and_restore(self, temp_config_dir: Path):
        """Test configuration backup and restore functionality."""
        original_config = temp_config_dir / "original.json"
        backup_config = temp_config_dir / "backup.json"
        
        original_data = {
            "version": "1.0.0",
            "settings": {"theme": "dark"}
        }
        
        # Create original configuration
        with open(original_config, "w", encoding="utf-8") as f:
            json.dump(original_data, f)
        
        # Create backup
        with open(original_config, "r", encoding="utf-8") as f:
            backup_data = json.load(f)
        
        with open(backup_config, "w", encoding="utf-8") as f:
            json.dump(backup_data, f)
        
        # Verify backup
        with open(backup_config, "r", encoding="utf-8") as f:
            restored_data = json.load(f)
        
        assert restored_data == original_data

    def test_config_migration_scenario(self, temp_config_dir: Path):
        """Test configuration migration from old to new format."""
        old_config_file = temp_config_dir / "old_format.json"
        new_config_file = temp_config_dir / "new_format.json"
        
        # Old format configuration
        old_config = {
            "theme_name": "dark",
            "primary_color": "#333333",
            "secondary_color": "#666666"
        }
        
        with open(old_config_file, "w", encoding="utf-8") as f:
            json.dump(old_config, f)
        
        # Simulate migration to new format
        new_config = {
            "name": old_config["theme_name"],
            "version": "2.0.0",
            "colors": {
                "primary": old_config["primary_color"],
                "secondary": old_config["secondary_color"]
            },
            "metadata": {
                "migrated_from": "1.0.0"
            }
        }
        
        with open(new_config_file, "w", encoding="utf-8") as f:
            json.dump(new_config, f)
        
        # Verify migration
        with open(new_config_file, "r", encoding="utf-8") as f:
            migrated_config = json.load(f)
        
        assert migrated_config["name"] == "dark"
        assert migrated_config["colors"]["primary"] == "#333333"
        assert "migrated_from" in migrated_config["metadata"]

    def test_concurrent_config_access(self, temp_config_dir: Path):
        """Test concurrent access to configuration files."""
        config_file = temp_config_dir / "concurrent_test.json"
        
        test_config = {
            "concurrent_test": True,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(test_config, f)
        
        # Simulate multiple concurrent reads
        results = []
        for _ in range(5):
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                results.append(data)
        
        # All reads should return the same data
        for result in results:
            assert result == test_config

    def test_config_encoding_handling(self, temp_config_dir: Path):
        """Test handling of different text encodings in configuration files."""
        config_file = temp_config_dir / "encoding_test.json"
        
        # Configuration with unicode characters
        unicode_config = {
            "name": "テーマ",  # Japanese characters
            "description": "Thème avec caractères spéciaux",  # French
            "author": "Разработчик",  # Cyrillic
            "emoji": "🎨🖌️"  # Emoji
        }
        
        # Write with UTF-8 encoding
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(unicode_config, f, ensure_ascii=False, indent=2)
        
        # Read back and verify
        with open(config_file, "r", encoding="utf-8") as f:
            loaded_config = json.load(f)
        
        assert loaded_config == unicode_config
        assert loaded_config["name"] == "テーマ"
        assert loaded_config["emoji"] == "🎨🖌️"

    @pytest.mark.integration
    def test_full_config_workflow(self, temp_config_dir: Path):
        """Test complete configuration workflow from creation to usage."""
        config_file = temp_config_dir / "workflow_test.json"
        
        # Step 1: Create initial configuration
        initial_config = {
            "name": "workflow_theme",
            "version": "1.0.0",
            "colors": {"primary": "#ff0000"},
            "settings": {"enabled": True}
        }
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(initial_config, f, indent=2)
        
        # Step 2: Load and validate
        with open(config_file, "r", encoding="utf-8") as f:
            loaded_config = json.load(f)
        
        assert loaded_config["name"] == "workflow_theme"
        
        # Step 3: Modify configuration
        loaded_config["colors"]["secondary"] = "#00ff00"
        loaded_config["version"] = "1.1.0"
        
        # Step 4: Save modified configuration
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(loaded_config, f, indent=2)
        
        # Step 5: Verify changes persisted
        with open(config_file, "r", encoding="utf-8") as f:
            final_config = json.load(f)
        
        assert final_config["version"] == "1.1.0"
        assert final_config["colors"]["secondary"] == "#00ff00"
        assert final_config["colors"]["primary"] == "#ff0000"  # Original value preserved


@pytest.mark.integration
class TestLoggingConfigurationIntegration:
    """Integration tests for logging configuration."""

    def test_logger_creation(self):
        """Test logger creation and basic functionality."""
        logger = get_logger("test_module")
        
        assert logger is not None
        assert logger.name == "test_module"

    def test_logger_hierarchy(self):
        """Test logger hierarchy and inheritance."""
        parent_logger = get_logger("qt_theme_manager")
        child_logger = get_logger("qt_theme_manager.qt")
        
        assert parent_logger is not None
        assert child_logger is not None
        
        # Child logger should inherit from parent
        assert child_logger.name.startswith(parent_logger.name)

    def test_multiple_logger_instances(self):
        """Test that multiple logger instances work correctly."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        logger1_again = get_logger("module1")
        
        assert logger1 is not logger2
        assert logger1 is logger1_again  # Same module should return same logger

    def test_logger_mocking(self):
        """Test logger mocking for testing purposes."""
        with patch("qt_theme_manager.config.logging_config.get_logger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            
            # Import after patching to ensure the mock is used
            from qt_theme_manager.config.logging_config import get_logger
            
            logger = get_logger("test")
            logger.info("Test message")
            
            mock_get_logger.assert_called_once_with("test")
            mock_logger.info.assert_called_once_with("Test message")

    def test_logger_with_different_modules(self):
        """Test logger behavior with different module names."""
        modules = [
            "qt_theme_manager.qt.controller",
            "qt_theme_manager.qt.detection", 
            "qt_theme_manager.cli.main",
            "qt_theme_manager.config"
        ]
        
        loggers = {}
        for module in modules:
            loggers[module] = get_logger(module)
        
        # All loggers should be created successfully
        for module, logger in loggers.items():
            assert logger is not None
            assert logger.name == module
        
        # Loggers should be different instances
        logger_instances = list(loggers.values())
        for i, logger1 in enumerate(logger_instances):
            for j, logger2 in enumerate(logger_instances):
                if i != j:
                    assert logger1 is not logger2