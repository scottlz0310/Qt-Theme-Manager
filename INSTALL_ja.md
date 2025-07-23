# Qt-Theme-Manager インストールガイド

## v0.2.3の新機能

インストール後、以下のGUIツールが直接使用できます：

```bash
theme-editor    # 高度なテーマエディターを起動
theme-preview   # テーマプレビューウィンドウを起動
theme-manager   # CLIテーマ管理ツール
```

## システム要件

- **Python**: 3.9 以上（Python 3.8のサポートは終了）
- **オペレーティングシステム**: Windows, macOS, Linux
- **Qtフレームワーク**: PyQt5、PyQt6、または PySide6（GUIツールに必要）

## インストール方法

### オプション1: PyPIからのインストール（推奨）

#### GUIツール付きクイックインストール
```bash
# PyQt6と一緒にインストール（新プロジェクト推奨）
pip install qt-theme-manager[pyqt6]

# その後GUIツールを使用:
theme-editor    # 高度なテーマエディター
theme-preview   # テーマプレビューウィンドウ
```

#### フレームワーク指定インストール
```bash
# お好みのQtフレームワークでインストール
pip install qt-theme-manager[pyqt6]    # PyQt6を使用
pip install qt-theme-manager[pyqt5]    # PyQt5を使用
pip install qt-theme-manager[pyside6]  # PySide6を使用

# すべてのQtフレームワークでインストール
pip install qt-theme-manager[all]
```

#### 基本インストール（GUIツールなし）
```bash
# 基本インストール（自動的にQtフレームワークを検出）
pip install qt-theme-manager
# 注意: GUIツールにはQtフレームワークを別途インストールする必要があります
```

### オプション2: ソースからのインストール（開発者向け）

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
# お好みのQtフレームワークでインストール
pip install -e .[pyqt6]    # PyQt6を使用
pip install -e .[pyqt5]    # PyQt5を使用
pip install -e .[pyside6]  # PySide6を使用

# またはすべてのフレームワークでインストール
pip install -e .[all]
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
