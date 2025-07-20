# ThemeManager API Reference

This document provides detailed information about all APIs available in the ThemeManager library.

## 🆕 New in v0.2.0

### GUI Tools Entry Points

```python
# Theme Editor (also available as `theme-editor` command)
from theme_manager.qt.theme_editor import launch_theme_editor
launch_theme_editor()

# Theme Preview (also available as `theme-preview` command)  
from theme_manager.qt.preview import launch_preview
launch_preview()
```

### Advanced Features

- Enhanced `ThemeController` with improved error handling
- New accessibility features in theme editor
- Expanded theme configuration options

## Table of Contents

1. [GUI Tools](#gui-tools)
2. [ThemeController](#themecontroller)
3. [ThemeLoader](#themeloader) 
4. [StylesheetGenerator](#stylesheetgenerator)
5. [Utility Functions](#utility-functions)
6. [Configuration File Specification](#configuration-file-specification)
7. [Error Handling](#error-handling)

## GUI Tools

### launch_theme_editor()

Launch the advanced theme editor application.

```python
from theme_manager.qt.theme_editor import launch_theme_editor

launch_theme_editor(config_path=None)
```

**Parameters:**
- `config_path` (Optional): Path to theme configuration file

**Features:**
- Color theory-based design tools
- Real-time preview
- Component-specific customization
- Accessibility features
- Import/Export functionality

### launch_preview()

Launch the theme preview application.

```python
from theme_manager.qt.preview import launch_preview

launch_preview()
```

**Features:**
- 16+ built-in themes
- Live theme switching
- Comprehensive widget showcase

## ThemeController

Main class for theme management.

### Constructor

```python
ThemeController(config_path: Optional[Union[str, Path]] = None)
```

**Parameters:**
- `config_path` (Optional): Path to theme configuration file. If None, uses default configuration file

**Example:**
```python
# Use default configuration
controller = ThemeController()

# Use custom configuration file
controller = ThemeController("/path/to/custom/config.json")
```

### Methods

#### `get_available_themes() -> Dict[str, Any]`

Get all available themes.

**Returns:**
- `Dict[str, Any]`: Dictionary with theme names as keys and theme configurations as values

**Example:**
```python
themes = controller.get_available_themes()
for name, config in themes.items():
    print(f"Theme: {name}, Display: {config.get('display_name')}")
```

#### `get_current_theme_name() -> str`

Get the currently active theme name.

**Returns:**
- `str`: Current theme name

**Example:**
```python
current = controller.get_current_theme_name()
print(f"Current theme: {current}")
```

#### `set_theme(theme_name: str, save_settings: bool = True) -> bool`

Switch to the specified theme.

**Parameters:**
- `theme_name` (str): Name of theme to set
- `save_settings` (bool): Whether to save settings to file (default: True)

**Returns:**
- `bool`: True if successful, False if failed

**Example:**
```python
# Set theme and save
success = controller.set_theme("dark")

# Set theme without saving (temporary)
success = controller.set_theme("light", save_settings=False)
```

#### `apply_theme_to_widget(widget) -> None`

Apply theme to the specified widget.

**Parameters:**
- `widget`: Qt widget to apply theme to

**Example:**
```python
# Apply theme to main window
controller.apply_theme_to_widget(main_window)

# Apply theme to specific button
controller.apply_theme_to_widget(my_button)
```

#### `apply_theme_to_application(app=None) -> None`

Apply theme to the entire application.

**Parameters:**
- `app` (Optional): QApplication instance. If None, uses current application

**Example:**
```python
# Apply theme to current application
controller.apply_theme_to_application()

# Apply theme to specific application
controller.apply_theme_to_application(my_app)
```

#### `export_qss(output_path: str, theme_name: Optional[str] = None) -> bool`

Export QSS stylesheet to file.

**Parameters:**
- `output_path` (str): Output file path
- `theme_name` (Optional): Theme name to export. If None, uses current theme

**Returns:**
- `bool`: True if successful, False if failed

**Example:**
```python
# Export current theme
controller.export_qss("current_theme.qss")

# Export specific theme
controller.export_qss("dark_theme.qss", "dark")
```

## ThemeLoader

Class responsible for loading and saving theme configurations.

### Constructor

```python
ThemeLoader(config_path: Optional[Union[str, Path]] = None)
```

**Parameters:**
- `config_path` (Optional): Path to configuration file

### Methods

#### `load_settings() -> Dict[str, Any]`

Load theme settings from configuration file.

**Returns:**
- `Dict[str, Any]`: Loaded settings

**Example:**
```python
loader = ThemeLoader()
settings = loader.load_settings()
print(f"Settings version: {settings.get('version')}")
```

#### `get_available_themes() -> Dict[str, Any]`

Get dictionary of available themes.

**Returns:**
- `Dict[str, Any]`: Theme configuration dictionary

#### `get_current_theme() -> str`

Get current theme name.

**Returns:**
- `str`: Current theme name

#### `update_current_theme(theme_name: str, save: bool = True) -> bool`

Update current theme.

**Parameters:**
- `theme_name` (str): New theme name
- `save` (bool): Whether to save to file

**Returns:**
- `bool`: True if successful

#### `save_settings() -> bool`

Save current settings to file.

**Returns:**
- `bool`: True if successful

## StylesheetGenerator

Class responsible for generating QSS stylesheets.

### Constructor

```python
StylesheetGenerator(theme_config: Dict[str, Any])
```

**Parameters:**
- `theme_config` (Dict): Theme configuration dictionary

### Methods

#### `generate_qss() -> str`

Generate complete QSS stylesheet.

**Returns:**
- `str`: Generated QSS stylesheet

**Example:**
```python
generator = StylesheetGenerator(theme_config)
qss = generator.generate_qss()
widget.setStyleSheet(qss)
```

#### `generate_widget_qss(widget_type: str) -> str`

Generate QSS for specific widget type.

**Parameters:**
- `widget_type` (str): Widget type ('button', 'panel', 'input', etc.)

**Returns:**
- `str`: QSS style for specified widget

**Example:**
```python
# Generate QSS for buttons only
button_qss = generator.generate_widget_qss('button')

# Generate QSS for panels only
panel_qss = generator.generate_widget_qss('panel')
```

#### `validate_theme_config(theme_config: Dict[str, Any]) -> bool`

Validate theme configuration.

**Parameters:**
- `theme_config` (Dict): Theme configuration to validate

**Returns:**
- `bool`: True if valid

**Example:**
```python
is_valid = StylesheetGenerator.validate_theme_config(my_theme_config)
if not is_valid:
    print("Theme configuration has issues")
```

## Utility Functions

### `apply_theme_to_widget(widget, theme_name: Optional[str] = None)`

Convenience function to apply theme to a widget.

**Parameters:**
- `widget`: Target Qt widget
- `theme_name` (Optional): Theme name. If None, uses current theme

**Example:**
```python
from theme_manager import apply_theme_to_widget

# Apply current theme
apply_theme_to_widget(my_widget)

# Apply specific theme
apply_theme_to_widget(my_widget, "dark")
```

### `apply_theme_to_application(theme_name: Optional[str] = None)`

Convenience function to apply theme to entire application.

**Parameters:**
- `theme_name` (Optional): Theme name. If None, uses current theme

**Example:**
```python
from theme_manager import apply_theme_to_application

# Apply current theme to entire application
apply_theme_to_application()

# Apply specific theme to entire application
apply_theme_to_application("blue")
```

## Configuration File Specification

### Basic Structure

```json
{
  "current_theme": "dark",
  "last_selected_theme": "dark", 
  "theme_switching_enabled": true,
  "remember_theme_choice": true,
  "version": "0.0.1",
  "available_themes": {
    "theme_name": {
      // Theme configuration
    }
  }
}
```

### Theme Configuration Structure

```json
{
  "name": "dark",
  "display_name": "Dark Mode",
  "description": "Dark background low-strain theme",
  "primaryColor": "#222831",
  "accentColor": "#00adb5", 
  "backgroundColor": "#1a1a1a",
  "textColor": "#eeeeee",
  "button": {
    "background": "#4a5568",
    "text": "#ffffff",
    "hover": "#00adb5",
    "pressed": "#2d3748",
    "border": "#718096"
  },
  "panel": {
    "background": "#23272f",
    "border": "#393e46",
    "header": {
      "background": "#2d3748",
      "text": "#ffffff",
      "border": "#4a5568"
    }
  },
  "input": {
    "background": "#2d3748",
    "text": "#ffffff",
    "border": "#4a5568",
    "focus": "#00adb5",
    "placeholder": "#a0aec0"
  },
  "text": {
    "primary": "#ffffff",
    "secondary": "#cbd5e0",
    "muted": "#a0aec0",
    "success": "#48bb78",
    "warning": "#ed8936",
    "error": "#f56565"
  }
}
```

### Required Fields

- `name`: Internal theme name
- `backgroundColor`: Background color
- `textColor`: Basic text color
- `primaryColor`: Primary color
- `accentColor`: Accent color

### Optional Fields

- `display_name`: Display name
- `description`: Theme description
- `button`: Button style settings
- `panel`: Panel style settings
- `input`: Input field style settings
- `text`: Text color variations

## Error Handling

### Common Exceptions

#### `FileNotFoundError`
Raised when configuration file is not found.

```python
try:
    controller = ThemeController("/nonexistent/config.json")
except FileNotFoundError:
    print("Configuration file not found")
```

#### `json.JSONDecodeError`
Raised when configuration file JSON is invalid.

```python
try:
    controller = ThemeController()
except json.JSONDecodeError:
    print("Configuration file JSON is invalid")
```

#### `KeyError`
Raised when required theme configuration is missing.

```python
try:
    controller.set_theme("nonexistent_theme")
except KeyError:
    print("Specified theme does not exist")
```

### Error Handling Example

```python
from theme_manager.qt.controller import ThemeController
import json

def safe_theme_setup():
    try:
        controller = ThemeController()
        
        # Check theme existence
        available_themes = controller.get_available_themes()
        if "dark" in available_themes:
            success = controller.set_theme("dark")
            if success:
                print("Theme set successfully")
            else:
                print("Failed to set theme")
        else:
            print("Specified theme is not available")
            
    except FileNotFoundError:
        print("Configuration file not found")
    except json.JSONDecodeError:
        print("Configuration file format is incorrect")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

# Usage example
safe_theme_setup()
```

## Performance Considerations

### Best Practices

1. **Reuse ThemeController**: Reuse the same ThemeController instance within your application
2. **Optimize Theme Application**: For applications with many widgets, apply theme only to parent widgets
3. **Batch Settings Updates**: When making multiple theme changes, use `save_settings=False` and save at the end

### Example

```python
# Efficient theme management
class MyApp:
    def __init__(self):
        self.theme_controller = ThemeController()  # Create only once
        
    def setup_ui(self):
        # Apply only to parent widget
        self.theme_controller.apply_theme_to_widget(self.main_window)
        
    def batch_theme_changes(self):
        # Batch changes (save only at the end)
        self.theme_controller.set_theme("dark", save_settings=False)
        # ... other configuration changes ...
        self.theme_controller.save_settings()  # Save at the end
```

Use this API reference to efficiently utilize the ThemeManager library.
