# Qt-Theme-Manager for PyQt5/PyQt6/PySide6

[![CI/CD Tests](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml/badge.svg)](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml)
[![PyPI version](https://badge.fury.io/py/qt-theme-manager.svg)](https://badge.fury.io/py/qt-theme-manager)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qt-theme-manager)](https://pypi.org/project/qt-theme-manager/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **pure theme management library** for PyQt5/PyQt6/PySide6 applications with automatic Qt framework detection, providing dynamic theme switching and 16+ built-in themes. **v1.0.1 - Production Ready!**

## 🎯 ライブラリ分離思想

### 背景と目的

Qt-Theme-Managerは、**純粋なライブラリ**として設計されており、テーマ管理の核となる機能に特化しています。この設計思想は、以下の原則に基づいています：

#### 関心の分離による保守性向上
- **ライブラリコア**: テーマ管理、スタイルシート生成、Qt統合機能
- **GUIツール**: テーマエディタ、プレビューアプリケーション（別リポジトリ: qt-theme-studio）
- **明確な責任分界**: 各コンポーネントが独立した責任を持つ

#### 外部開発者の貢献促進
- **シンプルなAPI**: 最小限の依存関係で使いやすいインターフェース
- **モジュラー設計**: 機能ごとに独立したモジュール構造
- **拡張性**: カスタムテーマやプラグインの開発が容易

#### 長期的な持続可能性
- **独立したリリースサイクル**: ライブラリとGUIツールの個別更新
- **軽量な配布**: 必要最小限のファイルサイズ
- **後方互換性**: 既存APIの安定性保証

### 利点

1. **開発効率の向上**: 関心の分離により、各部分の開発・テスト・保守が独立して行える
2. **コードの再利用性**: ライブラリ機能を他のプロジェクトで簡単に利用可能
3. **品質の向上**: 焦点を絞った開発により、より高品質なコードを実現
4. **コミュニティの拡大**: シンプルな構造により、外部開発者の参加が促進される

### アーキテクチャ

```
qt-theme-manager (ライブラリ)
├── qt_theme_manager/          # コアライブラリパッケージ
│   ├── qt/                    # Qt統合モジュール
│   ├── cli/                   # コマンドライン機能
│   └── config/                # 設定管理
└── 最小限の依存関係

qt-theme-studio (GUIツール - 別リポジトリ)
├── テーマエディタ
├── プレビューアプリケーション
├── 高度な編集機能
└── GUI固有の依存関係
```

この分離により、ライブラリユーザーは軽量で高性能なテーマ管理機能を利用でき、GUI機能が必要な場合は別途qt-theme-studioを使用できます。

## ✨ ライブラリ機能

### 🎯 コア機能
- **動的テーマ切り替え**: 実行時のテーマ変更とスタイル適用
- **Qt自動検出**: PySide6 → PyQt6 → PyQt5の自動選択
- **スタイルシート生成**: テーマ設定からQSSの自動生成
- **設定管理**: テーマ設定の永続化と管理
- **CLI機能**: コマンドライン経由でのテーマ操作

### 🔧 技術的特徴
- **軽量設計**: 最小限の依存関係で高性能
- **クロスプラットフォーム**: Windows/macOS/Linux対応
- **マルチフレームワーク**: PyQt5/PyQt6/PySide6サポート
- **後方互換性**: 既存APIの安定性保証
- **Python 3.9+**: モダンなPython環境に最適化

### ♿ アクセシビリティ
- **WCAG準拠**: 科学的な色彩計算による最適なコントラスト
- **縞模様最適化**: 6%明度コントラストによる読みやすさ向上
- **目の疲労軽減**: 長時間使用に配慮した色彩設計

## Features

- 🎨 **16+ Built-in Themes**: Light, Dark, High Contrast, and colorful themes
- 🔄 **Dynamic Theme Switching**: Change themes at runtime without restarting
- 💾 **Persistent Settings**: Theme preferences are automatically saved
- 🎯 **Easy Integration**: Simple API for applying themes to widgets/applications
- ⚡ **QSS Generation**: Automatic stylesheet generation from theme configurations
- 📟 **CLI Support**: Command-line theme management
- ♿ **Accessibility Features**: WCAG-compliant color calculations and contrast optimization
- 🔧 **Qt Auto-Detection**: Automatic framework detection (PySide6/PyQt6/PyQt5)
- 📦 **Lightweight**: Minimal dependencies for optimal performance

## 🚀 30秒クイックスタート

**3行のコードでQt アプリに美しいテーマを追加:**

```python
from qt_theme_manager import apply_theme_to_widget

# ウィジェットに現在のテーマを適用
apply_theme_to_widget(your_widget)
```

**動的なテーマ切り替え:**

```python
from qt_theme_manager import ThemeController

controller = ThemeController()
controller.set_theme("dark")  # "light", "blue", "cyberpunk"など
controller.apply_theme_to_application()
```

**CLIでのテーマ管理:**

```bash
# インストール
pip install qt-theme-manager[pyqt6]

# テーマ一覧表示
qt-theme-manager list

# テーマ切り替え
qt-theme-manager set dark
```

**16の美しいテーマが利用可能:** `dark`, `light`, `blue`, `green`, `cyberpunk`, `ocean`など

### GUIツールについて
テーマエディタやプレビューアプリケーションは、別リポジトリ（**qt-theme-studio**）に移行されました。
ライブラリとしての機能に集中することで、より軽量で高性能なテーマ管理を実現しています。

---

## Installation

### Option 1: Install from PyPI (recommended)

```bash
# Basic installation
pip install qt-theme-manager

# Install with your preferred Qt framework
pip install qt-theme-manager[pyqt6]    # For PyQt6 (recommended)
pip install qt-theme-manager[pyqt5]    # For PyQt5
pip install qt-theme-manager[pyside6]  # For PySide6

# Install with all Qt frameworks
pip install qt-theme-manager[all]
```



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

- Python 3.9+
- PyQt5, PyQt6, or PySide6 (for GUI functionality)

## Quick Start

### Basic Usage

```python
from qt_theme_manager.qt.controller import apply_theme_to_widget
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
from qt_theme_manager.qt.controller import ThemeController

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

### 🖥️ CLI機能

Qt-Theme-Managerは、コマンドライン経由でのテーマ管理をサポートしています：

```bash
# 利用可能なテーマ一覧を表示
qt-theme-manager list

# 現在のテーマを表示
qt-theme-manager current

# テーマを設定
qt-theme-manager set dark

# テーマをQSSファイルにエクスポート
qt-theme-manager export dark dark_theme.qss

# ヘルプを表示
qt-theme-manager --help
```

### 🎨 GUIツールについて（移行済み）

テーマエディタやプレビューアプリケーションなどのGUIツールは、**qt-theme-studio**リポジトリに移行されました：

- **テーマエディタ**: 高度なテーマ作成・編集機能
- **プレビューアプリケーション**: リアルタイムテーマプレビュー
- **Zebraパターンエディタ**: アクセシビリティ対応の縞模様生成

これらのツールを使用する場合は、qt-theme-studioリポジトリをご利用ください。

### ♿ アクセシビリティ機能

ライブラリには以下のアクセシビリティ機能が組み込まれています：

```python
# 縞模様の自動最適化
list_widget.setAlternatingRowColors(True)
controller.apply_theme_to_widget(list_widget)
# WCAG準拠の色彩が自動適用されます
```

### レガシーCLIメソッド

高度なユーザーやスクリプト用：

```bash
# 推奨方法
qt-theme-manager list
qt-theme-manager set dark
qt-theme-manager export dark dark_theme.qss
qt-theme-manager current

# レガシーメソッド
python -m qt_theme_manager.cli.main list
python -m qt_theme_manager.cli.main set dark
python -m qt_theme_manager.main current
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
from qt_theme_manager.qt.controller import ThemeController

# Use custom config file
controller = ThemeController("/path/to/custom/config.json")
```

### Theme Preview Window

```python
from qt_theme_manager.qt.preview import show_preview

# Show interactive preview window
preview_window = show_preview()
```

### Manual QSS Generation

```python
from qt_theme_manager.qt.stylesheet import StylesheetGenerator

theme_config = {...}  # Your theme configuration
generator = StylesheetGenerator(theme_config)

# Generate complete stylesheet
qss = generator.generate_qss()

# Generate specific widget styles
button_qss = generator.generate_widget_qss('button')
```

## Project Structure

```
qt_theme_manager/               # ライブラリコアパッケージ
├── __init__.py                 # パブリックAPI
├── main.py                     # CLIエントリーポイント
├── config/
│   └── theme_settings.json     # テーマ定義
├── qt/                         # Qt統合モジュール
│   ├── __init__.py
│   ├── detection.py            # Qt自動検出
│   ├── loader.py               # 設定ファイル読み込み
│   ├── stylesheet.py           # QSS生成
│   ├── advanced_stylesheet.py  # 高度なスタイル機能
│   └── controller.py           # テーマ管理
└── cli/                        # CLI機能
    ├── __init__.py
    └── themectl.py             # CLIインターフェース
```

### 移行されたGUIツール
以下のGUIツールは**qt-theme-studio**リポジトリに移行されました：
- テーマエディタ
- プレビューアプリケーション
- Zebraパターンエディタ
- 各種起動スクリプト

## Testing

Run the test suite to verify functionality:

```bash
python test_qt_theme_manager.py
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
