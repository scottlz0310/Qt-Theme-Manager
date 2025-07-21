#!/usr/bin/env python3
"""
Qt Framework Testing Script
Tests PyQt5, PyQt6, and PySide6 installations in CI/CD environments.
"""

import sys
import os
import argparse

def print_environment():
    """Print environment information for debugging"""
    print("=== Environment Information ===")
    print(f"DISPLAY: {os.environ.get('DISPLAY', 'Not set')}")
    print(f"QT_QPA_PLATFORM: {os.environ.get('QT_QPA_PLATFORM', 'Not set')}")
    print(f"XDG_RUNTIME_DIR: {os.environ.get('XDG_RUNTIME_DIR', 'Not set')}")
    print(f"PYTHONIOENCODING: {os.environ.get('PYTHONIOENCODING', 'Not set')}")
    print()

def test_qt_framework(framework):
    """Test specific Qt framework"""
    try:
        print_environment()
        print(f"=== Testing {framework} Framework ===")
        print(f"Python version: {sys.version}")
        print(f"Python executable: {sys.executable}")
        
        if framework == "pyqt5":
            return test_pyqt5()
        elif framework == "pyqt6":
            return test_pyqt6()
        elif framework == "pyside6":
            return test_pyside6()
        else:
            print(f"ERROR: Unknown framework '{framework}'")
            return False
    except Exception as e:
        print(f"ERROR: Qt framework test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_platform_fallback(framework_name, test_func):
    """Test Qt framework with platform fallbacks"""
    platforms = ['xcb', 'offscreen', 'minimal']
    original_platform = os.environ.get('QT_QPA_PLATFORM', '')
    
    for platform in platforms:
        try:
            print(f"Trying {framework_name} with platform: {platform}")
            os.environ['QT_QPA_PLATFORM'] = platform
            result = test_func()
            print(f"{framework_name} works with platform: {platform}")
            return result
        except Exception as e:
            print(f"{framework_name} failed with platform {platform}: {e}")
            continue
        finally:
            # Restore original platform
            if original_platform:
                os.environ['QT_QPA_PLATFORM'] = original_platform
            elif 'QT_QPA_PLATFORM' in os.environ:
                del os.environ['QT_QPA_PLATFORM']
    
    print(f"ERROR: {framework_name} failed with all platforms")
    return False


def test_pyqt5_core():
    """Core PyQt5 test"""
    # Test QtCore import
    from PyQt5.QtCore import qVersion, PYQT_VERSION_STR, QT_VERSION_STR
    print(f"PyQt5 version: {PYQT_VERSION_STR}")
    print(f"Qt version: {QT_VERSION_STR}")
    print(f"Runtime Qt version: {qVersion()}")
    
    # Test QtWidgets import
    from PyQt5.QtWidgets import QApplication
    print("PyQt5.QtWidgets imported successfully")
    
    # Test QApplication creation
    app = QApplication.instance() or QApplication([])
    app.processEvents()
    print("PyQt5 QApplication created successfully")
    
    return True


def test_pyqt5():
    """Test PyQt5 installation."""
    print("Testing PyQt5...")
    return test_with_platform_fallback("PyQt5", test_pyqt5_core)


def test_pyqt6_core():
    """Core PyQt6 test"""
    # Test QtCore import
    from PyQt6.QtCore import qVersion, PYQT_VERSION_STR, QT_VERSION_STR
    print(f"PyQt6 version: {PYQT_VERSION_STR}")
    print(f"Qt version: {QT_VERSION_STR}")
    print(f"Runtime Qt version: {qVersion()}")
    
    # Test QtWidgets import
    from PyQt6.QtWidgets import QApplication
    print("PyQt6.QtWidgets imported successfully")
    
    # Test QApplication creation
    app = QApplication.instance() or QApplication([])
    app.processEvents()
    print("PyQt6 QApplication created successfully")
    
    return True


def test_pyqt6():
    """Test PyQt6 installation."""
    print("Testing PyQt6...")
    return test_with_platform_fallback("PyQt6", test_pyqt6_core)


def test_pyside6_core():
    """Core PySide6 test"""
    # Test QtCore import
    from PySide6.QtCore import qVersion, __version__
    print(f"PySide6 version: {__version__}")
    print(f"Runtime Qt version: {qVersion()}")
    
    # Test QtWidgets import
    from PySide6.QtWidgets import QApplication
    print("PySide6.QtWidgets imported successfully")
    
    # Test QApplication creation
    app = QApplication.instance() or QApplication([])
    app.processEvents()
    print("PySide6 QApplication created successfully")
    
    return True


def test_pyside6():
    """Test PySide6 installation."""
    print("Testing PySide6...")
    return test_with_platform_fallback("PySide6", test_pyside6_core)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Test Qt framework installation')
    parser.add_argument('framework', choices=['pyqt5', 'pyqt6', 'pyside6'], 
                       help='Qt framework to test')
    parser.add_argument('--verbose', action='store_true', 
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Testing {args.framework} framework...")
        print("-" * 50)
    
    try:
        success = test_qt_framework(args.framework)
        if success:
            print(f"SUCCESS: {args.framework} test passed")
            sys.exit(0)
        else:
            print(f"FAILED: {args.framework} test failed")
            sys.exit(1)
    except Exception as e:
        print(f"FAILED: {args.framework} test failed with exception: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
import sys
import os
import argparse


def test_qt_framework(framework):
    """Test specific Qt framework installation and functionality."""
    print(f"=== Testing {framework} Framework ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    try:
        if framework == "pyqt5":
            return test_pyqt5()
        elif framework == "pyqt6":
            return test_pyqt6()
        elif framework == "pyside6":
            return test_pyside6()
        else:
            print(f"ERROR: Unknown framework '{framework}'")
            return False
            
    except Exception as e:
        print(f"ERROR: Qt framework test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pyqt5():
    """Test PyQt5 installation."""
    print("Testing PyQt5...")
    
    # Test QtCore import
    from PyQt5.QtCore import qVersion, PYQT_VERSION_STR, QT_VERSION_STR
    print(f"PyQt5 version: {PYQT_VERSION_STR}")
    print(f"Qt version: {QT_VERSION_STR}")
    print(f"Runtime Qt version: {qVersion()}")
    
    # Test QtWidgets import
    from PyQt5.QtWidgets import QApplication
    print("PyQt5.QtWidgets imported successfully")
    
    # Test QApplication creation
    app = QApplication.instance() or QApplication([])
    print("QApplication creation: SUCCESS")
    
    # Test basic application functionality
    app.processEvents()
    print("QApplication processEvents: SUCCESS")
    
    # Clean shutdown
    if not QApplication.instance():
        app.quit()
    print("QApplication cleanup: SUCCESS")
    
    return True


def test_pyqt6():
    """Test PyQt6 installation."""
    print("Testing PyQt6...")
    
    # Test QtCore import
    from PyQt6.QtCore import qVersion, PYQT_VERSION_STR, QT_VERSION_STR
    print(f"PyQt6 version: {PYQT_VERSION_STR}")
    print(f"Qt version: {QT_VERSION_STR}")
    print(f"Runtime Qt version: {qVersion()}")
    
    # Test QtWidgets import
    from PyQt6.QtWidgets import QApplication
    print("PyQt6.QtWidgets imported successfully")
    
    # Test QApplication creation
    app = QApplication.instance() or QApplication([])
    print("QApplication creation: SUCCESS")
    
    # Test basic application functionality
    app.processEvents()
    print("QApplication processEvents: SUCCESS")
    
    # Clean shutdown
    if not QApplication.instance():
        app.quit()
    print("QApplication cleanup: SUCCESS")
    
    return True


def test_pyside6():
    """Test PySide6 installation."""
    print("Testing PySide6...")
    
    # Test QtCore import
    from PySide6.QtCore import qVersion, __version__ as PYSIDE_VERSION
    print(f"PySide6 version: {PYSIDE_VERSION}")
    print(f"Runtime Qt version: {qVersion()}")
    
    # Test QtWidgets import
    from PySide6.QtWidgets import QApplication
    print("PySide6.QtWidgets imported successfully")
    
    # Test QApplication creation
    app = QApplication.instance() or QApplication([])
    print("QApplication creation: SUCCESS")
    
    # Test basic application functionality
    app.processEvents()
    print("QApplication processEvents: SUCCESS")
    
    # Clean shutdown
    if not QApplication.instance():
        app.quit()
    print("QApplication cleanup: SUCCESS")
    
    return True


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test Qt framework installation")
    parser.add_argument("framework", choices=["pyqt5", "pyqt6", "pyside6"],
                       help="Qt framework to test")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        print("=== Environment Information ===")
        print(f"DISPLAY: {os.environ.get('DISPLAY', 'Not set')}")
        print(f"QT_QPA_PLATFORM: {os.environ.get('QT_QPA_PLATFORM', 'Not set')}")
        print(f"XDG_RUNTIME_DIR: {os.environ.get('XDG_RUNTIME_DIR', 'Not set')}")
        print(f"PYTHONIOENCODING: {os.environ.get('PYTHONIOENCODING', 'Not set')}")
        print()
    
    success = test_qt_framework(args.framework)
    
    if success:
        print(f"SUCCESS: {args.framework} test completed successfully")
        sys.exit(0)
    else:
        print(f"FAILED: {args.framework} test failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
