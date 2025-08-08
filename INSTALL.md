# Qt-Theme-Manager Library Installation Guide

## 📚 ライブラリ専用インストール

Qt-Theme-Managerは純粋なライブラリとして設計されており、軽量で高性能なテーマ管理機能を提供します。

### 主要機能
- **動的テーマ切り替え**: 実行時のテーマ変更
- **Qt自動検出**: PySide6 → PyQt6 → PyQt5の自動選択
- **スタイルシート生成**: テーマ設定からQSSの自動生成
- **CLI機能**: コマンドライン経由でのテーマ操作
- **軽量設計**: 最小限の依存関係

### GUIツールについて
テーマエディタやプレビューアプリケーションは、別リポジトリ（qt-theme-studio）に移行されました。
ライブラリとしての機能に集中することで、より効率的な開発体験を提供します。

## System Requirements

- **Python**: 3.9 or higher
- **Operating System**: Windows, macOS, Linux
- **Qt Framework**: PyQt5, PyQt6, or PySide6 (自動検出)

## Installation Options

### Option 1: Install from PyPI (推奨)

#### 基本インストール
```bash
# 基本インストール（Qt自動検出）
pip install qt-theme-manager
```

#### フレームワーク指定インストール
```bash
# 特定のQtフレームワークと一緒にインストール
pip install qt-theme-manager[pyqt6]    # PyQt6用
pip install qt-theme-manager[pyqt5]    # PyQt5用
pip install qt-theme-manager[pyside6]  # PySide6用

# 全フレームワーク対応
pip install qt-theme-manager[all]
```

#### 開発者向けインストール
```bash
# 開発依存関係を含む
pip install qt-theme-manager[dev]
```

### Option 2: ソースからのインストール（開発者向け）

#### 1. リポジトリのクローン

```bash
git clone https://github.com/scottlz0310/Qt-Theme-Manager.git
cd Qt-Theme-Manager
```

#### 2. 仮想環境の作成（推奨）

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

#### 3. 開発モードでのインストール

```bash
# 特定のQtフレームワークと一緒にインストール
pip install -e .[pyqt6]    # PyQt6用
pip install -e .[pyqt5]    # PyQt5用
pip install -e .[pyside6]  # PySide6用

# 全フレームワーク対応
pip install -e .[all]

# 開発依存関係を含む
pip install -e .[dev]
```

#### 4. インストールの確認

```bash
python -c "from qt_theme_manager import ThemeController; print('インストール成功')"
```

## ライブラリの使用方法

### 基本的な使用例

```python
from qt_theme_manager import ThemeController, apply_theme_to_widget

# テーマコントローラーの初期化
controller = ThemeController()

# 利用可能なテーマの確認
themes = controller.get_available_themes()
print("利用可能なテーマ:", list(themes.keys()))

# テーマの切り替え
controller.set_theme("dark")

# ウィジェットにテーマを適用
apply_theme_to_widget(your_widget)

# アプリケーション全体にテーマを適用
controller.apply_theme_to_application()
```

### CLIの使用

```bash
# 利用可能なテーマ一覧
qt-theme-manager list

# 現在のテーマを表示
qt-theme-manager current

# テーマの設定
qt-theme-manager set dark

# QSSファイルのエクスポート
qt-theme-manager export dark dark_theme.qss
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
python -m qt_theme_manager.main list
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

### 基本テスト
```bash
# CLIテスト
qt-theme-manager list

# ライブラリテスト
python -c "from qt_theme_manager import ThemeController; print('動作確認OK')"
```

### 完全なテストスイートの実行
```bash
pytest tests/
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
