#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ゼブラパターン自動生成エディター - テーマエディター統合版
リアルタイムでコントラスト比を調整できるゼブラパターン生成機能
"""

from typing import Tuple, Optional
import colorsys
from pathlib import Path

try:
    from PyQt5.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
        QSlider, QSpinBox, QPushButton, QCheckBox, QGridLayout,
        QFrame, QDoubleSpinBox
    )
    from PyQt5.QtCore import Qt, pyqtSignal
    from PyQt5.QtGui import QFont
    QtHorizontal = Qt.Horizontal
    QtAlignCenter = Qt.AlignCenter
    QFontBold = QFont.Bold
    qt_available = True
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
            QSlider, QSpinBox, QPushButton, QCheckBox, QGridLayout,
            QFrame, QDoubleSpinBox
        )
        from PyQt6.QtCore import Qt, pyqtSignal
        from PyQt6.QtGui import QFont
        QtHorizontal = Qt.Orientation.Horizontal
        QtAlignCenter = Qt.AlignmentFlag.AlignCenter
        QFontBold = QFont.Weight.Bold
        qt_available = True
    except ImportError:
        try:
            from PySide6.QtWidgets import (
                QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
                QSlider, QSpinBox, QPushButton, QCheckBox, QGridLayout,
                QFrame, QDoubleSpinBox
            )
            from PySide6.QtCore import Qt, Signal as pyqtSignal
            from PySide6.QtGui import QFont
            QtHorizontal = Qt.Orientation.Horizontal
            QtAlignCenter = Qt.AlignmentFlag.AlignCenter
            QFontBold = QFont.Weight.Bold
            qt_available = True
        except ImportError:
            qt_available = False


class ZebraPatternGenerator:
    """ゼブラパターン色の自動生成ユーティリティクラス"""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """16進数カラーコードをRGBに変換"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """RGBを16進数カラーコードに変換"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def get_luminance(hex_color: str) -> float:
        """色の相対輝度を計算 (WCAG準拠)"""
        r, g, b = ZebraPatternGenerator.hex_to_rgb(hex_color)
        
        # 0-1範囲に正規化
        r, g, b = r/255.0, g/255.0, b/255.0
        
        # ガンマ補正
        def gamma_correct(c):
            return c/12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        r, g, b = map(gamma_correct, [r, g, b])
        
        # 輝度計算
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    @staticmethod
    def get_contrast_ratio(color1: str, color2: str) -> float:
        """2色間のコントラスト比を計算"""
        l1 = ZebraPatternGenerator.get_luminance(color1)
        l2 = ZebraPatternGenerator.get_luminance(color2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    @staticmethod
    def adjust_brightness_hsl(hex_color: str, lightness_change_percent: float) -> str:
        """HSL色空間で明度を調整（より精密）"""
        r, g, b = ZebraPatternGenerator.hex_to_rgb(hex_color)
        h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
        
        # 明度を調整（0-1の範囲で）
        new_l = max(0, min(1, l + lightness_change_percent/100))
        
        # HSLからRGBに戻す
        new_r, new_g, new_b = colorsys.hls_to_rgb(h, new_l, s)
        
        # 0-255の範囲に戻す
        new_r = int(round(new_r * 255))
        new_g = int(round(new_g * 255))
        new_b = int(round(new_b * 255))
        
        return ZebraPatternGenerator.rgb_to_hex(new_r, new_g, new_b)
    
    @staticmethod
    def adjust_brightness_hsv(hex_color: str, brightness_factor: float) -> str:
        """HSV色空間で明度を調整"""
        r, g, b = ZebraPatternGenerator.hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # 明度を調整
        new_v = max(0, min(1, v * (1 + brightness_factor)))
        
        r, g, b = colorsys.hsv_to_rgb(h, s, new_v)
        return ZebraPatternGenerator.rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    @staticmethod
    def generate_zebra_color(base_color: str, contrast_target: float = 1.2, 
                           method: str = "auto") -> str:
        """
        ベース色からゼブラパターン色を生成
        
        Args:
            base_color: ベースとなる背景色
            contrast_target: 目標コントラスト比 (1.1-3.0推奨)
            method: 調整方法 ("auto", "lighter", "darker", "hsl", "hsv")
        
        Returns:
            ゼブラパターン用の色
        """
        base_luminance = ZebraPatternGenerator.get_luminance(base_color)
        
        if method == "auto":
            # 背景の明度に基づいて自動選択
            if base_luminance > 0.5:
                method = "darker"
            else:
                method = "lighter"
        
        # 目標コントラスト比を達成するまで調整
        best_color = base_color
        best_contrast = 1.0
        
        # 明度調整の幅を設定（-50%から+50%まで）
        adjustment_range = range(-50, 51, 2)
        
        for adjustment in adjustment_range:
            if method in ["darker", "lighter"]:
                # 方向を制限
                if method == "darker" and adjustment > 0:
                    continue
                if method == "lighter" and adjustment < 0:
                    continue
            
            if method in ["auto", "darker", "lighter", "hsl"]:
                test_color = ZebraPatternGenerator.adjust_brightness_hsl(base_color, adjustment)
            else:  # hsv
                test_color = ZebraPatternGenerator.adjust_brightness_hsv(base_color, adjustment/100.0)
            
            contrast = ZebraPatternGenerator.get_contrast_ratio(base_color, test_color)
            
            # 目標に最も近いコントラスト比を選択
            if abs(contrast - contrast_target) < abs(best_contrast - contrast_target):
                best_color = test_color
                best_contrast = contrast
        
        return best_color
    
    @staticmethod
    def generate_accessibility_compliant_zebra(base_color: str, 
                                             accessibility_level: str = "subtle") -> dict:
        """
        アクセシビリティを考慮したゼブラパターンを生成
        
        Args:
            base_color: ベース色
            accessibility_level: "subtle"(控えめ), "moderate"(中程度), "high"(高コントラスト)
        
        Returns:
            ゼブラパターンの情報を含む辞書
        """
        contrast_targets = {
            "subtle": 1.15,      # 1.15:1 - 非常に控えめ
            "moderate": 1.3,     # 1.3:1 - 適度な識別性
            "high": 1.8          # 1.8:1 - 明確な識別性
        }
        
        target_contrast = contrast_targets.get(accessibility_level, 1.15)
        
        zebra_colors = {}
        methods = ["auto", "hsl", "hsv"]
        
        for method in methods:
            zebra_color = ZebraPatternGenerator.generate_zebra_color(
                base_color, target_contrast, method
            )
            actual_contrast = ZebraPatternGenerator.get_contrast_ratio(base_color, zebra_color)
            
            zebra_colors[method] = {
                "color": zebra_color,
                "contrast_ratio": actual_contrast,
                "luminance_diff": abs(
                    ZebraPatternGenerator.get_luminance(base_color) - 
                    ZebraPatternGenerator.get_luminance(zebra_color)
                )
            }
        
        # 最適な方法を選択（目標コントラスト比に最も近い）
        best_method = min(zebra_colors.keys(), 
                         key=lambda m: abs(zebra_colors[m]["contrast_ratio"] - target_contrast))
        
        return {
            "base_color": base_color,
            "zebra_color": zebra_colors[best_method]["color"],
            "contrast_ratio": zebra_colors[best_method]["contrast_ratio"],
            "luminance_difference": zebra_colors[best_method]["luminance_diff"],
            "accessibility_level": accessibility_level,
            "method_used": best_method,
            "all_options": zebra_colors
        }


class ZebraPatternEditor(QWidget if qt_available else object):
    """ゼブラパターン編集ウィジェット"""
    
    zebraColorChanged = pyqtSignal(str)  # ゼブラ色変更シグナル
    
    def __init__(self, parent=None):
        if not qt_available:
            raise RuntimeError("Qt framework not available")
        
        super().__init__(parent)
        self.base_color = "#ffffff"
        self.zebra_color = "#f5f5f5"
        self.setup_ui()
    
    def setup_ui(self):
        """UIを設定"""
        layout = QVBoxLayout(self)
        
        # タイトル
        title = QLabel("🦓 ゼブラパターン自動生成")
        title.setFont(QFont("", 12, QFontBold))
        layout.addWidget(title)
        
        # プレビューエリア
        self.setup_preview_area(layout)
        
        # コントラスト調整
        self.setup_contrast_controls(layout)
        
        # アクセシビリティレベル
        self.setup_accessibility_controls(layout)
        
        # 生成方法選択
        self.setup_method_controls(layout)
        
        # アクションボタン
        self.setup_action_buttons(layout)
    
    def setup_preview_area(self, parent_layout):
        """プレビューエリアを設定"""
        preview_group = QGroupBox("プレビュー")
        layout = QVBoxLayout(preview_group)
        
        # カラープレビュー
        preview_container = QWidget()
        preview_layout = QHBoxLayout(preview_container)
        
        # ベース色プレビュー
        self.base_preview = QFrame()
        self.base_preview.setFixedSize(100, 60)
        self.base_preview.setFrameStyle(QFrame.Box)
        preview_layout.addWidget(QLabel("ベース色:"))
        preview_layout.addWidget(self.base_preview)
        
        # ゼブラ色プレビュー
        self.zebra_preview = QFrame()
        self.zebra_preview.setFixedSize(100, 60)
        self.zebra_preview.setFrameStyle(QFrame.Box)
        preview_layout.addWidget(QLabel("ゼブラ色:"))
        preview_layout.addWidget(self.zebra_preview)
        
        layout.addWidget(preview_container)
        
        # 情報表示
        info_layout = QGridLayout()
        
        self.contrast_info = QLabel("コントラスト比: 1.00:1")
        info_layout.addWidget(self.contrast_info, 0, 0)
        
        self.luminance_info = QLabel("輝度差: 0.00")
        info_layout.addWidget(self.luminance_info, 0, 1)
        
        self.accessibility_info = QLabel("レベル: 適切")
        info_layout.addWidget(self.accessibility_info, 1, 0)
        
        self.recommendation = QLabel("推奨: ✓")
        info_layout.addWidget(self.recommendation, 1, 1)
        
        layout.addLayout(info_layout)
        
        parent_layout.addWidget(preview_group)
    
    def setup_contrast_controls(self, parent_layout):
        """コントラスト調整コントロールを設定"""
        contrast_group = QGroupBox("コントラスト比調整")
        layout = QVBoxLayout(contrast_group)
        
        # スライダーでの調整
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("目標比:"))
        
        self.contrast_slider = QSlider(QtHorizontal)
        self.contrast_slider.setRange(105, 300)  # 1.05から3.00まで
        self.contrast_slider.setValue(120)  # デフォルト1.20
        self.contrast_slider.valueChanged.connect(self.on_contrast_changed)
        slider_layout.addWidget(self.contrast_slider)
        
        self.contrast_spinbox = QDoubleSpinBox()
        self.contrast_spinbox.setRange(1.05, 3.00)
        self.contrast_spinbox.setSingleStep(0.05)
        self.contrast_spinbox.setValue(1.20)
        self.contrast_spinbox.valueChanged.connect(self.on_contrast_spinbox_changed)
        slider_layout.addWidget(self.contrast_spinbox)
        
        # スライダーとスピンボックスを連動
        self.contrast_slider.valueChanged.connect(
            lambda v: self.contrast_spinbox.setValue(v/100.0)
        )
        
        layout.addLayout(slider_layout)
        
        parent_layout.addWidget(contrast_group)
    
    def setup_accessibility_controls(self, parent_layout):
        """アクセシビリティレベル選択を設定"""
        accessibility_group = QGroupBox("アクセシビリティレベル")
        layout = QHBoxLayout(accessibility_group)
        
        self.accessibility_buttons = {}
        levels = [
            ("subtle", "控えめ (1.15:1)", "日常使用に適した控えめなコントラスト"),
            ("moderate", "中程度 (1.30:1)", "バランスの取れた視認性"),  
            ("high", "高 (1.80:1)", "明確な識別が必要な場合")
        ]
        
        for level, label, tooltip in levels:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            btn.clicked.connect(lambda checked, l=level: self.set_accessibility_level(l))
            layout.addWidget(btn)
            self.accessibility_buttons[level] = btn
        
        # デフォルトで「控えめ」を選択
        self.accessibility_buttons["subtle"].setChecked(True)
        self.current_accessibility_level = "subtle"
        
        parent_layout.addWidget(accessibility_group)
    
    def setup_method_controls(self, parent_layout):
        """生成方法選択を設定"""
        method_group = QGroupBox("生成方法")
        layout = QHBoxLayout(method_group)
        
        self.method_buttons = {}
        methods = [
            ("auto", "自動", "背景色の明度に基づいて最適な方法を選択"),
            ("hsl", "HSL", "HSL色空間での明度調整"),
            ("hsv", "HSV", "HSV色空間での明度調整")
        ]
        
        for method, label, tooltip in methods:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            btn.clicked.connect(lambda checked, m=method: self.set_method(m))
            layout.addWidget(btn)
            self.method_buttons[method] = btn
        
        # デフォルトで「自動」を選択
        self.method_buttons["auto"].setChecked(True)
        self.current_method = "auto"
        
        parent_layout.addWidget(method_group)
    
    def setup_action_buttons(self, parent_layout):
        """アクションボタンを設定"""
        button_layout = QHBoxLayout()
        
        auto_generate_btn = QPushButton("🎨 自動生成")
        auto_generate_btn.clicked.connect(self.auto_generate)
        button_layout.addWidget(auto_generate_btn)
        
        reset_btn = QPushButton("🔄 リセット")
        reset_btn.clicked.connect(self.reset_to_default)
        button_layout.addWidget(reset_btn)
        
        apply_btn = QPushButton("✓ 適用")
        apply_btn.clicked.connect(self.apply_zebra_color)
        button_layout.addWidget(apply_btn)
        
        parent_layout.addLayout(button_layout)
    
    def set_base_color(self, color: str):
        """ベース色を設定"""
        self.base_color = color
        self.update_preview()
        self.auto_generate()  # 自動的に新しいゼブラ色を生成
    
    def on_contrast_changed(self, value):
        """コントラストスライダー変更時"""
        self.auto_generate()
    
    def on_contrast_spinbox_changed(self, value):
        """コントラストスピンボックス変更時"""
        self.contrast_slider.setValue(int(value * 100))
        self.auto_generate()
    
    def set_accessibility_level(self, level):
        """アクセシビリティレベルを設定"""
        # 他のボタンのチェックを外す
        for btn in self.accessibility_buttons.values():
            btn.setChecked(False)
        
        # 選択されたボタンをチェック
        self.accessibility_buttons[level].setChecked(True)
        self.current_accessibility_level = level
        
        # 対応するコントラスト比を設定
        level_ratios = {"subtle": 1.15, "moderate": 1.30, "high": 1.80}
        self.contrast_spinbox.setValue(level_ratios[level])
        
        self.auto_generate()
    
    def set_method(self, method):
        """生成方法を設定"""
        # 他のボタンのチェックを外す
        for btn in self.method_buttons.values():
            btn.setChecked(False)
        
        # 選択されたボタンをチェック
        self.method_buttons[method].setChecked(True)
        self.current_method = method
        
        self.auto_generate()
    
    def auto_generate(self):
        """自動生成を実行"""
        target_contrast = self.contrast_spinbox.value()
        
        self.zebra_color = ZebraPatternGenerator.generate_zebra_color(
            self.base_color, target_contrast, self.current_method
        )
        
        self.update_preview()
        self.zebraColorChanged.emit(self.zebra_color)
    
    def reset_to_default(self):
        """デフォルト設定にリセット"""
        self.contrast_spinbox.setValue(1.20)
        self.set_accessibility_level("subtle")
        self.set_method("auto")
        self.auto_generate()
    
    def apply_zebra_color(self):
        """ゼブラ色を適用（外部に通知）"""
        self.zebraColorChanged.emit(self.zebra_color)
    
    def update_preview(self):
        """プレビューを更新"""
        # カラープレビューを更新
        self.base_preview.setStyleSheet(f"background-color: {self.base_color};")
        self.zebra_preview.setStyleSheet(f"background-color: {self.zebra_color};")
        
        # 情報を更新
        contrast_ratio = ZebraPatternGenerator.get_contrast_ratio(self.base_color, self.zebra_color)
        base_luminance = ZebraPatternGenerator.get_luminance(self.base_color)
        zebra_luminance = ZebraPatternGenerator.get_luminance(self.zebra_color)
        luminance_diff = abs(base_luminance - zebra_luminance)
        
        self.contrast_info.setText(f"コントラスト比: {contrast_ratio:.2f}:1")
        self.luminance_info.setText(f"輝度差: {luminance_diff:.3f}")
        
        # アクセシビリティ評価
        if contrast_ratio < 1.1:
            level_text = "低すぎ ❌"
            recommendation = "コントラストを上げてください"
        elif contrast_ratio < 1.3:
            level_text = "控えめ ✓"
            recommendation = "日常使用に適しています"
        elif contrast_ratio < 1.8:
            level_text = "中程度 ✓"
            recommendation = "良好な視認性です"
        else:
            level_text = "高コントラスト ✓"
            recommendation = "明確な識別が可能です"
        
        self.accessibility_info.setText(f"レベル: {level_text}")
        self.recommendation.setText(f"推奨: {recommendation}")
    
    def get_zebra_config(self) -> dict:
        """現在のゼブラ設定を取得"""
        return {
            "base_color": self.base_color,
            "zebra_color": self.zebra_color,
            "contrast_ratio": ZebraPatternGenerator.get_contrast_ratio(self.base_color, self.zebra_color),
            "accessibility_level": self.current_accessibility_level,
            "generation_method": self.current_method
        }


if __name__ == "__main__":
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
        
        # テスト用ウィンドウ
        editor = ZebraPatternEditor()
        editor.setWindowTitle("ゼブラパターンエディター - テスト")
        editor.resize(600, 500)
        editor.show()
        
        # テスト用の色を設定
        editor.set_base_color("#2d3748")  # 暗い背景色
        
        sys.exit(app.exec_())
    else:
        print("Qt framework not available. Please install PyQt5/PyQt6/PySide6.")
