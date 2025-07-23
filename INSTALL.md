# Qt-Theme-Manager Installation Guide

## What's New in v0.2.3

After installation, you can now use these GUI tools directly:

```bash
theme-editor    # Launch the advanced theme editor
theme-preview   # Launch theme preview window
theme-manager   # CLI theme management tools
```

## System Requirements

- **Python**: 3.9 or higher (Python 3.8 support ended)
- **Operating System**: Windows, macOS, Linux
- **Qt Framework**: PyQt5, PyQt6, or PySide6 (required for GUI tools)

## Installation Options

### Option 1: Install from PyPI (Recommended)

#### Quick Installation with GUI Tools
```bash
# Install with PyQt6 (recommended for new projects)
pip install qt-theme-manager[pyqt6]

# Then use GUI tools:
theme-editor    # Advanced theme editor
theme-preview   # Theme preview window
```

#### Framework-Specific Installation
```bash
# Install with your preferred Qt framework
pip install qt-theme-manager[pyqt6]    # For PyQt6
pip install qt-theme-manager[pyqt5]    # For PyQt5
pip install qt-theme-manager[pyside6]  # For PySide6

# Install with all Qt frameworks
pip install qt-theme-manager[all]
```

#### Basic Installation (No GUI Tools)
```bash
# Basic installation with automatic Qt framework detection
pip install qt-theme-manager
# Note: GUI tools require a Qt framework to be installed separately
```

### Option 2: Install from Source (For Developers)

#### 1. Clone the Repository

```bash
git clone https://github.com/scottlz0310/Qt-Theme-Manager.git
cd Qt-Theme-Manager
```

#### 2. Create Virtual Environment (Recommended)

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install in Development Mode

```bash
# Install with your preferred Qt framework
pip install -e .[pyqt6]    # For PyQt6
pip install -e .[pyqt5]    # For PyQt5
pip install -e .[pyside6]  # For PySide6

# Or install with all frameworks
pip install -e .[all]
```

### 4. Verify Installation

```bash
cd Theme-Manager
python -c "from theme_manager import ThemeController; print('Installation successful')"
```

## Developer Installation

### Install Development Dependencies

```bash
pip install pytest>=6.0 pytest-qt>=4.0
```

### Install using setup.py

```bash
# Install in development mode
pip install -e .

# Install with PyQt5 dependencies
pip install -e .[pyqt5]

# Install with PySide6 dependencies
pip install -e .[pyside6]

# Install with development dependencies
pip install -e .[dev]
```

## Troubleshooting

### Common Issues

#### 1. Qt Library Not Found
```
ImportError: No module named 'PyQt5'
```

**Solution**: Install PyQt5 or PySide6
```bash
pip install PyQt5
# or
pip install PySide6
```

#### 2. Configuration File Not Found
```
FileNotFoundError: theme_settings.json not found
```

**Solution**: Make sure you're running the library from the correct directory
```bash
cd Theme-Manager
python -m theme_manager.main list
```

#### 3. Python Version Error
```
SyntaxError: invalid syntax
```

**Solution**: Ensure you're using Python 3.7 or higher
```bash
python --version
# or
python3 --version
```

### System-Specific Issues

#### Linux (Ubuntu/Debian)
```bash
# For PyQt5
sudo apt-get install python3-pyqt5

# For PySide6
sudo apt-get install python3-pyside6
```

#### macOS
```bash
# Using Homebrew
brew install pyqt5
# or
brew install pyside6
```

#### Windows
- PyQt5/PySide6 usually install correctly via pip
- If you encounter issues, consider using Anaconda

```bash
conda install pyqt5
# or
conda install pyside6
```

## Verification

### Basic Test
```bash
# CLI test
python -m theme_manager.main list

# GUI test (requires desktop environment)
python -c "from theme_manager.qt.preview import show_preview; show_preview()"
```

### Run Complete Test Suite
```bash
python test_theme_manager.py
```

## Next Steps

After installation is complete:

1. Check the [Quick Start Guide](README.md#quick-start)
2. Read the [API Reference](API_REFERENCE.md)
3. Try the [Example Code](EXAMPLES.md)

## Support

If you encounter installation issues:
- Report on [GitHub Issues](https://github.com/scottlz0310/Theme-Manager/issues)
- Include details about your environment (OS, Python version, error messages)
