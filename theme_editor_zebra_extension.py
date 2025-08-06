#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーマエディター拡張 - ゼブラパターン自動生成機能統合
"""

import json
from pathlib import Path

# 既存のzebra_pattern_editorをインポート
try:
    from zebra_pattern_editor import ZebraPatternEditor, ZebraPatternGenerator

    zebra_editor_available = True
except ImportError:
    zebra_editor_available = False

# 既存のテーマエディターのインポートを試行
try:
    from theme_manager.qt.theme_editor import (
        ColorSliderGroup,
        ThemeEditorWindow,
    )

    theme_editor_available = True
except ImportError:
    theme_editor_available = False

# Qt imports
try:
    from PyQt5.QtCore import Qt, pyqtSignal
    from PyQt5.QtGui import QFont
    from PyQt5.QtWidgets import (
        QCheckBox,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QListWidget,
        QListWidgetItem,
        QPushButton,
        QScrollArea,
        QSpinBox,
        QSplitter,
        QTabWidget,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

    qt_available = True
except ImportError:
    try:
        from PyQt6.QtCore import Qt, pyqtSignal
        from PyQt6.QtGui import QFont
        from PyQt6.QtWidgets import (
            QCheckBox,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QListWidget,
            QListWidgetItem,
            QPushButton,
            QScrollArea,
            QSpinBox,
            QSplitter,
            QTabWidget,
            QTextEdit,
            QVBoxLayout,
            QWidget,
        )

        qt_available = True
    except ImportError:
        try:
            from PySide6.QtCore import Qt
            from PySide6.QtCore import Signal as pyqtSignal
            from PySide6.QtGui import QFont
            from PySide6.QtWidgets import (
                QCheckBox,
                QGroupBox,
                QHBoxLayout,
                QLabel,
                QListWidget,
                QListWidgetItem,
                QPushButton,
                QScrollArea,
                QSpinBox,
                QSplitter,
                QTabWidget,
                QTextEdit,
                QVBoxLayout,
                QWidget,
            )

            qt_available = True
        except ImportError:
            qt_available = False


class ZebraPatternTab(QWidget if qt_available else object):
    """ゼブラパターン生成専用タブ"""

    zebraConfigChanged = pyqtSignal(dict)

    def __init__(self, parent=None):
        if not qt_available:
            raise RuntimeError("Qt framework not available")

        super().__init__(parent)
        self.current_theme_config = {}
        self.current_theme_name = "default"  # デフォルトテーマ名
        self.current_background = "#ffffff"  # デフォルト背景色
        self.zebra_configs = {}  # テーマごとのゼブラ設定
        self.setup_ui()

    def setup_ui(self):
        """UIを設定"""
        layout = QVBoxLayout(self)

        # タイトル
        title = QLabel("🦓 ゼブラパターン自動生成")
        title.setFont(
            QFont(
                "",
                14,
                (
                    QFont.Weight.Bold
                    if hasattr(QFont.Weight, "Bold")
                    else QFont.Bold
                ),
            )
        )
        layout.addWidget(title)

        # 説明
        description = QLabel(
            """
        リスト、ツリー、テーブルウィジェットの交互背景色（ゼブラパターン）を自動生成します。
        コントラスト比を調整して、アクセシビリティと視認性のバランスを最適化できます。
        """
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; margin: 10px 0;")
        layout.addWidget(description)

        # メインコンテンツをスプリッターで分割
        splitter = QSplitter(
            Qt.Orientation.Horizontal
            if hasattr(Qt.Orientation, "Horizontal")
            else Qt.Horizontal
        )
        layout.addWidget(splitter)

        # 左側：ゼブラパターンエディター
        if zebra_editor_available:
            self.zebra_editor = ZebraPatternEditor()
            self.zebra_editor.zebraColorChanged.connect(
                self.on_zebra_color_changed
            )
            splitter.addWidget(self.zebra_editor)
        else:
            # フォールバック：シンプルなコントロール
            self.zebra_editor = self.create_simple_zebra_controls()
            splitter.addWidget(self.zebra_editor)

        # 右側：プレビューとテンプレート
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        # スプリッターの比率設定
        splitter.setSizes([400, 300])

    def create_simple_zebra_controls(self):
        """シンプルなゼブラコントロール（フォールバック）"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # コントラスト調整
        contrast_group = QGroupBox("コントラスト調整")
        contrast_layout = QVBoxLayout(contrast_group)

        contrast_layout.addWidget(QLabel("目標コントラスト比:"))
        self.contrast_spinbox = QSpinBox()
        self.contrast_spinbox.setRange(110, 300)  # 1.10から3.00
        self.contrast_spinbox.setValue(120)  # デフォルト1.20
        self.contrast_spinbox.setSuffix("%")
        self.contrast_spinbox.valueChanged.connect(self.generate_zebra_simple)
        contrast_layout.addWidget(self.contrast_spinbox)

        layout.addWidget(contrast_group)

        # 生成ボタン
        generate_btn = QPushButton("ゼブラ色を生成")
        generate_btn.clicked.connect(self.generate_zebra_simple)
        layout.addWidget(generate_btn)

        layout.addStretch()
        return widget

    def create_right_panel(self):
        """右パネル（プレビューとテンプレート）を作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # ゼブラプレビュー
        preview_group = QGroupBox("プレビュー")
        preview_layout = QVBoxLayout(preview_group)

        # サンプルリスト
        self.preview_list = QListWidget()
        self.preview_list.setAlternatingRowColors(True)
        sample_items = [
            "📁 ドキュメント",
            "📄 プロジェクト計画.docx",
            "📊 データ分析.xlsx",
            "🖼️ プレゼンテーション.pptx",
            "📝 メモ.txt",
            "📋 タスクリスト.md",
            "📈 グラフ.png",
            "📚 リファレンス.pdf",
        ]

        for item_text in sample_items:
            item = QListWidgetItem(item_text)
            self.preview_list.addItem(item)

        self.preview_list.setMaximumHeight(200)
        preview_layout.addWidget(self.preview_list)

        # 設定情報表示
        self.info_display = QTextEdit()
        self.info_display.setMaximumHeight(100)
        self.info_display.setReadOnly(True)
        self.info_display.setPlainText(
            "背景色を設定すると、ゼブラパターンが自動生成されます。"
        )
        preview_layout.addWidget(self.info_display)

        layout.addWidget(preview_group)

        # テンプレート選択
        template_group = QGroupBox("クイックテンプレート")
        template_layout = QVBoxLayout(template_group)

        templates = [
            (
                "subtle",
                "控えめ (1.15:1)",
                "日常使用に適した控えめなコントラスト",
            ),
            ("moderate", "中程度 (1.30:1)", "適度な視認性"),
            ("high", "高コントラスト (1.80:1)", "明確な識別が必要な場合"),
        ]

        for template_id, name, description in templates:
            btn = QPushButton(name)
            btn.setToolTip(description)
            btn.clicked.connect(
                lambda checked, tid=template_id: self.apply_template(tid)
            )
            template_layout.addWidget(btn)

        layout.addWidget(template_group)

        # 全テーマに適用
        apply_group = QGroupBox("適用")
        apply_layout = QVBoxLayout(apply_group)

        self.auto_apply_checkbox = QCheckBox("背景色変更時に自動更新")
        self.auto_apply_checkbox.setChecked(True)
        apply_layout.addWidget(self.auto_apply_checkbox)

        apply_all_btn = QPushButton("全テーマに適用")
        apply_all_btn.clicked.connect(self.apply_to_all_themes)
        apply_layout.addWidget(apply_all_btn)

        layout.addWidget(apply_group)

        layout.addStretch()
        return widget

    def set_background_color(self, color: str):
        """背景色を設定してゼブラパターンを更新"""
        if hasattr(self, "zebra_editor") and hasattr(
            self.zebra_editor, "set_base_color"
        ):
            self.zebra_editor.set_base_color(color)
        else:
            # シンプルなフォールバック
            self.current_background = color
            if self.auto_apply_checkbox.isChecked():
                self.generate_zebra_simple()

    def on_zebra_color_changed(self, zebra_color: str):
        """ゼブラ色変更時の処理"""
        self.update_preview(zebra_color)

        # 設定を更新
        if hasattr(self, "zebra_editor"):
            config = self.zebra_editor.get_zebra_config()
            self.zebra_configs[self.current_theme_name] = config
            self.zebraConfigChanged.emit(config)

    def generate_zebra_simple(self):
        """シンプルなゼブラ生成（フォールバック）"""
        if not hasattr(self, "current_background"):
            return

        if zebra_editor_available:
            target_contrast = self.contrast_spinbox.value() / 100.0
            zebra_color = ZebraPatternGenerator.generate_zebra_color(
                self.current_background, target_contrast, "auto"
            )
            self.update_preview(zebra_color)

            # 設定情報を更新
            contrast_ratio = ZebraPatternGenerator.get_contrast_ratio(
                self.current_background, zebra_color
            )

            info_text = f"""背景色: {self.current_background}
ゼブラ色: {zebra_color}
コントラスト比: {contrast_ratio:.2f}:1
目標比: {target_contrast:.2f}:1"""

            self.info_display.setPlainText(info_text)

    def update_preview(self, zebra_color: str):
        """プレビューを更新"""
        if hasattr(self, "current_background"):
            # リストの背景とゼブラ色を更新
            style = f"""
            QListWidget {{
                background-color: {self.current_background};
                alternate-background-color: {zebra_color};
                border: 1px solid #ccc;
                border-radius: 4px;
            }}
            QListWidget::item {{
                padding: 5px;
                border-bottom: 1px solid transparent;
            }}
            """
            self.preview_list.setStyleSheet(style)

    def apply_template(self, template_id: str):
        """テンプレートを適用"""
        ratios = {"subtle": 115, "moderate": 130, "high": 180}

        if template_id in ratios:
            if hasattr(self, "contrast_spinbox"):
                self.contrast_spinbox.setValue(ratios[template_id])

            if hasattr(self, "zebra_editor") and hasattr(
                self.zebra_editor, "set_accessibility_level"
            ):
                level_map = {
                    "subtle": "subtle",
                    "moderate": "moderate",
                    "high": "high",
                }
                self.zebra_editor.set_accessibility_level(
                    level_map[template_id]
                )

    def apply_to_all_themes(self):
        """全テーマにゼブラ設定を適用"""
        if hasattr(self, "zebra_editor"):
            current_config = self.zebra_editor.get_zebra_config()

            # 現在のテーマ設定ファイルを読み込み
            config_path = Path("theme_manager/config/theme_settings.json")
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)

                # 全テーマにゼブラ設定を適用
                for theme_name, theme_config in config[
                    "available_themes"
                ].items():
                    if "panel" not in theme_config:
                        theme_config["panel"] = {}

                    if "zebra" not in theme_config["panel"]:
                        theme_config["panel"]["zebra"] = {}

                    # 各テーマの背景色に基づいてゼブラ色を生成
                    bg_color = theme_config["panel"].get(
                        "background", "#ffffff"
                    )
                    zebra_color = ZebraPatternGenerator.generate_zebra_color(
                        bg_color,
                        current_config.get("contrast_ratio", 1.2),
                        current_config.get("generation_method", "auto"),
                    )

                    theme_config["panel"]["zebra"]["alternate"] = zebra_color

                # ファイルに保存
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(config, f, ensure_ascii=False, indent=4)

                print(f"✅ 全テーマにゼブラ設定を適用しました")

    def set_theme_config(self, theme_name: str, theme_config: dict):
        """テーマ設定を更新"""
        self.current_theme_name = theme_name
        self.current_theme_config = theme_config

        # 背景色を取得してゼブラエディターに設定
        bg_color = theme_config.get("panel", {}).get("background", "#ffffff")
        self.set_background_color(bg_color)


def extend_theme_editor_with_zebra():
    """テーマエディターにゼブラパターン機能を追加する関数"""

    if not (qt_available and theme_editor_available):
        print("❌ テーマエディターまたはQtが利用できません")
        return None

    # 既存のThemeEditorWindowクラスを拡張
    original_setup_controls_panel = ThemeEditorWindow.setup_controls_panel

    def extended_setup_controls_panel(self, parent):
        """拡張されたコントロールパネル設定"""
        # 元の設定を実行
        original_setup_controls_panel(self, parent)

        # ゼブラパターンタブを追加
        zebra_tab = ZebraPatternTab()
        zebra_tab.zebraConfigChanged.connect(self.on_zebra_config_changed)
        self.tabs.addTab(zebra_tab, "🦓 ゼブラ")

        # 参照を保存
        self.zebra_tab = zebra_tab

    def on_zebra_config_changed(self, config):
        """ゼブラ設定変更時の処理"""
        print(f"🦓 ゼブラ設定が更新されました: {config}")

        # テーマ設定にゼブラ設定を反映
        if "panel" not in self.current_theme_config:
            self.current_theme_config["panel"] = {}

        if "zebra" not in self.current_theme_config["panel"]:
            self.current_theme_config["panel"]["zebra"] = {}

        self.current_theme_config["panel"]["zebra"]["alternate"] = config[
            "zebra_color"
        ]
        print("✅ ゼブラ設定をテーマに適用しました")

    def extended_update_color(self, color_key: str, hex_color: str):
        """拡張された色更新処理"""
        # 元の更新処理を実行
        self.current_theme_config[f"{color_key}Color"] = hex_color

        # 背景色が変更された場合、ゼブラタブを更新
        if color_key == "background" and hasattr(self, "zebra_tab"):
            self.zebra_tab.set_background_color(hex_color)

        print(f"✅ 色を更新しました: {color_key} = {hex_color}")

    # メソッドを置き換え
    ThemeEditorWindow.setup_controls_panel = extended_setup_controls_panel
    ThemeEditorWindow.on_zebra_config_changed = on_zebra_config_changed
    ThemeEditorWindow.update_color = extended_update_color

    print("✅ テーマエディターにゼブラパターン機能を統合しました")
    return ThemeEditorWindow


if __name__ == "__main__":
    """テスト実行"""
    import sys

    if qt_available:
        try:
            from PyQt5.QtWidgets import QApplication
        except ImportError:
            try:
                from PyQt6.QtWidgets import QApplication
            except ImportError:
                from PySide6.QtWidgets import QApplication

        app = QApplication(sys.argv)

        # 拡張されたテーマエディターを作成
        extended_editor_class = extend_theme_editor_with_zebra()

        if extended_editor_class:
            editor = extended_editor_class()
            editor.show()
            sys.exit(app.exec_())
        else:
            # フォールバック：ゼブラタブのみ表示
            zebra_tab = ZebraPatternTab()
            zebra_tab.setWindowTitle("ゼブラパターンエディター - 単体テスト")
            zebra_tab.resize(800, 600)
            zebra_tab.show()
            sys.exit(app.exec_())
    else:
        print("❌ Qt framework not available")
