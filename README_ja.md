# Qt-Theme-Manager for PyQt5/PyQt6/PySide6

[![CI/CD Tests](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml/badge.svg)](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml)
[![PyPI version](https://badge.fury.io/py/qt-theme-manager.svg)](https://badge.fury.io/py/qt-theme-manager)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qt-theme-manager)](https://pypi.org/project/qt-theme-manager/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

PyQt5/PyQt6/PySide6アプリケーション用の**純粋なテーマ管理ライブラリ**。Qt フレームワークの自動検出、動的テーマ切り替え、16以上の組み込みテーマを提供。**v1.0.1 - プロダクション対応！**

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
uv add qt-theme-manager --group pyside6

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

## インストール

### オプション1: uvを使用（推奨）

```bash
# 基本インストール
uv add qt-theme-manager

# 好みのQtフレームワークと一緒にインストール
uv add qt-theme-manager --group pyside6    # PySide6用（推奨）
uv add qt-theme-manager --group pyqt6      # PyQt6用
uv add qt-theme-manager --group pyqt5      # PyQt5用

# 開発依存関係も含めてインストール
uv add qt-theme-manager --group dev
```

### オプション2: pipを使用

```bash
# 基本インストール
pip install qt-theme-manager

# 好みのQtフレームワークと一緒にインストール
pip install qt-theme-manager[pyside6]    # PySide6用（推奨）
pip install qt-theme-manager[pyqt6]      # PyQt6用
pip install qt-theme-manager[pyqt5]      # PyQt5用
```

### オプション3: ソースからインストール（開発者向け）

```bash
git clone https://github.com/scottlz0310/Qt-Theme-Manager.git
cd Qt-Theme-Manager

# uvを使用
uv sync --group dev

# または従来の方法
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または: venv\Scripts\activate  # Windows

pip install -e .[dev]
```

### 要件

- Python 3.9+
- PyQt5、PyQt6、またはPySide6（GUI機能用）

## クイックスタート

### 基本的な使用方法

```python
from qt_theme_manager.qt.controller import apply_theme_to_widget
from PyQt5.QtWidgets import QApplication, QMainWindow

app = QApplication([])
window = QMainWindow()

# ウィジェットに現在のテーマを適用
apply_theme_to_widget(window)

window.show()
app.exec_()
```

### ThemeControllerの使用

```python
from qt_theme_manager.qt.controller import ThemeController

# テーマコントローラーを初期化
controller = ThemeController()

# 利用可能なテーマを取得
themes = controller.get_available_themes()
print("利用可能なテーマ:", list(themes.keys()))

# テーマを切り替え
controller.set_theme("dark")

# アプリケーションに適用
controller.apply_theme_to_application()
```

## コマンドラインインターフェース

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

## 利用可能なテーマ

ライブラリには16の組み込みテーマが含まれています：

### コアテーマ
- **light** - 明るい背景のライトモード
- **dark** - 目に優しい色のダークモード
- **high_contrast** - アクセシビリティ用の高コントラスト

### カラーテーマ
- **blue** - プロフェッショナルなブルーベースのテーマ
- **green** - 自然なグリーンベースのテーマ
- **purple** - エレガントなパープルベースのテーマ
- **orange** - 暖かいオレンジベースのテーマ
- **pink** - 遊び心のあるピンクベースのテーマ
- **red** - 大胆なレッドベースのテーマ
- **teal** - 落ち着いたティールベースのテーマ
- **yellow** - 明るいイエローベースのテーマ
- **gray** - シンプルなグレーベースのテーマ
- **sepia** - 目に優しいセピアテーマ
- **cyberpunk** - ネオンサイバーパンクテーマ
- **forest** - 自然な森のテーマ
- **ocean** - 深い海のブルーテーマ

## 設定

テーマは `config/theme_settings.json` で定義されています。各テーマには以下が含まれます：

- **基本色**: background、text、primary、accent
- **コンポーネントスタイル**: buttons、inputs、panels、toolbars
- **テキストバリエーション**: primary、secondary、muted、success、warning、error

### テーマ設定の例

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

## 高度な使用方法

### カスタムテーマ設定

```python
from qt_theme_manager.qt.controller import ThemeController

# カスタム設定ファイルを使用
controller = ThemeController("/path/to/custom/config.json")
```

### 手動QSS生成

```python
from qt_theme_manager.qt.stylesheet import StylesheetGenerator

theme_config = {...}  # あなたのテーマ設定
generator = StylesheetGenerator(theme_config)

# 完全なスタイルシートを生成
qss = generator.generate_qss()

# 特定のウィジェットスタイルを生成
button_qss = generator.generate_widget_qss('button')
```

## プロジェクト構造

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

## テスト

機能を確認するためにテストスイートを実行：

```bash
# uvを使用
uv run pytest

# または従来の方法
python test_qt_theme_manager.py
```

これにより以下がテストされます：
- テーマの読み込みと設定
- スタイルシート生成
- テーマ切り替え
- CLI機能
- QSSエクスポート

## API リファレンス

### ThemeController

テーマ管理のメインクラス。

#### メソッド

- `get_available_themes()` - 利用可能な全テーマを取得
- `get_current_theme_name()` - 現在アクティブなテーマを取得
- `set_theme(theme_name, save_settings=True)` - 指定されたテーマに切り替え
- `apply_theme_to_widget(widget)` - 特定のウィジェットにテーマを適用
- `apply_theme_to_application(app=None)` - アプリケーション全体にテーマを適用
- `export_qss(output_path, theme_name=None)` - QSSをファイルにエクスポート

### ThemeLoader

テーマ設定の読み込みと保存を処理。

#### メソッド

- `load_settings()` - ファイルからテーマ設定を読み込み
- `get_available_themes()` - 利用可能なテーマ辞書を取得
- `get_current_theme()` - 現在のテーマ名を取得
- `update_current_theme(theme_name)` - 現在のテーマを更新・保存

### StylesheetGenerator

テーマ設定からQSSスタイルシートを生成。

#### メソッド

- `generate_qss()` - 完全なQSSスタイルシートを生成
- `generate_widget_qss(widget_type)` - 特定のウィジェットタイプ用QSSを生成
- `validate_theme_config(theme_config)` - テーマ設定を検証

## ライセンス

[ライセンス情報をここに追加]

## 貢献

[貢献ガイドラインをここに追加]

## 変更履歴

### バージョン 0.0.1（初回リリース）
- 基本的なテーマ管理機能
- 16の組み込みテーマ
- CLIインターフェース
- GUIプレビューウィンドウ
- QSSエクスポート機能
