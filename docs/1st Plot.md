**PyQt5 / PySide6 に特化したテーマ管理ライブラリの仕様書（初期版）**

---

## 📘 ライブラリ仕様書：ThemeManager for PyQt5 / PySide6

### 🧭 概要

**ThemeManager** は、PyQt5 / PySide6 アプリケーション向けに、ダークテーマを含む複数のテーマを管理・適用するためのライブラリです。CLIとGUIの両方から操作可能で、設定ファイルを通じてテーマの永続化と動的切り替えを提供します。

---

### 📦 構成

#### ディレクトリ構成（初期）

```
theme_manager/
├── __init__.py
├── config/
│   └── theme_settings.json         # テーマ定義と状態管理
├── qt/
│   ├── loader.py                   # JSON読み込み
│   ├── stylesheet.py               # QSS生成
│   ├── controller.py               # テーマ切り替え・保存
│   └── preview.py                  # GUIプレビュー（任意）
├── cli/
│   └── themectl.py                 # CLI操作（list, set, export）
└── main.py                         # CLIエントリーポイント
```

---

### 🎨 機能一覧

#### 1. テーマ設定ファイルの読み込み
- `theme_settings.json` を読み込み、利用可能なテーマ一覧を取得。
- 現在のテーマ状態（`current_theme`, `last_selected_theme`）を保持。

#### 2. QSSスタイルの生成
- テーマ定義から PyQt5 / PySide6 用のスタイルシート（QSS）を生成。
- `QWidget`, `QPushButton`, `QLineEdit`, `QListWidget`, `QGroupBox` などの基本スタイルをカバー。

#### 3. テーマの切り替えと保存
- `set_theme(theme_name)` によりテーマを変更。
- `save_settings()` により設定ファイルを更新。

#### 4. CLI操作
- `themectl list`：利用可能なテーマ一覧を表示
- `themectl set <theme>`：テーマを切り替え
- `themectl export <theme>`：QSSをファイル出力

#### 5. GUIプレビュー（任意）
- サンプルウィジェット群を並べたウィンドウで、テーマの見た目を確認。
- `apply_theme_to_widget(widget)` により任意のウィジェットにテーマを適用。

---

### 🧪 設定ファイル仕様（`theme_settings.json`）

### 🔮 将来的な拡張余地

- 他のUIフレームワーク（Tkinter, Kivy, Web）への対応
- アクセシビリティ調整（コントラスト、色覚対応、フォントサイズ）
- GUI設定画面でのスライダーによる動的調整
- テーマのインポート・エクスポート機能
- テーマのプレビュー画像生成

---

### 🛠 使用例（PyQt5）

```python
from theme_manager.qt.controller import apply_theme_to_widget

app = QApplication([])
window = QMainWindow()
apply_theme_to_widget(window)
window.show()
app.exec_()
```

---

この仕様書をベースに、VSCode内で開発を進めていくのが理想的です。  
必要であれば、Markdown形式で保存できるようにファイル化もできますよ。どうしますか？