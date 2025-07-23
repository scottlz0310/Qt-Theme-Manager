# Qt-Theme-Manager for PyQt5/PyQt6/PySide6

[![CI/CD Tests](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml/badge.svg)](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml)
[![PyPI version](https://badge.fury.io/py/qt-theme-manager.svg)](https://badge.fury.io/py/qt-theme-manager)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qt-theme-manager)](https://pypi.org/project/qt-theme-manager/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

PyQt5/PyQt6/PySide6アプリケーション向けの包括的なテーマ管理ライブラリです。高度なテーマエディターと16種類以上の内蔵テーマで動的なテーマ切り替えを提供します。

## ✨ v0.2.3の新機能

- 🎨 **CLIプレビュー機能強化**: `--config`と`--theme`オプション対応
- ♿ **アクセシビリティ大幅改善**: 6%ライトネス差のゼブラスタイル（WCAG対応）
- 🔄 **テーマフォーマット変換**: カスタムテーマ→Qt-Theme-Manager形式変換
- 📊 **16テーマの統一改善**: 全テーマでアクセシビリティ最適化
- 🚀 **エントリーポイント追加**: `theme-editor`、`theme-preview`コマンドで簡単起動
- 🐍 **Python 3.9+サポート**: Python 3.8サポート終了、モダンな環境に最適化

## ✨ v0.2.1の新機能

- 🔧 **GUI起動問題の完全解決**: すべてのQtフレームワークでテーマエディターが確実に起動
- ⚙️ **Qt互換性の向上**: PyQt5、PyQt6、PySide6の完全サポート  
- 🚀 **起動方法の改善**: モジュール実行とスクリプト実行の両方が完璧に動作
- 📦 **エラーハンドリングの改善**: よりクリアなエラーメッセージと中断サポート

## 特徴

- 🎨 **16種類以上の内蔵テーマ**: ライト、ダーク、ハイコントラスト、カラフルなテーマ
- ✨ **高度なテーマエディター**: プロ仕様のテーマ作成ツール
- 🔄 **動的テーマ切り替え**: 再起動なしでリアルタイムにテーマを変更
- 💾 **永続的な設定**: テーマの設定は自動的に保存されます
- 🖥️ **GUIツール**: インタラクティブなエディターとプレビューアプリケーション
- 📟 **CLIサポート**: テーマ管理用のコマンドラインインターフェース
- 🎯 **簡単な統合**: ウィジェット/アプリケーションにテーマを適用する簡単なAPI
- ⚡ **QSS生成**: テーマ設定からスタイルシートを自動生成

## 🚀 30秒クイックスタート

**新しいテーマエディターを試してみたい？**

```bash
# インストールしてテーマエディターを起動（新しいエントリーポイント！）
pip install qt-theme-manager[pyqt6]
theme-editor

# 代替起動方法（すべて確実に動作します）：
python -m theme_manager.qt.theme_editor
python launch_theme_editor.py  # リポジトリをクローンした場合
```

**たった3行でQtアプリに美しいテーマを追加したい？**

```python
from theme_manager.qt.controller import apply_theme_to_widget

# これだけ！任意のウィジェットに現在のテーマを適用:
apply_theme_to_widget(your_widget)
```

**動的にテーマを切り替えたい？**

```python
from theme_manager.qt.controller import ThemeController

controller = ThemeController()
controller.set_theme("dark")  # または "light", "blue", "cyberpunk" など
controller.apply_theme_to_application()
```

**16種類の美しいテーマがすぐに使用可能:** `dark`, `light`, `blue`, `green`, `cyberpunk`, `ocean` など！

---

## インストール

### 方法1: PyPIからインストール（推奨）

```bash
# 基本インストール
pip install qt-theme-manager

# お好みのQtフレームワークと一緒にインストール
pip install qt-theme-manager[pyqt6]    # PyQt6の場合
pip install qt-theme-manager[pyqt5]    # PyQt5の場合  
pip install qt-theme-manager[pyside6]  # PySide6の場合

# 全てのQtフレームワーク対応
pip install qt-theme-manager[all]
```

### 方法2: ソースからインストール（開発者向け）

```bash
git clone https://github.com/scottlz0310/Qt-Theme-Manager.git
cd Qt-Theme-Manager

# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または: venv\Scripts\activate  # Windows

# お好みのQtフレームワークでインストール
pip install -e .[pyqt6]    # PyQt6の場合
# pip install -e .[pyqt5]  # PyQt5の場合
# pip install -e .[pyside6] # PySide6の場合
```

### 必要条件

- Python 3.9+ (Python 3.8サポートは終了しました)
- PyQt5、PyQt6、または PySide6（GUI機能用）

## クイックスタート

### 基本的な使用方法

```python
from theme_manager.qt.controller import apply_theme_to_widget
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
from theme_manager.qt.controller import ThemeController

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

### 🎨 高度なテーマエディター

色彩理論とアクセシビリティガイドラインに基づいた高機能なGUIテーマエディターを起動：

```bash
# 新しいエントリーポイント（推奨）
theme-editor

# 従来の方法
python -m theme_manager.qt.theme_editor
```

このテーマエディターの特徴：
- 🎯 **リアルタイムプレビュー**: 色の変更がリアルタイムで反映
- 📊 **WCAGコントラスト計算**: アクセシビリティ基準の自動チェック
- 🤖 **インテリジェント色調整**: 輝度に基づく最適なテキスト色の自動選択
- 🎨 **カラーパレット生成**: 色彩理論に基づく調和のとれた色の自動生成
- 📏 **RGBスライダー**: 直感的な色調整インターフェース
- 💾 **テーマエクスポート**: 作成したテーマをJSONファイルとして保存

### テーマのビジュアルプレビュー

すべてのテーマの外観を確認できるGUIプレビューウィンドウを起動：

```bash
# 新しいエントリーポイント（推奨）
theme-preview

# 従来の方法
python launch_gui_preview.py
```

このプレビューウィンドウでは：
- 16種類すべてのテーマをリアルタイムで切り替え
- 各テーマでのボタン、入力欄、スライダーなどの表示を確認
- テーマの色合いやコントラストを直感的に比較

### 利用可能なテーマを一覧表示

```bash
# 新しいCLIコマンド（推奨）
theme-manager list

# 従来の方法
python -m theme_manager.main list
```

### テーマを設定

```bash
# 新しいCLIコマンド（推奨）
theme-manager set dark

# 従来の方法
python -m theme_manager.main set dark
```

### QSSスタイルシートをエクスポート

```bash
# 新しいCLIコマンド（推奨）
theme-manager export dark dark_theme.qss

# 従来の方法
python -m theme_manager.main export dark dark_theme.qss
```

### 現在のテーマを表示

```bash
# 新しいCLIコマンド（推奨）
theme-manager current

# 従来の方法
python -m theme_manager.main current
```

## 利用可能なテーマ

ライブラリには16種類の内蔵テーマが含まれています：

### 基本テーマ
- **light** - 明るい背景のライトモード
- **dark** - 目に優しい色合いのダークモード  
- **high_contrast** - アクセシビリティ用のハイコントラスト

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
- **ocean** - 深海ブルーテーマ

## 設定

テーマは`config/theme_settings.json`で定義されています。各テーマには以下が含まれます：

- **基本色**: background（背景）、text（テキスト）、primary（プライマリ）、accent（アクセント）
- **コンポーネントスタイル**: ボタン、入力欄、パネル、ツールバー
- **テキストバリエーション**: primary（主要）、secondary（副次）、muted（ミュート）、success（成功）、warning（警告）、error（エラー）

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
from theme_manager.qt.controller import ThemeController

# カスタム設定ファイルを使用
controller = ThemeController("/path/to/custom/config.json")
```

### テーマプレビューウィンドウ

```python
from theme_manager.qt.preview import show_preview

# インタラクティブなプレビューウィンドウを表示
preview_window = show_preview()
```

### 手動QSS生成

```python
from theme_manager.qt.stylesheet import StylesheetGenerator

theme_config = {...}  # あなたのテーマ設定
generator = StylesheetGenerator(theme_config)

# 完全なスタイルシートを生成
qss = generator.generate_qss()

# 特定のウィジェットスタイルを生成
button_qss = generator.generate_widget_qss('button')
```

## プロジェクト構造

```
theme_manager/
├── __init__.py                 # メインパッケージのエクスポート
├── config/
│   └── theme_settings.json     # テーマ定義
├── qt/
│   ├── __init__.py
│   ├── loader.py               # JSON設定ローダー
│   ├── stylesheet.py           # QSS生成
│   ├── controller.py           # テーマ管理
│   └── preview.py              # GUIプレビューウィンドウ
├── cli/
│   ├── __init__.py
│   └── themectl.py             # CLIインターフェース
└── main.py                     # CLIエントリーポイント
```

## テスト

機能を確認するためにテストスイートを実行：

```bash
python test_theme_manager.py
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

- `get_available_themes()` - 利用可能なすべてのテーマを取得
- `get_current_theme_name()` - 現在アクティブなテーマを取得
- `set_theme(theme_name, save_settings=True)` - 指定されたテーマに切り替え
- `apply_theme_to_widget(widget)` - 特定のウィジェットにテーマを適用
- `apply_theme_to_application(app=None)` - アプリケーション全体にテーマを適用
- `export_qss(output_path, theme_name=None)` - QSSをファイルにエクスポート

### ThemeLoader

テーマ設定の読み込みと保存を処理。

#### メソッド

- `load_settings()` - ファイルからテーマ設定を読み込み
- `get_available_themes()` - 利用可能なテーマの辞書を取得
- `get_current_theme()` - 現在のテーマ名を取得
- `update_current_theme(theme_name)` - 現在のテーマを更新して保存

### StylesheetGenerator

テーマ設定からQSSスタイルシートを生成。

#### メソッド

- `generate_qss()` - 完全なQSSスタイルシートを生成
- `generate_widget_qss(widget_type)` - 特定のウィジェットタイプ用のQSSを生成
- `validate_theme_config(theme_config)` - テーマ設定を検証

## ライセンス

MIT License

## コントリビューション

プルリクエストやイシューを歓迎します。コントリビューションガイドラインについては、GitHubリポジトリをご確認ください。

## 変更履歴

### バージョン 0.0.1（初回リリース）
- 基本的なテーマ管理機能
- 16種類の内蔵テーマ
- CLIインターフェース
- GUIプレビューウィンドウ
- QSSエクスポート機能

## サポート

問題が発生した場合や質問がある場合：
- GitHubでイシューを開く
- ドキュメントを確認
- サンプルコードを確認

---

Qt コミュニティのために ❤️ で作成されました
