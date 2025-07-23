# Qt-Theme-Manager Examples and Sample Code

This document provides various usage examples and practical implementations of the Qt-Theme-Manager library.

## 🆕 New in v0.2.3: Enhanced GUI Tools

### Quick Start with GUI Tools

```bash
# Try the new theme editor (after pip install qt-theme-manager[pyqt6])
theme-editor

# Preview all themes instantly
theme-preview

# Enhanced preview with custom themes (v0.2.3)
theme-preview --config my_themes.json --theme ocean

# CLI management
theme-manager list
```

## Table of Contents

1. [GUI Tools Usage](#gui-tools-usage)
2. [Basic Usage](#basic-usage)
3. [Application Examples](#application-examples)
4. [Custom Theme Creation](#custom-theme-creation)
5. [CLI Usage Examples](#cli-usage-examples)
6. [Advanced Usage](#advanced-usage)

## GUI Tools Usage

### Theme Editor Features

The new `theme-editor` command provides:

- **Color Theory Tools**: Choose colors using complementary, triadic, or analogous schemes
- **Real-time Preview**: See changes instantly as you edit
- **Component Settings**: Customize buttons, inputs, panels separately
- **Accessibility**: Built-in contrast ratio checking
- **Import/Export**: Save and share custom themes

### Theme Preview Features

The `theme-preview` command offers:

- **16+ Built-in Themes**: Test all available themes instantly
- **Live Switching**: Change themes with one click
- **Widget Showcase**: See how all Qt widgets look in each theme

## Basic Usage

### 1. Minimal Application

```python
#!/usr/bin/env python3
"""
Minimal ThemeManager application example
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from theme_manager.qt.controller import apply_theme_to_widget

class MinimalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimal Theme App")
        
        # Central widget
        label = QLabel("Hello, ThemeManager!")
        self.setCentralWidget(label)
        
        # Apply theme
        apply_theme_to_widget(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinimalApp()
    window.show()
    sys.exit(app.exec_())
```

### 2. Theme Switcher App

```python
#!/usr/bin/env python3
"""
Application with theme switching functionality
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel, QComboBox
)
from theme_manager.qt.controller import ThemeController

class ThemeSwitcherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = ThemeController()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Theme Switcher App")
        
        # Central widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Current theme display
        self.current_theme_label = QLabel()
        self.update_theme_label()
        layout.addWidget(self.current_theme_label)
        
        # Theme selection combo box
        self.theme_combo = QComboBox()
        themes = self.controller.get_available_themes()
        for theme_name in themes.keys():
            display_name = themes[theme_name].get("display_name", theme_name)
            self.theme_combo.addItem(f"{display_name} ({theme_name})", theme_name)
        
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        layout.addWidget(self.theme_combo)
        
        # Sample button
        sample_button = QPushButton("Sample Button")
        layout.addWidget(sample_button)
        
        self.setCentralWidget(central_widget)
        
        # Apply initial theme
        self.controller.apply_theme_to_widget(self)
        
    def update_theme_label(self):
        current_theme = self.controller.get_current_theme_name()
        themes = self.controller.get_available_themes()
        display_name = themes.get(current_theme, {}).get("display_name", current_theme)
        self.current_theme_label.setText(f"Current Theme: {display_name}")
        
    def on_theme_changed(self):
        theme_data = self.theme_combo.currentData()
        if theme_data:
            self.controller.set_theme(theme_data)
            self.controller.apply_theme_to_widget(self)
            self.update_theme_label()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThemeSwitcherApp()
    window.show()
    sys.exit(app.exec_())
```

## Application Examples

### 3. Complete GUI Application

```python
#!/usr/bin/env python3
"""
Complete GUI application example
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QGroupBox, 
    QListWidget, QMenuBar, QToolBar, QStatusBar, QAction
)
from PyQt5.QtCore import Qt
from theme_manager.qt.controller import ThemeController

class FullGuiApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = ThemeController()
        self.setup_ui()
        self.create_menu()
        self.create_toolbar()
        self.create_status_bar()
        
    def setup_ui(self):
        self.setWindowTitle("Complete GUI Application")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # Left side: Input area
        left_group = QGroupBox("Input Area")
        left_layout = QVBoxLayout(left_group)
        
        left_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        left_layout.addWidget(self.name_input)
        
        left_layout.addWidget(QLabel("Message:"))
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(100)
        left_layout.addWidget(self.message_input)
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_item)
        left_layout.addWidget(add_button)
        
        main_layout.addWidget(left_group)
        
        # Right side: List display
        right_group = QGroupBox("Message List")
        right_layout = QVBoxLayout(right_group)
        
        self.message_list = QListWidget()
        right_layout.addWidget(self.message_list)
        
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_list)
        right_layout.addWidget(clear_button)
        
        main_layout.addWidget(right_group)
        
        self.setCentralWidget(central_widget)
        
        # Apply theme
        self.controller.apply_theme_to_widget(self)
        
    def create_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New", self)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open", self)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Theme menu
        theme_menu = menubar.addMenu("Themes")
        
        themes = self.controller.get_available_themes()
        for theme_name, theme_config in themes.items():
            display_name = theme_config.get("display_name", theme_name)
            action = QAction(display_name, self)
            action.triggered.connect(lambda checked, name=theme_name: self.change_theme(name))
            theme_menu.addAction(action)
        
    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        add_action = QAction("Add", self)
        add_action.triggered.connect(self.add_item)
        toolbar.addAction(add_action)
        
        clear_action = QAction("Clear", self)
        clear_action.triggered.connect(self.clear_list)
        toolbar.addAction(clear_action)
        
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def add_item(self):
        name = self.name_input.text()
        message = self.message_input.toPlainText()
        
        if name and message:
            item_text = f"{name}: {message}"
            self.message_list.addItem(item_text)
            self.name_input.clear()
            self.message_input.clear()
            self.status_bar.showMessage(f"Message added: {name}")
        else:
            self.status_bar.showMessage("Please enter both name and message")
            
    def clear_list(self):
        self.message_list.clear()
        self.status_bar.showMessage("List cleared")
        
    def change_theme(self, theme_name):
        self.controller.set_theme(theme_name)
        self.controller.apply_theme_to_widget(self)
        self.status_bar.showMessage(f"Theme changed to '{theme_name}'")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FullGuiApp()
    window.show()
    sys.exit(app.exec_())
```

## Custom Theme Creation

### 4. Creating and Using Custom Themes

```python
#!/usr/bin/env python3
"""
Custom theme creation example
"""

import json
import tempfile
import os
from theme_manager.qt.controller import ThemeController

# Custom theme configuration
custom_theme_config = {
    "current_theme": "custom_purple",
    "last_selected_theme": "custom_purple",
    "theme_switching_enabled": True,
    "remember_theme_choice": True,
    "version": "0.0.1",
    "available_themes": {
        "custom_purple": {
            "name": "custom_purple",
            "display_name": "Custom Purple",
            "description": "A custom purple theme",
            "primaryColor": "#6B46C1",
            "accentColor": "#A855F7",
            "backgroundColor": "#1F1B24",
            "textColor": "#E5E7EB",
            "button": {
                "background": "#6B46C1",
                "text": "#FFFFFF",
                "hover": "#A855F7",
                "pressed": "#553C9A",
                "border": "#9333EA"
            },
            "panel": {
                "background": "#2D1B3D",
                "border": "#6B46C1",
                "header": {
                    "background": "#553C9A",
                    "text": "#FFFFFF",
                    "border": "#9333EA"
                }
            }
        }
    }
}

def create_custom_theme_demo():
    # Save custom configuration to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(custom_theme_config, f, indent=2, ensure_ascii=False)
        custom_config_path = f.name
    
    try:
        # Initialize ThemeController with custom configuration
        controller = ThemeController(custom_config_path)
        
        # Display available themes
        themes = controller.get_available_themes()
        print("Custom themes available:")
        for name, config in themes.items():
            print(f"  - {config['display_name']} ({name})")
        
        # Generate and export QSS
        output_path = "custom_purple_theme.qss"
        success = controller.export_qss(output_path, "custom_purple")
        
        if success:
            print(f"Custom theme QSS exported to {output_path}")
        
        return controller
        
    finally:
        # Clean up temporary file
        os.unlink(custom_config_path)

if __name__ == "__main__":
    create_custom_theme_demo()
```

## CLI Usage Examples

### 5. Command Line Interface Usage

```bash
# List available themes
python -m theme_manager.main list

# Output example:
# Available themes:
# --------------------------------------------------
#   dark (current)
#     Display Name: Dark Mode
#     Description: Dark background low-strain theme
#
#   light
#     Display Name: Light Mode
#     Description: Clean bright background theme

# Change theme
python -m theme_manager.main set light

# Check current theme
python -m theme_manager.main current

# Export QSS to file
python -m theme_manager.main export dark my_dark_theme.qss
```

## Advanced Usage

### 6. Programmatic Theme Management

```python
#!/usr/bin/env python3
"""
Advanced theme management example
"""

from theme_manager.qt.controller import ThemeController
from theme_manager.qt.stylesheet import StylesheetGenerator
from theme_manager.qt.loader import ThemeLoader

class AdvancedThemeManager:
    def __init__(self):
        self.controller = ThemeController()
        self.loader = ThemeLoader()
        
    def get_theme_statistics(self):
        """Get theme statistics"""
        themes = self.controller.get_available_themes()
        
        stats = {
            "total_themes": len(themes),
            "dark_themes": 0,
            "light_themes": 0,
            "color_themes": 0
        }
        
        for name, config in themes.items():
            if "dark" in name:
                stats["dark_themes"] += 1
            elif "light" in name:
                stats["light_themes"] += 1
            else:
                stats["color_themes"] += 1
                
        return stats
    
    def generate_theme_report(self):
        """Generate theme report"""
        themes = self.controller.get_available_themes()
        current = self.controller.get_current_theme_name()
        
        report = f"Theme Report\n{'='*50}\n"
        report += f"Current Theme: {current}\n"
        report += f"Available Themes: {len(themes)}\n\n"
        
        for name, config in themes.items():
            report += f"Theme: {name}\n"
            report += f"  Display Name: {config.get('display_name', 'N/A')}\n"
            report += f"  Description: {config.get('description', 'N/A')}\n"
            report += f"  Background: {config.get('backgroundColor', 'N/A')}\n"
            report += f"  Text Color: {config.get('textColor', 'N/A')}\n"
            report += "-" * 30 + "\n"
            
        return report
    
    def create_theme_preview_qss(self, theme_name):
        """Generate preview QSS for specific theme"""
        themes = self.controller.get_available_themes()
        if theme_name not in themes:
            return None
            
        theme_config = themes[theme_name]
        generator = StylesheetGenerator(theme_config)
        
        # Generate basic preview QSS
        preview_qss = f"""
/* {theme_config.get('display_name', theme_name)} Theme Preview */
{generator.generate_qss()}

/* Additional preview styles */
.preview-container {{
    background-color: {theme_config.get('backgroundColor', '#ffffff')};
    color: {theme_config.get('textColor', '#000000')};
    padding: 10px;
    border: 2px solid {theme_config.get('accentColor', '#0078d4')};
}}
"""
        return preview_qss

def main():
    manager = AdvancedThemeManager()
    
    # Display statistics
    stats = manager.get_theme_statistics()
    print("Theme Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*50)
    
    # Generate report
    report = manager.generate_theme_report()
    print(report)
    
    # Generate preview QSS
    preview_qss = manager.create_theme_preview_qss("dark")
    if preview_qss:
        with open("dark_theme_preview.qss", "w", encoding="utf-8") as f:
            f.write(preview_qss)
        print("Preview QSS saved to dark_theme_preview.qss")

if __name__ == "__main__":
    main()
```

### 7. Animated Theme Switching App

```python
#!/usr/bin/env python3
"""
Application with animated theme switching
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel, QGraphicsOpacityEffect
)
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtSlot
from theme_manager.qt.controller import ThemeController

class AnimatedThemeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = ThemeController()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Animated Theme Switcher")
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Theme display label
        self.theme_label = QLabel("Current Theme")
        self.theme_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.theme_label)
        
        # Theme switching buttons
        themes = ["dark", "light", "blue", "green"]
        for theme in themes:
            button = QPushButton(f"{theme.capitalize()} Theme")
            button.clicked.connect(lambda checked, t=theme: self.change_theme_animated(t))
            layout.addWidget(button)
            
        self.setCentralWidget(central_widget)
        
        # Apply initial theme
        self.controller.apply_theme_to_widget(self)
        self.update_theme_label()
        
        # Set up opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
    def update_theme_label(self):
        current_theme = self.controller.get_current_theme_name()
        themes = self.controller.get_available_themes()
        display_name = themes.get(current_theme, {}).get("display_name", current_theme)
        self.theme_label.setText(f"Current Theme: {display_name}")
        
    def change_theme_animated(self, theme_name):
        # Fade out animation
        self.fade_out_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out_animation.setDuration(200)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.3)
        self.fade_out_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_out_animation.finished.connect(lambda: self.apply_theme_and_fade_in(theme_name))
        self.fade_out_animation.start()
        
    @pyqtSlot()
    def apply_theme_and_fade_in(self, theme_name):
        # Apply theme
        self.controller.set_theme(theme_name)
        self.controller.apply_theme_to_widget(self)
        self.update_theme_label()
        
        # Fade in animation
        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(200)
        self.fade_in_animation.setStartValue(0.3)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InCubic)
        self.fade_in_animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimatedThemeApp()
    window.show()
    sys.exit(app.exec_())
```

Use these examples as a reference to integrate ThemeManager into your applications. For more detailed information, see [README.md](README.md) and [API Reference](API_REFERENCE.md).
