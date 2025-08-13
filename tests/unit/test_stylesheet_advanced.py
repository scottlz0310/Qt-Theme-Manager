"""
Test module for advanced stylesheet functionality.
"""

import unittest
from unittest.mock import patch

from qt_theme_manager.qt.stylesheet import StylesheetGenerator


class TestStylesheetAdvanced(unittest.TestCase):
    """Test cases for advanced stylesheet functionality."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.basic_config = {
            'name': 'test_theme',
            'display_name': 'Test Theme',
            'backgroundColor': '#ffffff',
            'textColor': '#000000'
        }
        
        self.advanced_config = {
            'name': 'advanced_theme',
            'display_name': 'Advanced Theme',
            'backgroundColor': '#1a1a1a',
            'textColor': '#ffffff',
            'primaryColor': '#4a90e2',
            'button': {
                'normal': '#4a90e2',
                'hover': '#5ba0f2',
                'pressed': '#357abd',
                'disabled': '#a0a0a0',
                'border': '#2c5aa0'
            },
            'input': {
                'background': '#2a2a2a',
                'text': '#ffffff',
                'border': '#404040',
                'focus': '#4a90e2',
                'placeholder': '#888888',
                'error': '#e53e3e',
                'success': '#38a169'
            },
            'panel': {
                'background': '#2a2a2a',
                'border': '#404040',
                'header': {
                    'background': '#3a3a3a',
                    'text': '#ffffff',
                    'border': '#505050'
                },
                'zebra': {
                    'alternate': '#323232'
                }
            },
            'menu': {
                'background': '#2a2a2a',
                'text': '#ffffff',
                'border': '#404040',
                'hover': '#3a3a3a',
                'separator': '#505050'
            },
            'progress': {
                'background': '#2a2a2a',
                'bar': '#4a90e2',
                'text': '#ffffff',
                'border': '#404040'
            },
            'scrollbar': {
                'background': '#2a2a2a',
                'handle': '#505050',
                'handle_hover': '#606060',
                'border': '#404040'
            },
            'list': {
                'background': '#2a2a2a',
                'text': '#ffffff',
                'border': '#404040',
                'selection': '#4a90e2',
                'selection_text': '#ffffff'
            },
            'tab': {
                'background': '#2a2a2a',
                'text': '#ffffff',
                'selected': '#4a90e2',
                'selected_text': '#ffffff',
                'border': '#404040'
            }
        }

    def test_advanced_mode_initialization(self) -> None:
        """Test advanced mode initialization."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        
        self.assertTrue(generator.advanced_mode)
        self.assertEqual(generator.theme_config, self.advanced_config)

    def test_basic_mode_initialization(self) -> None:
        """Test basic mode initialization."""
        generator = StylesheetGenerator(self.basic_config, advanced_mode=False)
        
        self.assertFalse(generator.advanced_mode)
        self.assertEqual(generator.theme_config, self.basic_config)

    def test_default_mode_is_basic(self) -> None:
        """Test that default mode is basic."""
        generator = StylesheetGenerator(self.basic_config)
        
        self.assertFalse(generator.advanced_mode)

    def test_generate_qss_basic_mode(self) -> None:
        """Test QSS generation in basic mode."""
        generator = StylesheetGenerator(self.basic_config, advanced_mode=False)
        qss = generator.generate_qss()
        
        # Should contain basic styles
        self.assertIn('QWidget', qss)
        self.assertIn('QPushButton', qss)
        self.assertIn('QLineEdit', qss)
        
        # Should not contain advanced styles
        self.assertNotIn('QCheckBox', qss)
        self.assertNotIn('QRadioButton', qss)
        self.assertNotIn('QTabWidget', qss)

    def test_generate_qss_advanced_mode(self) -> None:
        """Test QSS generation in advanced mode."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Should contain all styles including advanced
        self.assertIn('QWidget', qss)
        self.assertIn('QPushButton', qss)
        self.assertIn('QLineEdit', qss)
        self.assertIn('QCheckBox', qss)
        self.assertIn('QRadioButton', qss)
        self.assertIn('QTabWidget', qss)
        self.assertIn('QMenu', qss)
        self.assertIn('QProgressBar', qss)
        self.assertIn('QScrollBar', qss)

    def test_enhanced_button_styles(self) -> None:
        """Test enhanced button styles generation."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Check for enhanced button styles
        self.assertIn('QPushButton[class="primary"]', qss)
        self.assertIn('background-color: #4a90e2', qss)
        self.assertIn('border: 2px solid #2c5aa0', qss)

    def test_enhanced_input_styles(self) -> None:
        """Test enhanced input styles generation."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Check for enhanced input styles
        self.assertIn('QLineEdit[class="error"]', qss)
        self.assertIn('QLineEdit[class="success"]', qss)
        self.assertIn('box-shadow: 0 0 0 2px', qss)
        self.assertIn('font-style: italic', qss)

    def test_enhanced_panel_styles(self) -> None:
        """Test enhanced panel styles generation."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Check for enhanced panel styles
        self.assertIn('QGroupBox::title', qss)
        self.assertIn('QFrame[frameShape="4"]', qss)
        self.assertIn('QListWidget::item:hover', qss)

    def test_enhanced_menu_styles(self) -> None:
        """Test enhanced menu styles generation."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Check for enhanced menu styles
        self.assertIn('QMenuBar::item', qss)
        self.assertIn('QMenu::item', qss)
        self.assertIn('QMenu::separator', qss)

    def test_enhanced_progress_styles(self) -> None:
        """Test enhanced progress bar styles generation."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Check for enhanced progress styles
        self.assertIn('QProgressBar[textVisible="false"]', qss)
        self.assertIn('QProgressBar::chunk', qss)

    def test_enhanced_scrollbar_styles(self) -> None:
        """Test enhanced scrollbar styles generation."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Check for enhanced scrollbar styles
        self.assertIn('QScrollBar:vertical', qss)
        self.assertIn('QScrollBar:horizontal', qss)
        self.assertIn('QScrollBar::handle:vertical:hover', qss)
        self.assertIn('QScrollBar::handle:horizontal:hover', qss)

    def test_enhanced_list_styles(self) -> None:
        """Test enhanced list and tree styles generation."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Check for enhanced list styles
        self.assertIn('QListView::item:hover', qss)
        self.assertIn('QTreeView::branch', qss)
        self.assertIn('QTreeView::branch:has-children', qss)

    def test_enhanced_tab_styles(self) -> None:
        """Test enhanced tab styles generation."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Check for enhanced tab styles
        self.assertIn('QTabWidget::tab-bar', qss)
        self.assertIn('QTabBar::tab:selected', qss)
        self.assertIn('QTabBar::tab:hover', qss)

    def test_checkbox_radio_styles(self) -> None:
        """Test checkbox and radio button styles generation."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Check for checkbox and radio styles
        self.assertIn('QCheckBox::indicator', qss)
        self.assertIn('QRadioButton::indicator', qss)
        self.assertIn('QCheckBox::indicator:checked', qss)
        self.assertIn('QRadioButton::indicator:checked', qss)

    def test_svg_icon_integration(self) -> None:
        """Test SVG icon integration in styles."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Check for SVG icon usage
        self.assertIn('image: url(data:image/svg+xml;base64,', qss)
        self.assertIn('PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIg', qss)

    def test_advanced_mode_color_inheritance(self) -> None:
        """Test color inheritance in advanced mode."""
        generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Check that advanced styles inherit from base colors
        self.assertIn('background-color: #1a1a1a', qss)  # backgroundColor
        self.assertIn('color: #ffffff', qss)  # textColor
        self.assertIn('background-color: #4a90e2', qss)  # primaryColor

    def test_advanced_mode_fallback_values(self) -> None:
        """Test fallback values in advanced mode."""
        config_without_advanced = {
            'name': 'simple_theme',
            'display_name': 'Simple Theme',
            'backgroundColor': '#ffffff',
            'textColor': '#000000'
        }
        
        generator = StylesheetGenerator(config_without_advanced, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Should still generate advanced styles with fallback values
        self.assertIn('QCheckBox::indicator', qss)
        self.assertIn('QTabWidget::pane', qss)
        self.assertIn('QMenu::item', qss)

    def test_advanced_mode_performance(self) -> None:
        """Test that advanced mode doesn't significantly impact performance."""
        import time
        
        # Basic mode timing
        basic_generator = StylesheetGenerator(self.basic_config, advanced_mode=False)
        start_time = time.time()
        basic_qss = basic_generator.generate_qss()
        basic_time = time.time() - start_time
        
        # Advanced mode timing
        advanced_generator = StylesheetGenerator(self.advanced_config, advanced_mode=True)
        start_time = time.time()
        advanced_qss = advanced_generator.generate_qss()
        advanced_time = time.time() - start_time
        
        # Advanced mode should not be more than 3x slower
        self.assertLess(advanced_time, basic_time * 3)
        
        # Advanced QSS should be significantly larger
        self.assertGreater(len(advanced_qss), len(basic_qss) * 2)

    def test_advanced_mode_consistency(self) -> None:
        """Test consistency between basic and advanced mode outputs."""
        basic_generator = StylesheetGenerator(self.basic_config, advanced_mode=False)
        advanced_generator = StylesheetGenerator(self.basic_config, advanced_mode=True)
        
        basic_qss = basic_generator.generate_qss()
        advanced_qss = advanced_generator.generate_qss()
        
        # Both modes should contain basic widget styles
        self.assertIn('QWidget {', basic_qss)
        self.assertIn('QWidget {', advanced_qss)
        
        # Both modes should contain button styles
        self.assertIn('QPushButton {', basic_qss)
        self.assertIn('QPushButton {', advanced_qss)
        
        # Advanced mode should contain additional components
        self.assertIn('QCheckBox', advanced_qss)
        self.assertIn('QTabWidget', advanced_qss)
        self.assertIn('QMenu', advanced_qss)
        
        # Basic mode should not contain advanced components
        self.assertNotIn('QCheckBox', basic_qss)
        self.assertNotIn('QTabWidget', basic_qss)
        self.assertNotIn('QMenu', basic_qss)
        
        # Both should generate valid QSS
        self.assertIsInstance(basic_qss, str)
        self.assertIsInstance(advanced_qss, str)
        self.assertGreater(len(basic_qss), 0)
        self.assertGreater(len(advanced_qss), 0)

    def test_advanced_mode_error_handling(self) -> None:
        """Test error handling in advanced mode."""
        invalid_config = {
            'name': 'invalid_theme',
            'display_name': 'Invalid Theme',
            'backgroundColor': None,  # Invalid value
            'textColor': '#000000'
        }
        
        generator = StylesheetGenerator(invalid_config, advanced_mode=True)
        
        # Should not raise exception
        try:
            qss = generator.generate_qss()
            self.assertIsInstance(qss, str)
            self.assertGreater(len(qss), 0)
        except Exception as e:
            self.fail(f"Advanced mode should handle invalid config gracefully: {e}")

    def test_advanced_mode_customization(self) -> None:
        """Test advanced mode customization options."""
        custom_config = self.advanced_config.copy()
        custom_config['custom_component'] = {
            'background': '#ff0000',
            'text': '#ffffff'
        }
        
        generator = StylesheetGenerator(custom_config, advanced_mode=True)
        qss = generator.generate_qss()
        
        # Should still generate valid QSS
        self.assertIsInstance(qss, str)
        self.assertGreater(len(qss), 0)
        
        # Should contain all standard advanced components
        self.assertIn('QCheckBox', qss)
        self.assertIn('QTabWidget', qss)
        self.assertIn('QMenu', qss)


if __name__ == "__main__":
    unittest.main()
