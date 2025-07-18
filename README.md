# ThemeManager for PyQt5/PyQt6/PySide6

A comprehensive theme management library for PyQt5/PyQt6/PySide6 applications, providing dynamic theme switching with support for dark, light, and high contrast themes.

## Features

- 🎨 **16 Built-in Themes**: Light, Dark, High Contrast, and 13 additional color themes
- 🔄 **Dynamic Theme Switching**: Change themes at runtime without restarting
- 💾 **Persistent Settings**: Theme preferences are automatically saved
- 🖥️ **CLI Support**: Command-line interface for theme management
- 📱 **GUI Preview**: Interactive preview window to test themes
- 🎯 **Easy Integration**: Simple API for applying themes to widgets/applications
- ⚡ **QSS Generation**: Automatic stylesheet generation from theme configurations

## Installation

Currently, install from source:

```bash
git clone <repository-url>
cd Theme-Manager

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
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

### Visual Theme Preview

Launch a GUI preview window to see all themes in action:

```bash
python launch_gui_preview.py
```

This preview window allows you to:
- Switch between all 16 themes in real-time
- See how buttons, inputs, sliders, and other widgets look in each theme
- Intuitively compare colors and contrast across different themes

### List Available Themes

```bash
python -m theme_manager.main list
```

### Set Theme

```bash
python -m theme_manager.main set dark
```

### Export QSS Stylesheet

```bash
python -m theme_manager.main export dark dark_theme.qss
```

### Show Current Theme

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
