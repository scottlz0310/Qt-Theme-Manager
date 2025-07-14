# ThemeManager 使用例とサンプルコード

このドキュメントでは、ThemeManagerライブラリの様々な使用方法を具体例とともに説明します。

## 目次

1. [基本的な使用方法](#基本的な使用方法)
2. [アプリケーション例](#アプリケーション例)
3. [カスタムテーマ作成](#カスタムテーマ作成)
4. [CLI使用例](#cli使用例)
5. [高度な使用方法](#高度な使用方法)

## 基本的な使用方法

### 1. 最小限のアプリケーション

```python
#!/usr/bin/env python3
"""
最小限のThemeManagerアプリケーション例
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from theme_manager.qt.controller import apply_theme_to_widget

class MinimalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("最小限のテーマアプリ")
        
        # 中央ウィジェット
        label = QLabel("Hello, ThemeManager!")
        self.setCentralWidget(label)
        
        # テーマを適用
        apply_theme_to_widget(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinimalApp()
    window.show()
    sys.exit(app.exec_())
```

### 2. テーマ切り替えボタン付きアプリ

```python
#!/usr/bin/env python3
"""
テーマ切り替えボタン付きアプリケーション例
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel, QComboBox
)
from theme_manager.qt.controller import ThemeController

class ThemeSwitcherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = ThemeController()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("テーマ切り替えアプリ")
        
        # 中央ウィジェット
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 現在のテーマ表示
        self.current_theme_label = QLabel()
        self.update_theme_label()
        layout.addWidget(self.current_theme_label)
        
        # テーマ選択コンボボックス
        self.theme_combo = QComboBox()
        themes = self.controller.get_available_themes()
        for theme_name in themes.keys():
            display_name = themes[theme_name].get("display_name", theme_name)
            self.theme_combo.addItem(f"{display_name} ({theme_name})", theme_name)
        
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        layout.addWidget(self.theme_combo)
        
        # サンプルボタン
        sample_button = QPushButton("サンプルボタン")
        layout.addWidget(sample_button)
        
        self.setCentralWidget(central_widget)
        
        # 初期テーマを適用
        self.controller.apply_theme_to_widget(self)
        
    def update_theme_label(self):
        current_theme = self.controller.get_current_theme_name()
        themes = self.controller.get_available_themes()
        display_name = themes.get(current_theme, {}).get("display_name", current_theme)
        self.current_theme_label.setText(f"現在のテーマ: {display_name}")
        
    def on_theme_changed(self):
        theme_data = self.theme_combo.currentData()
        if theme_data:
            self.controller.set_theme(theme_data)
            self.controller.apply_theme_to_widget(self)
            self.update_theme_label()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThemeSwitcherApp()
    window.show()
    sys.exit(app.exec_())
```

## アプリケーション例

### 3. 完全なGUIアプリケーション

```python
#!/usr/bin/env python3
"""
完全なGUIアプリケーション例
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QGroupBox, 
    QListWidget, QMenuBar, QToolBar, QStatusBar, QAction
)
from PyQt5.QtCore import Qt
from theme_manager.qt.controller import ThemeController

class FullGuiApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = ThemeController()
        self.setup_ui()
        self.create_menu()
        self.create_toolbar()
        self.create_status_bar()
        
    def setup_ui(self):
        self.setWindowTitle("完全なGUIアプリケーション")
        self.setGeometry(100, 100, 800, 600)
        
        # 中央ウィジェット
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # 左側: 入力エリア
        left_group = QGroupBox("入力エリア")
        left_layout = QVBoxLayout(left_group)
        
        left_layout.addWidget(QLabel("名前:"))
        self.name_input = QLineEdit()
        left_layout.addWidget(self.name_input)
        
        left_layout.addWidget(QLabel("メッセージ:"))
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(100)
        left_layout.addWidget(self.message_input)
        
        add_button = QPushButton("追加")
        add_button.clicked.connect(self.add_item)
        left_layout.addWidget(add_button)
        
        main_layout.addWidget(left_group)
        
        # 右側: リスト表示
        right_group = QGroupBox("メッセージリスト")
        right_layout = QVBoxLayout(right_group)
        
        self.message_list = QListWidget()
        right_layout.addWidget(self.message_list)
        
        clear_button = QPushButton("クリア")
        clear_button.clicked.connect(self.clear_list)
        right_layout.addWidget(clear_button)
        
        main_layout.addWidget(right_group)
        
        self.setCentralWidget(central_widget)
        
        # テーマを適用
        self.controller.apply_theme_to_widget(self)
        
    def create_menu(self):
        menubar = self.menuBar()
        
        # ファイルメニュー
        file_menu = menubar.addMenu("ファイル")
        
        new_action = QAction("新規", self)
        file_menu.addAction(new_action)
        
        open_action = QAction("開く", self)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("終了", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # テーマメニュー
        theme_menu = menubar.addMenu("テーマ")
        
        themes = self.controller.get_available_themes()
        for theme_name, theme_config in themes.items():
            display_name = theme_config.get("display_name", theme_name)
            action = QAction(display_name, self)
            action.triggered.connect(lambda checked, name=theme_name: self.change_theme(name))
            theme_menu.addAction(action)
        
    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        add_action = QAction("追加", self)
        add_action.triggered.connect(self.add_item)
        toolbar.addAction(add_action)
        
        clear_action = QAction("クリア", self)
        clear_action.triggered.connect(self.clear_list)
        toolbar.addAction(clear_action)
        
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("準備完了")
        
    def add_item(self):
        name = self.name_input.text()
        message = self.message_input.toPlainText()
        
        if name and message:
            item_text = f"{name}: {message}"
            self.message_list.addItem(item_text)
            self.name_input.clear()
            self.message_input.clear()
            self.status_bar.showMessage(f"メッセージを追加しました: {name}")
        else:
            self.status_bar.showMessage("名前とメッセージを入力してください")
            
    def clear_list(self):
        self.message_list.clear()
        self.status_bar.showMessage("リストをクリアしました")
        
    def change_theme(self, theme_name):
        self.controller.set_theme(theme_name)
        self.controller.apply_theme_to_widget(self)
        self.status_bar.showMessage(f"テーマを '{theme_name}' に変更しました")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FullGuiApp()
    window.show()
    sys.exit(app.exec_())
```

## カスタムテーマ作成

### 4. カスタムテーマの作成と使用

```python
#!/usr/bin/env python3
"""
カスタムテーマの作成例
"""

import json
import tempfile
import os
from theme_manager.qt.controller import ThemeController

# カスタムテーマ設定
custom_theme_config = {
    "current_theme": "custom_purple",
    "last_selected_theme": "custom_purple",
    "theme_switching_enabled": True,
    "remember_theme_choice": True,
    "version": "0.0.1",
    "available_themes": {
        "custom_purple": {
            "name": "custom_purple",
            "display_name": "カスタムパープル",
            "description": "独自のパープルテーマ",
            "primaryColor": "#6B46C1",
            "accentColor": "#A855F7",
            "backgroundColor": "#1F1B24",
            "textColor": "#E5E7EB",
            "button": {
                "background": "#6B46C1",
                "text": "#FFFFFF",
                "hover": "#A855F7",
                "pressed": "#553C9A",
                "border": "#9333EA"
            },
            "panel": {
                "background": "#2D1B3D",
                "border": "#6B46C1",
                "header": {
                    "background": "#553C9A",
                    "text": "#FFFFFF",
                    "border": "#9333EA"
                }
            }
        }
    }
}

def create_custom_theme_demo():
    # 一時ファイルにカスタム設定を保存
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(custom_theme_config, f, indent=2, ensure_ascii=False)
        custom_config_path = f.name
    
    try:
        # カスタム設定でThemeControllerを初期化
        controller = ThemeController(custom_config_path)
        
        # 利用可能なテーマを表示
        themes = controller.get_available_themes()
        print("カスタムテーマが利用可能:")
        for name, config in themes.items():
            print(f"  - {config['display_name']} ({name})")
        
        # QSSを生成してファイルに出力
        output_path = "custom_purple_theme.qss"
        success = controller.export_qss(output_path, "custom_purple")
        
        if success:
            print(f"カスタムテーマのQSSを {output_path} にエクスポートしました")
        
        return controller
        
    finally:
        # 一時ファイルを削除
        os.unlink(custom_config_path)

if __name__ == "__main__":
    create_custom_theme_demo()
```

## CLI使用例

### 5. CLIコマンドの使用方法

```bash
# 利用可能なテーマを一覧表示
python -m theme_manager.main list

# 出力例:
# Available themes:
# --------------------------------------------------
#   dark (current)
#     Display Name: ダークモード
#     Description: 暗い背景の低負荷テーマ
#
#   light
#     Display Name: ライトモード
#     Description: 明るい背景のクリーンテーマ

# テーマを変更
python -m theme_manager.main set light

# 現在のテーマを確認
python -m theme_manager.main current

# QSSをファイルにエクスポート
python -m theme_manager.main export dark my_dark_theme.qss
```

## 高度な使用方法

### 6. プログラマティックなテーマ管理

```python
#!/usr/bin/env python3
"""
高度なテーマ管理の例
"""

from theme_manager.qt.controller import ThemeController
from theme_manager.qt.stylesheet import StylesheetGenerator
from theme_manager.qt.loader import ThemeLoader

class AdvancedThemeManager:
    def __init__(self):
        self.controller = ThemeController()
        self.loader = ThemeLoader()
        
    def get_theme_statistics(self):
        """テーマの統計情報を取得"""
        themes = self.controller.get_available_themes()
        
        stats = {
            "total_themes": len(themes),
            "dark_themes": 0,
            "light_themes": 0,
            "color_themes": 0
        }
        
        for name, config in themes.items():
            if "dark" in name:
                stats["dark_themes"] += 1
            elif "light" in name:
                stats["light_themes"] += 1
            else:
                stats["color_themes"] += 1
                
        return stats
    
    def generate_theme_report(self):
        """テーマレポートを生成"""
        themes = self.controller.get_available_themes()
        current = self.controller.get_current_theme_name()
        
        report = f"テーマレポート\n{'='*50}\n"
        report += f"現在のテーマ: {current}\n"
        report += f"利用可能なテーマ数: {len(themes)}\n\n"
        
        for name, config in themes.items():
            report += f"テーマ: {name}\n"
            report += f"  表示名: {config.get('display_name', 'N/A')}\n"
            report += f"  説明: {config.get('description', 'N/A')}\n"
            report += f"  背景色: {config.get('backgroundColor', 'N/A')}\n"
            report += f"  テキスト色: {config.get('textColor', 'N/A')}\n"
            report += "-" * 30 + "\n"
            
        return report
    
    def create_theme_preview_qss(self, theme_name):
        """特定のテーマのプレビュー用QSSを生成"""
        themes = self.controller.get_available_themes()
        if theme_name not in themes:
            return None
            
        theme_config = themes[theme_name]
        generator = StylesheetGenerator(theme_config)
        
        # 基本的なプレビュー用QSSを生成
        preview_qss = f"""
/* {theme_config.get('display_name', theme_name)} テーマプレビュー */
{generator.generate_qss()}

/* 追加のプレビュー用スタイル */
.preview-container {{
    background-color: {theme_config.get('backgroundColor', '#ffffff')};
    color: {theme_config.get('textColor', '#000000')};
    padding: 10px;
    border: 2px solid {theme_config.get('accentColor', '#0078d4')};
}}
"""
        return preview_qss

def main():
    manager = AdvancedThemeManager()
    
    # 統計情報を表示
    stats = manager.get_theme_statistics()
    print("テーマ統計:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*50)
    
    # レポートを生成
    report = manager.generate_theme_report()
    print(report)
    
    # プレビューQSSを生成
    preview_qss = manager.create_theme_preview_qss("dark")
    if preview_qss:
        with open("dark_theme_preview.qss", "w", encoding="utf-8") as f:
            f.write(preview_qss)
        print("プレビューQSSを dark_theme_preview.qss に保存しました")

if __name__ == "__main__":
    main()
```

### 7. テーマ切り替えアニメーション付きアプリ

```python
#!/usr/bin/env python3
"""
テーマ切り替えアニメーション付きアプリケーション例
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel, QGraphicsOpacityEffect
)
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtSlot
from theme_manager.qt.controller import ThemeController

class AnimatedThemeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = ThemeController()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("アニメーション付きテーマ切り替え")
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # テーマ表示ラベル
        self.theme_label = QLabel("現在のテーマ")
        self.theme_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.theme_label)
        
        # テーマ切り替えボタン
        themes = ["dark", "light", "blue", "green"]
        for theme in themes:
            button = QPushButton(f"{theme.capitalize()} テーマ")
            button.clicked.connect(lambda checked, t=theme: self.change_theme_animated(t))
            layout.addWidget(button)
            
        self.setCentralWidget(central_widget)
        
        # 初期テーマを適用
        self.controller.apply_theme_to_widget(self)
        self.update_theme_label()
        
        # オパシティエフェクトを設定
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
    def update_theme_label(self):
        current_theme = self.controller.get_current_theme_name()
        themes = self.controller.get_available_themes()
        display_name = themes.get(current_theme, {}).get("display_name", current_theme)
        self.theme_label.setText(f"現在のテーマ: {display_name}")
        
    def change_theme_animated(self, theme_name):
        # フェードアウトアニメーション
        self.fade_out_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out_animation.setDuration(200)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.3)
        self.fade_out_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_out_animation.finished.connect(lambda: self.apply_theme_and_fade_in(theme_name))
        self.fade_out_animation.start()
        
    @pyqtSlot()
    def apply_theme_and_fade_in(self, theme_name):
        # テーマを適用
        self.controller.set_theme(theme_name)
        self.controller.apply_theme_to_widget(self)
        self.update_theme_label()
        
        # フェードインアニメーション
        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(200)
        self.fade_in_animation.setStartValue(0.3)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InCubic)
        self.fade_in_animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimatedThemeApp()
    window.show()
    sys.exit(app.exec_())
```

これらの例を参考に、あなたのアプリケーションにThemeManagerを統合してください。より詳細な情報については、[README_ja.md](README_ja.md) および [API リファレンス](README_ja.md#api-リファレンス) をご確認ください。
