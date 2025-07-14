# ThemeManager API リファレンス

このドキュメントでは、ThemeManagerライブラリのすべてのAPIについて詳細に説明します。

## 目次

1. [ThemeController](#themecontroller)
2. [ThemeLoader](#themeloader) 
3. [StylesheetGenerator](#stylesheetgenerator)
4. [ユーティリティ関数](#ユーティリティ関数)
5. [設定ファイル仕様](#設定ファイル仕様)
6. [エラーハンドリング](#エラーハンドリング)

## ThemeController

テーマ管理のメインクラスです。

### コンストラクタ

```python
ThemeController(config_path: Optional[Union[str, Path]] = None)
```

**パラメータ:**
- `config_path` (Optional): テーマ設定ファイルのパス。Noneの場合、デフォルトの設定ファイルを使用

**例:**
```python
# デフォルト設定を使用
controller = ThemeController()

# カスタム設定ファイルを使用
controller = ThemeController("/path/to/custom/config.json")
```

### メソッド

#### `get_available_themes() -> Dict[str, Any]`

利用可能なすべてのテーマを取得します。

**戻り値:**
- `Dict[str, Any]`: テーマ名をキーとし、テーマ設定を値とする辞書

**例:**
```python
themes = controller.get_available_themes()
for name, config in themes.items():
    print(f"テーマ: {name}, 表示名: {config.get('display_name')}")
```

#### `get_current_theme_name() -> str`

現在アクティブなテーマ名を取得します。

**戻り値:**
- `str`: 現在のテーマ名

**例:**
```python
current = controller.get_current_theme_name()
print(f"現在のテーマ: {current}")
```

#### `set_theme(theme_name: str, save_settings: bool = True) -> bool`

指定されたテーマに切り替えます。

**パラメータ:**
- `theme_name` (str): 設定するテーマ名
- `save_settings` (bool): 設定をファイルに保存するかどうか（デフォルト: True）

**戻り値:**
- `bool`: 成功した場合True、失敗した場合False

**例:**
```python
# テーマを設定して保存
success = controller.set_theme("dark")

# テーマを設定するが保存しない（一時的）
success = controller.set_theme("light", save_settings=False)
```

#### `apply_theme_to_widget(widget) -> None`

指定されたウィジェットにテーマを適用します。

**パラメータ:**
- `widget`: テーマを適用するQtウィジェット

**例:**
```python
# メインウィンドウにテーマを適用
controller.apply_theme_to_widget(main_window)

# 特定のボタンにテーマを適用
controller.apply_theme_to_widget(my_button)
```

#### `apply_theme_to_application(app=None) -> None`

アプリケーション全体にテーマを適用します。

**パラメータ:**
- `app` (Optional): QApplicationインスタンス。Noneの場合、現在のアプリケーションを使用

**例:**
```python
# 現在のアプリケーションにテーマを適用
controller.apply_theme_to_application()

# 特定のアプリケーションにテーマを適用
controller.apply_theme_to_application(my_app)
```

#### `export_qss(output_path: str, theme_name: Optional[str] = None) -> bool`

QSSスタイルシートをファイルにエクスポートします。

**パラメータ:**
- `output_path` (str): 出力ファイルのパス
- `theme_name` (Optional): エクスポートするテーマ名。Noneの場合、現在のテーマを使用

**戻り値:**
- `bool`: 成功した場合True、失敗した場合False

**例:**
```python
# 現在のテーマをエクスポート
controller.export_qss("current_theme.qss")

# 特定のテーマをエクスポート
controller.export_qss("dark_theme.qss", "dark")
```

## ThemeLoader

テーマ設定の読み込みと保存を担当するクラスです。

### コンストラクタ

```python
ThemeLoader(config_path: Optional[Union[str, Path]] = None)
```

**パラメータ:**
- `config_path` (Optional): 設定ファイルのパス

### メソッド

#### `load_settings() -> Dict[str, Any]`

設定ファイルからテーマ設定を読み込みます。

**戻り値:**
- `Dict[str, Any]`: 読み込まれた設定

**例:**
```python
loader = ThemeLoader()
settings = loader.load_settings()
print(f"設定バージョン: {settings.get('version')}")
```

#### `get_available_themes() -> Dict[str, Any]`

利用可能なテーマの辞書を取得します。

**戻り値:**
- `Dict[str, Any]`: テーマ設定の辞書

#### `get_current_theme() -> str`

現在のテーマ名を取得します。

**戻り値:**
- `str`: 現在のテーマ名

#### `update_current_theme(theme_name: str, save: bool = True) -> bool`

現在のテーマを更新します。

**パラメータ:**
- `theme_name` (str): 新しいテーマ名
- `save` (bool): ファイルに保存するかどうか

**戻り値:**
- `bool`: 成功した場合True

#### `save_settings() -> bool`

現在の設定をファイルに保存します。

**戻り値:**
- `bool`: 成功した場合True

## StylesheetGenerator

QSSスタイルシート生成を担当するクラスです。

### コンストラクタ

```python
StylesheetGenerator(theme_config: Dict[str, Any])
```

**パラメータ:**
- `theme_config` (Dict): テーマ設定辞書

### メソッド

#### `generate_qss() -> str`

完全なQSSスタイルシートを生成します。

**戻り値:**
- `str`: 生成されたQSSスタイルシート

**例:**
```python
generator = StylesheetGenerator(theme_config)
qss = generator.generate_qss()
widget.setStyleSheet(qss)
```

#### `generate_widget_qss(widget_type: str) -> str`

特定のウィジェットタイプ用のQSSを生成します。

**パラメータ:**
- `widget_type` (str): ウィジェットタイプ（'button', 'panel', 'input'など）

**戻り値:**
- `str`: 指定されたウィジェット用のQSSスタイル

**例:**
```python
# ボタン用のQSSのみを生成
button_qss = generator.generate_widget_qss('button')

# パネル用のQSSのみを生成
panel_qss = generator.generate_widget_qss('panel')
```

#### `validate_theme_config(theme_config: Dict[str, Any]) -> bool`

テーマ設定の妥当性を検証します。

**パラメータ:**
- `theme_config` (Dict): 検証するテーマ設定

**戻り値:**
- `bool`: 妥当な場合True

**例:**
```python
is_valid = StylesheetGenerator.validate_theme_config(my_theme_config)
if not is_valid:
    print("テーマ設定に問題があります")
```

## ユーティリティ関数

### `apply_theme_to_widget(widget, theme_name: Optional[str] = None)`

ウィジェットにテーマを適用する便利関数です。

**パラメータ:**
- `widget`: 対象のQtウィジェット
- `theme_name` (Optional): テーマ名。Noneの場合、現在のテーマを使用

**例:**
```python
from theme_manager import apply_theme_to_widget

# 現在のテーマを適用
apply_theme_to_widget(my_widget)

# 特定のテーマを適用
apply_theme_to_widget(my_widget, "dark")
```

### `apply_theme_to_application(theme_name: Optional[str] = None)`

アプリケーション全体にテーマを適用する便利関数です。

**パラメータ:**
- `theme_name` (Optional): テーマ名。Noneの場合、現在のテーマを使用

**例:**
```python
from theme_manager import apply_theme_to_application

# 現在のテーマをアプリケーション全体に適用
apply_theme_to_application()

# 特定のテーマをアプリケーション全体に適用
apply_theme_to_application("blue")
```

## 設定ファイル仕様

### 基本構造

```json
{
  "current_theme": "dark",
  "last_selected_theme": "dark", 
  "theme_switching_enabled": true,
  "remember_theme_choice": true,
  "version": "0.0.1",
  "available_themes": {
    "theme_name": {
      // テーマ設定
    }
  }
}
```

### テーマ設定の構造

```json
{
  "name": "dark",
  "display_name": "ダークモード",
  "description": "暗い背景の低負荷テーマ",
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

### 必須フィールド

- `name`: テーマの内部名
- `backgroundColor`: 背景色
- `textColor`: 基本テキスト色
- `primaryColor`: プライマリ色
- `accentColor`: アクセント色

### オプションフィールド

- `display_name`: 表示用の名前
- `description`: テーマの説明
- `button`: ボタンスタイル設定
- `panel`: パネルスタイル設定
- `input`: 入力欄スタイル設定
- `text`: テキストカラーバリエーション

## エラーハンドリング

### 一般的な例外

#### `FileNotFoundError`
設定ファイルが見つからない場合に発生します。

```python
try:
    controller = ThemeController("/nonexistent/config.json")
except FileNotFoundError:
    print("設定ファイルが見つかりません")
```

#### `json.JSONDecodeError`
設定ファイルのJSONが不正な場合に発生します。

```python
try:
    controller = ThemeController()
except json.JSONDecodeError:
    print("設定ファイルのJSONが不正です")
```

#### `KeyError`
必須のテーマ設定が不足している場合に発生します。

```python
try:
    controller.set_theme("nonexistent_theme")
except KeyError:
    print("指定されたテーマが存在しません")
```

### エラーハンドリングの例

```python
from theme_manager.qt.controller import ThemeController
import json

def safe_theme_setup():
    try:
        controller = ThemeController()
        
        # テーマの存在確認
        available_themes = controller.get_available_themes()
        if "dark" in available_themes:
            success = controller.set_theme("dark")
            if success:
                print("テーマを正常に設定しました")
            else:
                print("テーマの設定に失敗しました")
        else:
            print("指定されたテーマが利用できません")
            
    except FileNotFoundError:
        print("設定ファイルが見つかりません")
    except json.JSONDecodeError:
        print("設定ファイルの形式が正しくありません")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")

# 使用例
safe_theme_setup()
```

## パフォーマンス考慮事項

### ベストプラクティス

1. **ThemeControllerの再利用**: アプリケーション内で同一のThemeControllerインスタンスを再利用する
2. **テーマ適用の最適化**: 大量のウィジェットがある場合、親ウィジェットにのみテーマを適用する
3. **設定の一括更新**: 複数のテーマ変更を行う場合、`save_settings=False`を使用して最後にまとめて保存する

### 例

```python
# 効率的なテーマ管理
class MyApp:
    def __init__(self):
        self.theme_controller = ThemeController()  # 1回だけ作成
        
    def setup_ui(self):
        # 親ウィジェットにのみ適用
        self.theme_controller.apply_theme_to_widget(self.main_window)
        
    def batch_theme_changes(self):
        # 一括変更（保存は最後のみ）
        self.theme_controller.set_theme("dark", save_settings=False)
        # ... 他の設定変更 ...
        self.theme_controller.save_settings()  # 最後に保存
```

このAPIリファレンスを参考に、ThemeManagerライブラリを効率的に活用してください。
