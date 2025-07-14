# ThemeManager Installation Guide

## System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, Linux
- **Qt Framework**: PyQt5 or PySide6 (either one)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/scottlz0310/Theme-Manager.git
cd Theme-Manager
```

### 2. Create Virtual Environment (Recommended)

#### Windows
```bash
python -m venv theme_manager_env
theme_manager_env\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv theme_manager_env
source theme_manager_env/bin/activate
```

### 3. Install Dependencies

#### For PyQt5
```bash
pip install PyQt5>=5.12.0
```

#### For PySide6
```bash
pip install PySide6>=6.0.0
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
