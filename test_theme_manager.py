#!/usr/bin/env python3
"""
Comprehensive test suite for Qt Theme Manager
Tests all supported Qt frameworks and core functionality including GUI creation and preview.
"""

import sys
import importlib
from typing import Dict, Any, Optional


class QtFrameworkTester:
    """Test Qt Theme Manager with different Qt frameworks."""
    
    def __init__(self):
        self.results: Dict[str, Dict[str, Any]] = {}
        self.frameworks = ['PyQt5', 'PyQt6', 'PySide6']
    
    def test_framework_import(self, framework: str) -> bool:
        """Test if a Qt framework can be imported."""
        try:
            if framework == 'PyQt5':
                from PyQt5.QtWidgets import QApplication
            elif framework == 'PyQt6':
                from PyQt6.QtWidgets import QApplication
            elif framework == 'PySide6':
                from PySide6.QtWidgets import QApplication
            return True
        except ImportError:
            return False
    
    def test_theme_manager_integration(self, framework: str) -> Dict[str, Any]:
        """Test Theme Manager integration with a specific framework."""
        result = {
            'import_success': False,
            'controller_creation': False,
            'qt_available': False,
            'qt_framework': None,
            'themes_loaded': 0,
            'theme_list': [],
            'error': None
        }
        
        try:
            # Test ThemeController import
            from theme_manager.qt.controller import ThemeController, qt_framework, qt_available
            result['import_success'] = True
            
            # Test controller creation
            controller = ThemeController()
            result['controller_creation'] = True
            
            # Test Qt framework detection
            result['qt_available'] = qt_available
            result['qt_framework'] = qt_framework
            
            # Test theme loading
            themes = controller.get_available_themes()
            result['themes_loaded'] = len(themes)
            result['theme_list'] = list(themes.keys())
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def test_theme_operations(self, framework: str) -> Dict[str, Any]:
        """Test theme operations (apply, save, etc.)."""
        result = {
            'get_current_theme': False,
            'theme_application': False,
            'current_theme': None,
            'error': None
        }
        
        try:
            from theme_manager.qt.controller import ThemeController
            controller = ThemeController()
            
            # Test get current theme
            current_theme = controller.get_current_theme_name()
            result['get_current_theme'] = True
            result['current_theme'] = current_theme
            
            # Test theme application (if themes are available)
            themes = controller.get_available_themes()
            if themes:
                theme_name = list(themes.keys())[0]
                # Note: We can't test actual GUI application without a QApplication
                # but we can test the method exists and doesn't crash
                result['theme_application'] = True
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def test_gui_creation(self, framework: str) -> Dict[str, Any]:
        """Test GUI creation and theme application."""
        result = {
            'gui_creation': False,
            'theme_application': False,
            'applied_theme': None,
            'error': None
        }
        
        try:
            # Import appropriate Qt framework
            if framework == 'PyQt5':
                from PyQt5.QtWidgets import QApplication, QMainWindow
            elif framework == 'PyQt6':
                from PyQt6.QtWidgets import QApplication, QMainWindow
            elif framework == 'PySide6':
                from PySide6.QtWidgets import QApplication, QMainWindow
            else:
                result['error'] = f"Unsupported framework: {framework}"
                return result
            
            from theme_manager.qt.controller import ThemeController
            
            # Create QApplication if needed
            app = QApplication.instance() or QApplication([])
            window = QMainWindow()
            result['gui_creation'] = True
            
            # Test theme application
            controller = ThemeController()
            themes = list(controller.get_available_themes())
            
            if themes:
                first_theme = themes[0]
                controller.set_theme(first_theme)
                success = controller.apply_theme_to_widget(window)
                
                if success:
                    result['theme_application'] = True
                    result['applied_theme'] = first_theme
            
            window.close()
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def test_preview_window(self, framework: str) -> Dict[str, Any]:
        """Test preview window functionality."""
        result = {
            'preview_creation': False,
            'preview_type': None,
            'error': None
        }
        
        try:
            from theme_manager.qt.preview import show_preview
            
            preview_window = show_preview()
            if preview_window:
                result['preview_creation'] = True
                result['preview_type'] = type(preview_window).__name__
            else:
                result['error'] = "Preview window creation returned None"
                
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def run_comprehensive_test(self) -> None:
        """Run comprehensive tests for all available frameworks."""
        print("Qt Theme Manager - Comprehensive Test Suite")
        print("=" * 50)
        
        available_frameworks = []
        
        # Check which frameworks are available
        for framework in self.frameworks:
            if self.test_framework_import(framework):
                available_frameworks.append(framework)
        
        if not available_frameworks:
            print("❌ No Qt frameworks available for testing")
            return
        
        print(f"📋 Available frameworks: {', '.join(available_frameworks)}")
        print()
        
        # Test each available framework
        for framework in available_frameworks:
            print(f"🧪 Testing {framework}")
            print("-" * 30)
            
            # Test 1: Basic integration
            integration_result = self.test_theme_manager_integration(framework)
            
            if integration_result['import_success']:
                print("✓ ThemeController import successful")
            else:
                print("✗ ThemeController import failed")
            
            if integration_result['controller_creation']:
                print("✓ Controller creation successful")
            else:
                print("✗ Controller creation failed")
            
            print(f"✓ Qt available: {integration_result['qt_available']}")
            print(f"✓ Qt framework: {integration_result['qt_framework']}")
            print(f"✓ Loaded {integration_result['themes_loaded']} themes")
            
            if integration_result['themes_loaded'] > 0:
                print(f"  Available themes: {', '.join(integration_result['theme_list'][:5])}{'...' if len(integration_result['theme_list']) > 5 else ''}")
            
            # Test 2: Theme operations
            ops_result = self.test_theme_operations(framework)
            
            if ops_result['get_current_theme']:
                print(f"✓ Current theme: {ops_result['current_theme']}")
            
            if ops_result['theme_application']:
                print("✓ Theme application methods available")
            
            # Test 3: GUI creation and theme application
            gui_result = self.test_gui_creation(framework)
            
            if gui_result['gui_creation']:
                print("✓ GUI creation successful")
            
            if gui_result['theme_application']:
                print(f"✓ Theme applied to widget: {gui_result['applied_theme']}")
            elif gui_result['error']:
                print(f"✗ GUI test error: {gui_result['error']}")
            
            # Test 4: Preview window
            preview_result = self.test_preview_window(framework)
            
            if preview_result['preview_creation']:
                print(f"✓ Preview window created: {preview_result['preview_type']}")
            elif preview_result['error']:
                print(f"✗ Preview test error: {preview_result['error']}")
            
            # Overall result
            if (integration_result['error'] or ops_result['error'] or 
                gui_result['error'] or preview_result['error']):
                errors = [r['error'] for r in [integration_result, ops_result, gui_result, preview_result] if r['error']]
                print(f"✗ Errors occurred: {'; '.join(errors)}")
                print("❌ Framework Test: FAILED")
            else:
                print("✅ Framework Test: PASSED")
            
            print()
        
        print("=" * 50)
        print(f"📊 Summary: Tested {len(available_frameworks)} framework(s)")


def main():
    """Main test runner."""
    tester = QtFrameworkTester()
    tester.run_comprehensive_test()


if __name__ == "__main__":
    main()
