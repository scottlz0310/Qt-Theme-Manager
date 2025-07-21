# ThemeManager for PyQt5/PyQt6/PySide6

[![CI/CD Tests](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml/badge.svg)](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml)
[![PyPI version](https://badge.fury.io/py/qt-theme-manager.svg)](https://badge.fury.io/py/qt-theme-manager)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qt-theme-manager)](https://pypi.org/project/qt-theme-manager/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive theme management library for PyQt5/PyQt6/PySide6 applications, providing dynamic theme switching with an advanced theme editor and 16+ built-in themes.

## ✨ What's New in v0.2.1

- 🔧 **Fixed GUI Startup Issues**: Theme editor now launches reliably across all Qt frameworks
- ⚙️ **Enhanced Qt Compatibility**: Full support for PyQt5, PyQt6, and PySide6
- 🚀 **Improved Startup Methods**: Both module and script execution work perfectly
- � **Better Error Handling**: Cleaner error messages and interruption support

## Features

- 🎨 **16+ Built-in Themes**: Light, Dark, High Contrast, and colorful themes
- ✨ **Advanced Theme Editor**: Professional-grade theme creation tools
- 🔄 **Dynamic Theme Switching**: Change themes at runtime without restarting
- 💾 **Persistent Settings**: Theme preferences are automatically saved
- 🖥️ **GUI Tools**: Interactive editor and preview applications
- 📟 **CLI Support**: Command-line interface for theme management
- 🎯 **Easy Integration**: Simple API for applying themes to widgets/applications
- ⚡ **QSS Generation**: Automatic stylesheet generation from theme configurations

## 🚀 30-Second Quick Start

**Want to try the new theme editor?**

```bash
# Install and launch theme editor (Now with enhanced startup reliability!)
pip install qt-theme-manager[pyqt6]
theme-editor

# Alternative launch methods (both work reliably):
python -m theme_manager.qt.theme_editor
python launch_theme_editor.py  # If you cloned the repo
```

**Want to add beautiful themes to your Qt app in just 3 lines of code?**

```python
from theme_manager.qt.controller import apply_theme_to_widget

# That's it! Apply current theme to any widget:
apply_theme_to_widget(your_widget)
```

**Want to switch themes dynamically?**

```python
from theme_manager.qt.controller import ThemeController

controller = ThemeController()
controller.set_theme("dark")  # or "light", "blue", "cyberpunk", etc.
controller.apply_theme_to_application()
```

**16 beautiful themes ready to use:** `dark`, `light`, `blue`, `green`, `cyberpunk`, `ocean`, and more!

---

## Installation

### Option 1: Install from PyPI (recommended)

```bash
# Basic installation
pip install qt-theme-manager

# Install with your preferred Qt framework (Enhanced compatibility in v0.2.1!)
pip install qt-theme-manager[pyqt6]    # For PyQt6 (recommended)
pip install qt-theme-manager[pyqt5]    # For PyQt5  
pip install qt-theme-manager[pyside6]  # For PySide6

# Install with all Qt frameworks
pip install qt-theme-manager[all]
```

> **✨ New in v0.2.1**: Enhanced Qt framework compatibility ensures reliable operation across PyQt5, PyQt6, and PySide6.

### Option 2: Install from source (for developers)

```bash
git clone https://github.com/scottlz0310/Qt-Theme-Manager.git
cd Qt-Theme-Manager

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install with your preferred Qt framework
pip install -e .[pyqt6]    # For PyQt6
# pip install -e .[pyqt5]  # For PyQt5
# pip install -e .[pyside6] # For PySide6
```

### Requirements

- Python 3.7+
- PyQt5, PyQt6, or PySide6 (for GUI functionality)

## Quick Start

### Basic Usage

```python
from theme_manager.qt.controller import apply_theme_to_widget
from PyQt5.QtWidgets import QApplication, QMainWindow

app = QApplication([])
window = QMainWindow()

# Apply current theme to widget
apply_theme_to_widget(window)

window.show()
app.exec_()
```

### Using ThemeController

```python
from theme_manager.qt.controller import ThemeController

# Initialize theme controller
controller = ThemeController()

# Get available themes
themes = controller.get_available_themes()
print("Available themes:", list(themes.keys()))

# Switch theme
controller.set_theme("dark")

# Apply to application
controller.apply_theme_to_application()
```

## Command Line Interface

### 🎨 GUI Tools (New in v0.2.0!)

After installing via pip, you can use these convenient GUI tools:

```bash
# Launch the advanced theme editor
theme-editor

# Launch theme preview window  
theme-preview

# Use CLI tools
theme-manager --help
```

#### Theme Editor Features
- **Color theory-based color selection** (complementary, triadic, analogous)
- **Real-time preview** of all changes
- **Component-specific settings** for detailed customization
- **Accessibility features** with contrast ratio checking
- **Import/Export** custom themes

#### Theme Preview Features
- **16 built-in themes** to test instantly
- **Live switching** between themes
- **All Qt widgets** displayed for comprehensive testing

### Legacy CLI Methods

For advanced users or scripting:

```bash
# List available themes
python -m theme_manager.cli.main list

# Set theme
python -m theme_manager.cli.main set dark

# Export QSS stylesheet
python -m theme_manager.cli.main export dark dark_theme.qss

# Show current theme

```bash
python -m theme_manager.main current
```

## Available Themes

The library includes 16 built-in themes:

### Core Themes
- **light** - Light mode with bright background
- **dark** - Dark mode with low-strain colors  
- **high_contrast** - High contrast for accessibility

### Color Themes
- **blue** - Professional blue-based theme
- **green** - Natural green-based theme
- **purple** - Elegant purple-based theme
- **orange** - Warm orange-based theme
- **pink** - Playful pink-based theme
- **red** - Bold red-based theme
- **teal** - Calm teal-based theme
- **yellow** - Bright yellow-based theme
- **gray** - Simple gray-based theme
- **sepia** - Eye-friendly sepia theme
- **cyberpunk** - Neon cyberpunk theme
- **forest** - Natural forest theme
- **ocean** - Deep ocean blue theme

## Configuration

Themes are defined in `config/theme_settings.json`. Each theme includes:

- **Basic Colors**: background, text, primary, accent
- **Component Styles**: buttons, inputs, panels, toolbars
- **Text Variants**: primary, secondary, muted, success, warning, error

### Example Theme Configuration

```json
{
  "dark": {
    "name": "dark",
    "display_name": "ダークモード",
    "description": "暗い背景の低負荷テーマ",
    "backgroundColor": "#1a1a1a",
    "textColor": "#eeeeee",
    "primaryColor": "#222831",
    "accentColor": "#00adb5",
    "button": {
      "background": "#4a5568",
      "text": "#ffffff",
      "hover": "#00adb5"
    }
  }
}
```

## Advanced Usage

### Custom Theme Configuration

```python
from theme_manager.qt.controller import ThemeController

# Use custom config file
controller = ThemeController("/path/to/custom/config.json")
```

### Theme Preview Window

```python
from theme_manager.qt.preview import show_preview

# Show interactive preview window
preview_window = show_preview()
```

### Manual QSS Generation

```python
from theme_manager.qt.stylesheet import StylesheetGenerator

theme_config = {...}  # Your theme configuration
generator = StylesheetGenerator(theme_config)

# Generate complete stylesheet
qss = generator.generate_qss()

# Generate specific widget styles
button_qss = generator.generate_widget_qss('button')
```

## Project Structure

```
theme_manager/
├── __init__.py                 # Main package exports
├── config/
│   └── theme_settings.json     # Theme definitions
├── qt/
│   ├── __init__.py
│   ├── loader.py               # JSON configuration loader
│   ├── stylesheet.py           # QSS generation
│   ├── controller.py           # Theme management
│   └── preview.py              # GUI preview window
├── cli/
│   ├── __init__.py
│   └── themectl.py             # CLI interface
└── main.py                     # CLI entry point
```

## Testing

Run the test suite to verify functionality:

```bash
python test_theme_manager.py
```

This will test:
- Theme loading and configuration
- Stylesheet generation
- Theme switching
- CLI functionality
- QSS export

## API Reference

### ThemeController

Main class for theme management.

#### Methods

- `get_available_themes()` - Get all available themes
- `get_current_theme_name()` - Get current active theme
- `set_theme(theme_name, save_settings=True)` - Switch to specified theme
- `apply_theme_to_widget(widget)` - Apply theme to specific widget
- `apply_theme_to_application(app=None)` - Apply theme to entire application
- `export_qss(output_path, theme_name=None)` - Export QSS to file

### ThemeLoader

Handles loading and saving theme configurations.

#### Methods

- `load_settings()` - Load theme configuration from file
- `get_available_themes()` - Get available themes dict
- `get_current_theme()` - Get current theme name
- `update_current_theme(theme_name)` - Update and save current theme

### StylesheetGenerator

Generates QSS stylesheets from theme configurations.

#### Methods

- `generate_qss()` - Generate complete QSS stylesheet
- `generate_widget_qss(widget_type)` - Generate QSS for specific widget type
- `validate_theme_config(theme_config)` - Validate theme configuration

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Changelog

### Version 0.0.1 (Initial Release)
- Basic theme management functionality
- 16 built-in themes
- CLI interface
- GUI preview window
- QSS export functionality
