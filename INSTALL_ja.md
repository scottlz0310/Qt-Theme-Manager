# ThemeManager インストールガイド

## システム要件

- **Python**: 3.7 以上
- **オペレーティングシステム**: Windows, macOS, Linux
- **Qtフレームワーク**: PyQt5 または PySide6（いずれか一つ）

## インストール手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/scottlz0310/Theme-Manager.git
cd Theme-Manager
```

### 2. 仮想環境の作成（推奨）

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

### 3. 依存関係のインストール

#### PyQt5を使用する場合
```bash
pip install PyQt5>=5.12.0
```

#### PySide6を使用する場合
```bash
pip install PySide6>=6.0.0
```

### 4. インストールの確認

```bash
cd Theme-Manager
python -c "from theme_manager import ThemeController; print('インストール成功')"
```

## 開発者向けインストール

### 開発依存関係のインストール

```bash
pip install pytest>=6.0 pytest-qt>=4.0
```

### setup.pyを使用したインストール

```bash
# 開発モードでインストール
pip install -e .

# PyQt5依存関係を含めてインストール
pip install -e .[pyqt5]

# PySide6依存関係を含めてインストール
pip install -e .[pyside6]

# 開発依存関係を含めてインストール
pip install -e .[dev]
```

## トラブルシューティング

### よくある問題

#### 1. Qtライブラリが見つからない
```
ImportError: No module named 'PyQt5'
```

**解決方法**: PyQt5またはPySide6をインストール
```bash
pip install PyQt5
# または
pip install PySide6
```

#### 2. 設定ファイルが見つからない
```
FileNotFoundError: theme_settings.json not found
```

**解決方法**: 正しいディレクトリからライブラリを実行しているか確認
```bash
cd Theme-Manager
python -m theme_manager.main list
```

#### 3. Python バージョンエラー
```
SyntaxError: invalid syntax
```

**解決方法**: Python 3.7以上を使用していることを確認
```bash
python --version
# または
python3 --version
```

### システム固有の問題

#### Linux（Ubuntu/Debian）
```bash
# PyQt5の場合
sudo apt-get install python3-pyqt5

# PySide6の場合
sudo apt-get install python3-pyside6
```

#### macOS
```bash
# Homebrewを使用
brew install pyqt5
# または
brew install pyside6
```

#### Windows
- PyQt5/PySide6は通常pipで正常にインストールされます
- 問題がある場合は、Anacondaの使用を検討してください

```bash
conda install pyqt5
# または
conda install pyside6
```

## 動作確認

### 基本テスト
```bash
# CLIテスト
python -m theme_manager.main list

# GUIテスト（デスクトップ環境が必要）
python -c "from theme_manager.qt.preview import show_preview; show_preview()"
```

### 完全なテストスイートの実行
```bash
python test_theme_manager.py
```

## 次のステップ

インストールが完了したら：

1. [クイックスタートガイド](README_ja.md#クイックスタート) を確認
2. [API リファレンス](README_ja.md#api-リファレンス) を読む
3. [サンプルコード](examples/) を試す

## サポート

インストールに関する問題がある場合：
- [GitHub Issues](https://github.com/scottlz0310/Theme-Manager/issues) で報告
- インストール環境の詳細（OS、Pythonバージョン、エラーメッセージ）を含めてください
