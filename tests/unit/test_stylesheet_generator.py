"""
Unit tests for StylesheetGenerator class.
"""

import pytest

from qt_theme_manager.qt.stylesheet import StylesheetGenerator


class TestStylesheetGenerator:
    """Unit tests for StylesheetGenerator class."""

    @pytest.fixture
    def sample_theme_config(self):
        """Sample theme configuration for testing."""
        return {
            "name": "test",
            "display_name": "Test Theme",
            "backgroundColor": "#ffffff",
            "textColor": "#000000",
            "button": {
                "background": "#f0f0f0",
                "text": "#000000",
                "hover": "#e0e0e0",
                "pressed": "#d0d0d0",
                "border": "#cccccc",
            },
            "input": {
                "background": "#ffffff",
                "text": "#000000",
                "border": "#cccccc",
                "focus": "#0078d4",
                "placeholder": "#888888",
            },
            "panel": {
                "background": "#f8f8f8",
                "border": "#ddd",
                "header": {
                    "background": "#e2e8f0",
                    "text": "#2d3748",
                    "border": "#cbd5e0",
                },
            },
        }

    def test_init(self, sample_theme_config):
        """Test StylesheetGenerator initialization."""
        generator = StylesheetGenerator(sample_theme_config)

        assert generator is not None
        assert generator.theme_config == sample_theme_config

    def test_generate_qss_basic(self, sample_theme_config):
        """Test basic QSS generation."""
        generator = StylesheetGenerator(sample_theme_config)

        qss = generator.generate_qss()

        assert isinstance(qss, str)
        assert len(qss) > 0
        assert "QWidget" in qss
        assert "#ffffff" in qss  # backgroundColor
        assert "#000000" in qss  # textColor

    def test_generate_qss_empty_theme(self):
        """Test QSS generation with minimal theme."""
        minimal_config = {
            "name": "minimal",
            "display_name": "Minimal",
            "backgroundColor": "#ffffff",
            "textColor": "#000000",
        }
        generator = StylesheetGenerator(minimal_config)

        qss = generator.generate_qss()

        assert isinstance(qss, str)
        assert len(qss) > 0
        assert "QWidget" in qss

    def test_generate_base_styles(self, sample_theme_config):
        """Test base styles generation."""
        generator = StylesheetGenerator(sample_theme_config)

        base_styles = generator._generate_base_styles()

        assert "QWidget" in base_styles
        assert "#ffffff" in base_styles
        assert "#000000" in base_styles

    def test_generate_button_styles(self, sample_theme_config):
        """Test button styles generation."""
        generator = StylesheetGenerator(sample_theme_config)

        button_styles = generator._generate_button_styles()

        assert "QPushButton" in button_styles
        assert "#f0f0f0" in button_styles  # button background

    def test_generate_input_styles(self, sample_theme_config):
        """Test input styles generation."""
        generator = StylesheetGenerator(sample_theme_config)

        input_styles = generator._generate_input_styles()

        assert "QLineEdit" in input_styles
        assert "QTextEdit" in input_styles
        assert "#0078d4" in input_styles  # focus color

    def test_generate_panel_styles(self, sample_theme_config):
        """Test panel styles generation."""
        generator = StylesheetGenerator(sample_theme_config)

        panel_styles = generator._generate_panel_styles()

        assert "QGroupBox" in panel_styles
        assert "#f8f8f8" in panel_styles  # panel background

    def test_generate_toolbar_styles(self, sample_theme_config):
        """Test toolbar styles generation."""
        generator = StylesheetGenerator(sample_theme_config)

        toolbar_styles = generator._generate_toolbar_styles()

        assert "QToolBar" in toolbar_styles
        assert "QToolButton" in toolbar_styles

    def test_generate_status_styles(self, sample_theme_config):
        """Test status bar styles generation."""
        generator = StylesheetGenerator(sample_theme_config)

        status_styles = generator._generate_status_styles()

        assert "QStatusBar" in status_styles

    def test_generate_text_styles(self, sample_theme_config):
        """Test text styles generation."""
        generator = StylesheetGenerator(sample_theme_config)

        text_styles = generator._generate_text_styles()

        assert "QLabel" in text_styles

    def test_generate_widget_qss_button(self, sample_theme_config):
        """Test widget-specific QSS generation for buttons."""
        generator = StylesheetGenerator(sample_theme_config)

        button_qss = generator.generate_widget_qss("button")

        assert "QPushButton" in button_qss
        assert "#f0f0f0" in button_qss

    def test_generate_widget_qss_invalid_type(self, sample_theme_config):
        """Test widget-specific QSS generation with invalid type."""
        generator = StylesheetGenerator(sample_theme_config)

        with pytest.raises(ValueError, match="Unsupported widget type"):
            generator.generate_widget_qss("invalid_type")

    def test_validate_theme_config_valid(self):
        """Test theme configuration validation with valid config."""
        valid_config = {
            "name": "test",
            "display_name": "Test Theme",
            "backgroundColor": "#ffffff",
            "textColor": "#000000",
        }

        result = StylesheetGenerator.validate_theme_config(valid_config)

        assert result is True

    def test_validate_theme_config_missing_required(self):
        """Test theme configuration validation with missing required fields."""
        invalid_config = {
            "name": "test",
            # Missing display_name, backgroundColor, textColor
        }

        result = StylesheetGenerator.validate_theme_config(invalid_config)

        assert result is False

    def test_validate_theme_config_empty(self):
        """Test theme configuration validation with empty config."""
        result = StylesheetGenerator.validate_theme_config({})

        assert result is False


class TestStylesheetGeneratorAdvanced:
    """Advanced tests for StylesheetGenerator."""

    @pytest.fixture
    def complex_theme_config(self):
        """Complex theme configuration for advanced testing."""
        return {
            "name": "complex",
            "display_name": "Complex Theme",
            "backgroundColor": "#2d3748",
            "textColor": "#ffffff",
            "button": {
                "background": "#4a5568",
                "text": "#ffffff",
                "hover": "#0078d4",
                "pressed": "#2c5282",
                "border": "#718096",
            },
            "input": {
                "background": "#1a202c",
                "text": "#ffffff",
                "border": "#4a5568",
                "focus": "#0078d4",
                "placeholder": "#a0aec0",
            },
            "panel": {
                "background": "#2d3748",
                "border": "#4a5568",
                "header": {
                    "background": "#4a5568",
                    "text": "#ffffff",
                    "border": "#718096",
                },
                "zebra": {"alternate": "#374151"},
            },
            "toolbar": {
                "background": "#1a202c",
                "text": "#ffffff",
                "border": "#4a5568",
                "button": {
                    "background": "#2d3748",
                    "text": "#ffffff",
                    "hover": "#0078d4",
                    "pressed": "#2c5282",
                },
            },
            "status": {
                "background": "#1a202c",
                "text": "#a0aec0",
                "border": "#4a5568",
            },
            "text": {
                "primary": "#ffffff",
                "secondary": "#e2e8f0",
                "muted": "#a0aec0",
                "heading": "#ffffff",
                "link": "#63b3ed",
                "success": "#68d391",
                "warning": "#fbd38d",
                "error": "#fc8181",
            },
        }

    def test_generate_complex_qss(self, complex_theme_config):
        """Test QSS generation with complex theme configuration."""
        generator = StylesheetGenerator(complex_theme_config)

        qss = generator.generate_qss()

        assert isinstance(qss, str)
        assert len(qss) > 1000  # Complex theme should generate substantial CSS
        assert "#2d3748" in qss  # backgroundColor
        assert "#ffffff" in qss  # textColor
        assert "#0078d4" in qss  # hover colors

    def test_generate_with_zebra_styles(self, complex_theme_config):
        """Test QSS generation with zebra striping."""
        generator = StylesheetGenerator(complex_theme_config)

        panel_styles = generator._generate_panel_styles()

        assert "alternate-background-color" in panel_styles
        assert "#374151" in panel_styles  # zebra alternate color

    def test_generate_with_all_text_styles(self, complex_theme_config):
        """Test QSS generation with all text style variants."""
        generator = StylesheetGenerator(complex_theme_config)

        text_styles = generator._generate_text_styles()

        # Check all text style classes are present
        assert 'class="secondary"' in text_styles
        assert 'class="muted"' in text_styles
        assert 'class="heading"' in text_styles
        assert 'class="link"' in text_styles
        assert 'class="success"' in text_styles
        assert 'class="warning"' in text_styles
        assert 'class="error"' in text_styles


class TestStylesheetGeneratorErrorHandling:
    """Error handling tests for StylesheetGenerator."""

    def test_handle_missing_optional_sections(self):
        """Test handling of missing optional configuration sections."""
        minimal_config = {
            "name": "minimal",
            "display_name": "Minimal Theme",
            "backgroundColor": "#ffffff",
            "textColor": "#000000",
            # Missing button, input, panel, etc. sections
        }

        generator = StylesheetGenerator(minimal_config)
        qss = generator.generate_qss()

        # Should not raise exception and should generate basic styles
        assert isinstance(qss, str)
        assert len(qss) > 0
        assert "QWidget" in qss

    def test_handle_partial_button_config(self):
        """Test handling of partial button configuration."""
        partial_config = {
            "name": "partial",
            "display_name": "Partial Theme",
            "backgroundColor": "#ffffff",
            "textColor": "#000000",
            "button": {
                "background": "#f0f0f0"
                # Missing text, hover, pressed, border
            },
        }

        generator = StylesheetGenerator(partial_config)
        button_styles = generator._generate_button_styles()

        assert "QPushButton" in button_styles
        assert "#f0f0f0" in button_styles

    def test_handle_empty_sections(self):
        """Test handling of empty configuration sections."""
        empty_sections_config = {
            "name": "empty",
            "display_name": "Empty Sections Theme",
            "backgroundColor": "#ffffff",
            "textColor": "#000000",
            "button": {},
            "input": {},
            "panel": {},
        }

        generator = StylesheetGenerator(empty_sections_config)
        qss = generator.generate_qss()

        # Should not raise exception
        assert isinstance(qss, str)
        assert len(qss) > 0


class TestStylesheetGeneratorIntegration:
    """Integration tests for StylesheetGenerator."""

    def test_full_theme_generation_workflow(self):
        """Test complete theme generation workflow."""
        theme_config = {
            "name": "integration_test",
            "display_name": "Integration Test Theme",
            "backgroundColor": "#f7fafc",
            "textColor": "#2d3748",
            "button": {
                "background": "#ffffff",
                "text": "#2d3748",
                "hover": "#0078d4",
                "pressed": "#2c5282",
                "border": "#e2e8f0",
            },
            "input": {
                "background": "#ffffff",
                "text": "#2d3748",
                "border": "#e2e8f0",
                "focus": "#0078d4",
                "placeholder": "#a0aec0",
            },
        }

        # Test initialization
        generator = StylesheetGenerator(theme_config)
        assert generator.theme_config == theme_config

        # Test validation
        assert StylesheetGenerator.validate_theme_config(theme_config) is True

        # Test full QSS generation
        qss = generator.generate_qss()
        assert isinstance(qss, str)
        assert len(qss) > 0

        # Test widget-specific generation
        button_qss = generator.generate_widget_qss("button")
        assert "QPushButton" in button_qss

        input_qss = generator.generate_widget_qss("input")
        assert "QLineEdit" in input_qss

    def test_theme_consistency_check(self):
        """Test that generated QSS is consistent with theme configuration."""
        theme_config = {
            "name": "consistency_test",
            "display_name": "Consistency Test",
            "backgroundColor": "#123456",
            "textColor": "#abcdef",
            "button": {
                "background": "#fedcba",
                "text": "#654321",
                "hover": "#111111",
                "pressed": "#222222",
                "border": "#333333",
            },
        }

        generator = StylesheetGenerator(theme_config)
        qss = generator.generate_qss()

        # Check that all specified colors appear in the generated QSS
        assert "#123456" in qss  # backgroundColor
        assert "#abcdef" in qss  # textColor
        assert "#fedcba" in qss  # button background
        assert "#654321" in qss  # button text
        assert "#111111" in qss  # button hover
        assert "#222222" in qss  # button pressed
        assert "#333333" in qss  # button border
