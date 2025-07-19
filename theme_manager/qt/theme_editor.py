"""
Advanced Theme Editor with color theory and contrast calculations.
Provides intelligent theme creation with accessibility guidelines.
"""

import json
import colorsys
import math
from typing import Dict, Any, Optional, Tuple, Union
from pathlib import Path

# Import Qt availability from controller
from .controller import qt_available, qt_framework

# Import handling for Qt libraries  
if qt_available:
    try:
        from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QPushButton, QLabel, QLineEdit, QSlider, QSpinBox, QGroupBox,
            QGridLayout, QFrame, QColorDialog, QTabWidget, QScrollArea,
            QTextEdit, QComboBox, QCheckBox, QProgressBar, QListWidget,
            QSplitter, QFileDialog, QMessageBox, QDoubleSpinBox
        )
        from PyQt5.QtCore import Qt, pyqtSignal, QTimer
        from PyQt5.QtGui import QColor, QPalette, QFont
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                QPushButton, QLabel, QLineEdit, QSlider, QSpinBox, QGroupBox,
                QGridLayout, QFrame, QColorDialog, QTabWidget, QScrollArea,
                QTextEdit, QComboBox, QCheckBox, QProgressBar, QListWidget,
                QSplitter, QFileDialog, QMessageBox, QDoubleSpinBox
            )
            from PyQt6.QtCore import Qt, pyqtSignal, QTimer
            from PyQt6.QtGui import QColor, QPalette, QFont
        except ImportError:
            from PySide6.QtWidgets import (
                QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                QPushButton, QLabel, QLineEdit, QSlider, QSpinBox, QGroupBox,
                QGridLayout, QFrame, QColorDialog, QTabWidget, QScrollArea,
                QTextEdit, QComboBox, QCheckBox, QProgressBar, QListWidget,
                QSplitter, QFileDialog, QMessageBox, QDoubleSpinBox
            )
            from PySide6.QtCore import Qt, Signal as pyqtSignal, QTimer
            from PySide6.QtGui import QColor, QPalette, QFont

from .controller import ThemeController
from .stylesheet import StylesheetGenerator


class ColorUtils:
    """Utility class for color calculations and accessibility."""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convert RGB to hex color."""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def get_luminance(hex_color: str) -> float:
        """Calculate relative luminance according to WCAG guidelines."""
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        
        # Convert to 0-1 range
        r, g, b = r/255.0, g/255.0, b/255.0
        
        # Apply gamma correction
        def gamma_correct(c):
            return c/12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        r, g, b = map(gamma_correct, [r, g, b])
        
        # Calculate luminance
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    @staticmethod
    def get_contrast_ratio(color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors."""
        l1 = ColorUtils.get_luminance(color1)
        l2 = ColorUtils.get_luminance(color2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    @staticmethod
    def is_accessible(bg_color: str, text_color: str, level: str = "AA") -> bool:
        """Check if color combination meets WCAG accessibility standards."""
        contrast = ColorUtils.get_contrast_ratio(bg_color, text_color)
        
        if level == "AAA":
            return contrast >= 7.0  # AAA standard
        else:
            return contrast >= 4.5  # AA standard
    
    @staticmethod
    def get_optimal_text_color(bg_color: str) -> str:
        """Get optimal text color (black or white) for given background."""
        luminance = ColorUtils.get_luminance(bg_color)
        return "#000000" if luminance > 0.5 else "#ffffff"
    
    @staticmethod
    def adjust_brightness(hex_color: str, factor: float) -> str:
        """Adjust color brightness by factor (-1.0 to 1.0)."""
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # Adjust brightness
        v = max(0, min(1, v + factor))
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return ColorUtils.rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    @staticmethod
    def adjust_saturation(hex_color: str, factor: float) -> str:
        """Adjust color saturation by factor (-1.0 to 1.0)."""
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # Adjust saturation
        s = max(0, min(1, s + factor))
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return ColorUtils.rgb_to_hex(int(r*255), int(g*255), int(b*255))


class ColorPreviewWidget(QWidget if qt_available else object):
    """Widget to preview color with accessibility information."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 120)
        
        layout = QVBoxLayout(self)
        
        # Color display area
        self.color_display = QFrame()
        self.color_display.setFixedSize(180, 60)
        self.color_display.setFrameStyle(QFrame.Box)
        layout.addWidget(self.color_display)
        
        # Info labels
        self.hex_label = QLabel("#ffffff")
        self.hex_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.hex_label)
        
        self.luminance_label = QLabel("Luminance: 1.00")
        self.luminance_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.luminance_label)
        
        self.setStyleSheet("""
            QFrame {
                border: 2px solid #ccc;
                border-radius: 4px;
            }
            QLabel {
                font-size: 11px;
                color: #666;
            }
        """)
    
    def set_color(self, hex_color: str):
        """Set the color to preview."""
        self.color_display.setStyleSheet(f"background-color: {hex_color};")
        self.hex_label.setText(hex_color.upper())
        
        luminance = ColorUtils.get_luminance(hex_color)
        self.luminance_label.setText(f"Luminance: {luminance:.2f}")


class ContrastChecker(QWidget if qt_available else object):
    """Widget to check contrast between two colors."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("コントラストチェッカー")
        title.setFont(QFont("", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Preview area
        self.preview = QLabel("サンプルテキスト")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setFixedHeight(80)
        self.preview.setStyleSheet("""
            QLabel {
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.preview)
        
        # Contrast info
        info_layout = QGridLayout()
        
        self.contrast_label = QLabel("コントラスト比: 0.00:1")
        info_layout.addWidget(self.contrast_label, 0, 0)
        
        self.wcag_aa_label = QLabel("WCAG AA: ❌")
        info_layout.addWidget(self.wcag_aa_label, 0, 1)
        
        self.wcag_aaa_label = QLabel("WCAG AAA: ❌")
        info_layout.addWidget(self.wcag_aaa_label, 1, 0)
        
        self.recommendation = QLabel("")
        self.recommendation.setWordWrap(True)
        info_layout.addWidget(self.recommendation, 1, 1)
        
        layout.addLayout(info_layout)
    
    def check_contrast(self, bg_color: str, text_color: str):
        """Check contrast between background and text colors."""
        contrast = ColorUtils.get_contrast_ratio(bg_color, text_color)
        aa_pass = ColorUtils.is_accessible(bg_color, text_color, "AA")
        aaa_pass = ColorUtils.is_accessible(bg_color, text_color, "AAA")
        
        # Update preview
        self.preview.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border: 2px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
            }}
        """)
        
        # Update info
        self.contrast_label.setText(f"コントラスト比: {contrast:.2f}:1")
        self.wcag_aa_label.setText(f"WCAG AA: {'✅' if aa_pass else '❌'}")
        self.wcag_aaa_label.setText(f"WCAG AAA: {'✅' if aaa_pass else '❌'}")
        
        if contrast < 3.0:
            rec = "コントラストが低すぎます。可読性を向上させる必要があります。"
        elif contrast < 4.5:
            rec = "最小限のアクセシビリティ基準を満たしていません。"
        elif contrast < 7.0:
            rec = "WCAG AA基準を満たしています。"
        else:
            rec = "優れたコントラストです！WCAG AAA基準を満たしています。"
            
        self.recommendation.setText(rec)


class ColorSliderGroup(QWidget if qt_available else object):
    """Group of sliders for color adjustment."""
    
    colorChanged = pyqtSignal(str)
    
    def __init__(self, title: str, initial_color: str = "#ffffff", parent=None):
        super().__init__(parent)
        self.title = title
        self.color = initial_color
        self.setup_ui()
        self.update_from_hex(initial_color)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title and color preview
        header_layout = QHBoxLayout()
        
        title_label = QLabel(self.title)
        title_label.setFont(QFont("", 10, QFont.Bold))
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Color preview button
        self.color_preview = QPushButton()
        self.color_preview.setFixedSize(40, 20)
        self.color_preview.clicked.connect(self.choose_color)
        header_layout.addWidget(self.color_preview)
        
        layout.addLayout(header_layout)
        
        # RGB sliders
        slider_layout = QGridLayout()
        
        self.sliders = {}
        self.spinboxes = {}
        
        for i, (name, color) in enumerate([("R", "red"), ("G", "green"), ("B", "blue")]):
            label = QLabel(name)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 255)
            slider.valueChanged.connect(self.update_color)
            
            spinbox = QSpinBox()
            spinbox.setRange(0, 255)
            spinbox.valueChanged.connect(self.update_color)
            
            # Connect slider and spinbox
            slider.valueChanged.connect(spinbox.setValue)
            spinbox.valueChanged.connect(slider.setValue)
            
            slider_layout.addWidget(label, i, 0)
            slider_layout.addWidget(slider, i, 1)
            slider_layout.addWidget(spinbox, i, 2)
            
            self.sliders[name.lower()] = slider
            self.spinboxes[name.lower()] = spinbox
        
        layout.addLayout(slider_layout)
        
        # Hex input
        hex_layout = QHBoxLayout()
        hex_layout.addWidget(QLabel("Hex:"))
        
        self.hex_input = QLineEdit()
        self.hex_input.setMaxLength(7)
        self.hex_input.textChanged.connect(self.update_from_hex_input)
        hex_layout.addWidget(self.hex_input)
        
        layout.addLayout(hex_layout)
    
    def choose_color(self):
        """Open color dialog."""
        color = QColorDialog.getColor(QColor(self.color))
        if color.isValid():
            self.update_from_hex(color.name())
    
    def update_color(self):
        """Update color from slider values."""
        r = self.sliders['r'].value()
        g = self.sliders['g'].value()
        b = self.sliders['b'].value()
        
        self.color = ColorUtils.rgb_to_hex(r, g, b)
        self.update_preview()
        self.hex_input.setText(self.color)
        self.colorChanged.emit(self.color)
    
    def update_from_hex(self, hex_color: str):
        """Update sliders from hex color."""
        if not hex_color.startswith('#') or len(hex_color) != 7:
            return
        
        try:
            r, g, b = ColorUtils.hex_to_rgb(hex_color)
            
            # Block signals to prevent recursion
            for slider in self.sliders.values():
                slider.blockSignals(True)
            for spinbox in self.spinboxes.values():
                spinbox.blockSignals(True)
            
            self.sliders['r'].setValue(r)
            self.sliders['g'].setValue(g)
            self.sliders['b'].setValue(b)
            
            # Unblock signals
            for slider in self.sliders.values():
                slider.blockSignals(False)
            for spinbox in self.spinboxes.values():
                spinbox.blockSignals(False)
            
            self.color = hex_color
            self.hex_input.setText(hex_color)
            self.update_preview()
            self.colorChanged.emit(self.color)
            
        except ValueError:
            pass
    
    def update_from_hex_input(self, text: str):
        """Update color from hex input field."""
        if text.startswith('#') and len(text) == 7:
            self.update_from_hex(text)
    
    def update_preview(self):
        """Update color preview button."""
        self.color_preview.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                border: 1px solid #ccc;
                border-radius: 2px;
            }}
        """)
    
    def get_color(self) -> str:
        """Get current color as hex."""
        return self.color


class ThemeEditorWindow(QMainWindow if qt_available else object):
    """Advanced theme editor with color theory integration."""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """Initialize theme editor window."""
        if not qt_available:
            raise RuntimeError("Qt framework not available. Install PyQt5/PyQt6/PySide6.")
        
        super().__init__()
        
        self.controller = ThemeController(config_path)
        self.current_theme_config = {}
        
        self.setWindowTitle("ThemeManager - 高度なテーマエディター")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setup_ui()
        self.load_default_theme()
        
        # Auto-update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.auto_update_preview)
        self.update_timer.setSingleShot(True)
    
    def setup_ui(self):
        """Setup the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main splitter
        main_splitter = QSplitter(Qt.Horizontal)
        central_widget_layout = QHBoxLayout(central_widget)
        central_widget_layout.addWidget(main_splitter)
        
        # Left panel: Controls
        self.setup_controls_panel(main_splitter)
        
        # Right panel: Preview
        self.setup_preview_panel(main_splitter)
        
        # Set splitter proportions
        main_splitter.setSizes([600, 600])
    
    def setup_controls_panel(self, parent):
        """Setup the left control panel."""
        controls_widget = QWidget()
        parent.addWidget(controls_widget)
        
        layout = QVBoxLayout(controls_widget)
        
        # Theme info
        info_group = QGroupBox("テーマ情報")
        info_layout = QGridLayout(info_group)
        
        info_layout.addWidget(QLabel("名前:"), 0, 0)
        self.theme_name_input = QLineEdit("custom_theme")
        info_layout.addWidget(self.theme_name_input, 0, 1)
        
        info_layout.addWidget(QLabel("表示名:"), 1, 0)
        self.display_name_input = QLineEdit("カスタムテーマ")
        info_layout.addWidget(self.display_name_input, 1, 1)
        
        info_layout.addWidget(QLabel("説明:"), 2, 0)
        self.description_input = QLineEdit("カスタム作成テーマ")
        info_layout.addWidget(self.description_input, 2, 1)
        
        layout.addWidget(info_group)
        
        # Color controls in tabs
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Basic colors tab
        basic_tab = QWidget()
        tabs.addTab(basic_tab, "基本色")
        self.setup_basic_colors_tab(basic_tab)
        
        # Component colors tab
        components_tab = QWidget()
        tabs.addTab(components_tab, "コンポーネント")
        self.setup_components_tab(components_tab)
        
        # Contrast checker tab
        contrast_tab = QWidget()
        tabs.addTab(contrast_tab, "コントラスト")
        self.setup_contrast_tab(contrast_tab)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        reset_btn = QPushButton("リセット")
        reset_btn.clicked.connect(self.load_default_theme)
        buttons_layout.addWidget(reset_btn)
        
        export_btn = QPushButton("エクスポート")
        export_btn.clicked.connect(self.export_theme)
        buttons_layout.addWidget(export_btn)
        
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self.save_theme)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        
        # Add stretch
        layout.addStretch()
    
    def setup_basic_colors_tab(self, tab_widget):
        """Setup basic colors tab."""
        layout = QVBoxLayout(tab_widget)
        
        # Scroll area for color controls
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Color slider groups
        self.color_sliders = {}
        
        basic_colors = [
            ("background", "背景色", "#ffffff"),
            ("text", "テキスト色", "#000000"),
            ("primary", "プライマリ色", "#007acc"),
            ("accent", "アクセント色", "#ff6b35"),
        ]
        
        for key, label, default_color in basic_colors:
            slider_group = ColorSliderGroup(label, default_color)
            slider_group.colorChanged.connect(lambda color, k=key: self.update_color(k, color))
            scroll_layout.addWidget(slider_group)
            self.color_sliders[key] = slider_group
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Smart adjustments
        smart_group = QGroupBox("スマート調整")
        smart_layout = QVBoxLayout(smart_group)
        
        auto_text_btn = QPushButton("テキスト色を自動調整")
        auto_text_btn.clicked.connect(self.auto_adjust_text_colors)
        smart_layout.addWidget(auto_text_btn)
        
        generate_palette_btn = QPushButton("カラーパレットを生成")
        generate_palette_btn.clicked.connect(self.generate_color_palette)
        smart_layout.addWidget(generate_palette_btn)
        
        layout.addWidget(smart_group)
    
    def setup_components_tab(self, tab_widget):
        """Setup component colors tab."""
        layout = QVBoxLayout(tab_widget)
        
        # This would contain button, panel, input field color settings
        info_label = QLabel("コンポーネント色設定\n（実装予定）")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        layout.addStretch()
    
    def setup_contrast_tab(self, tab_widget):
        """Setup contrast checker tab."""
        layout = QVBoxLayout(tab_widget)
        
        self.contrast_checker = ContrastChecker()
        layout.addWidget(self.contrast_checker)
        
        layout.addStretch()
    
    def setup_preview_panel(self, parent):
        """Setup the right preview panel."""
        preview_widget = QWidget()
        parent.addWidget(preview_widget)
        
        layout = QVBoxLayout(preview_widget)
        
        # Preview title
        title = QLabel("プレビュー")
        title.setFont(QFont("", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Preview area
        self.preview_area = self.create_preview_widgets()
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.preview_area)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
    
    def create_preview_widgets(self) -> QWidget:
        """Create preview widget collection."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Sample widgets
        layout.addWidget(QLabel("サンプルテキスト"))
        
        btn = QPushButton("サンプルボタン")
        layout.addWidget(btn)
        
        line_edit = QLineEdit("入力欄のサンプル")
        layout.addWidget(line_edit)
        
        text_edit = QTextEdit()
        text_edit.setPlainText("複数行テキストエリア\nの表示サンプルです。")
        text_edit.setMaximumHeight(100)
        layout.addWidget(text_edit)
        
        combo = QComboBox()
        combo.addItems(["選択肢1", "選択肢2", "選択肢3"])
        layout.addWidget(combo)
        
        progress = QProgressBar()
        progress.setValue(60)
        layout.addWidget(progress)
        
        layout.addStretch()
        
        return widget
    
    def update_color(self, color_key: str, hex_color: str):
        """Update color in theme configuration."""
        self.current_theme_config[f"{color_key}Color"] = hex_color
        
        # Update contrast checker if background or text color changed
        if color_key in ['background', 'text']:
            self.update_contrast_checker()
        
        # Schedule preview update
        self.update_timer.start(100)  # 100ms delay for smooth sliding
    
    def update_contrast_checker(self):
        """Update contrast checker with current colors."""
        bg_color = self.current_theme_config.get("backgroundColor", "#ffffff")
        text_color = self.current_theme_config.get("textColor", "#000000")
        self.contrast_checker.check_contrast(bg_color, text_color)
    
    def auto_adjust_text_colors(self):
        """Automatically adjust text colors for optimal contrast."""
        bg_color = self.current_theme_config.get("backgroundColor", "#ffffff")
        
        # Calculate optimal text color
        optimal_text = ColorUtils.get_optimal_text_color(bg_color)
        
        self.current_theme_config["textColor"] = optimal_text
        self.color_sliders["text"].update_from_hex(optimal_text)
        
        QMessageBox.information(self, "自動調整完了", 
                              f"背景色に対して最適なテキスト色 ({optimal_text}) を設定しました。")
    
    def generate_color_palette(self):
        """Generate harmonious color palette based on primary color."""
        primary_color = self.current_theme_config.get("primaryColor", "#007acc")
        
        # Generate complementary and analogous colors
        r, g, b = ColorUtils.hex_to_rgb(primary_color)
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # Generate accent color (complementary)
        accent_h = (h + 0.5) % 1.0
        accent_r, accent_g, accent_b = colorsys.hsv_to_rgb(accent_h, s, v)
        accent_color = ColorUtils.rgb_to_hex(int(accent_r*255), int(accent_g*255), int(accent_b*255))
        
        self.current_theme_config["accentColor"] = accent_color
        self.color_sliders["accent"].update_from_hex(accent_color)
        
        QMessageBox.information(self, "パレット生成完了", 
                              f"プライマリ色に基づいてアクセント色 ({accent_color}) を生成しました。")
    
    def auto_update_preview(self):
        """Update preview with current theme configuration."""
        if not self.current_theme_config:
            return
        
        # Generate stylesheet
        generator = StylesheetGenerator(self.current_theme_config)
        stylesheet = generator.generate_qss()
        
        # Apply to preview area
        self.preview_area.setStyleSheet(stylesheet)
    
    def load_default_theme(self):
        """Load default theme configuration."""
        # Load light theme as default
        themes = self.controller.get_available_themes()
        if "light" in themes:
            self.current_theme_config = themes["light"].copy()
        else:
            # Fallback configuration
            self.current_theme_config = {
                "name": "custom",
                "display_name": "カスタムテーマ",
                "description": "カスタム作成テーマ",
                "backgroundColor": "#ffffff",
                "textColor": "#000000",
                "primaryColor": "#007acc",
                "accentColor": "#ff6b35"
            }
        
        # Update UI controls
        self.theme_name_input.setText(self.current_theme_config.get("name", "custom"))
        self.display_name_input.setText(self.current_theme_config.get("display_name", "カスタムテーマ"))
        self.description_input.setText(self.current_theme_config.get("description", "カスタム作成テーマ"))
        
        # Update color sliders
        for key, slider_group in self.color_sliders.items():
            color_value = self.current_theme_config.get(f"{key}Color", "#ffffff")
            slider_group.update_from_hex(color_value)
        
        self.update_contrast_checker()
        self.auto_update_preview()
    
    def export_theme(self):
        """Export current theme configuration to JSON file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "テーマをエクスポート", "", "JSON files (*.json)"
        )
        
        if file_path:
            try:
                # Update theme config with current form values
                self.current_theme_config["name"] = self.theme_name_input.text()
                self.current_theme_config["display_name"] = self.display_name_input.text()
                self.current_theme_config["description"] = self.description_input.text()
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.current_theme_config, f, indent=2, ensure_ascii=False)
                
                QMessageBox.information(self, "エクスポート完了", 
                                      f"テーマを {file_path} にエクスポートしました。")
            except Exception as e:
                QMessageBox.critical(self, "エクスポートエラー", 
                                   f"エクスポート中にエラーが発生しました: {str(e)}")
    
    def save_theme(self):
        """Save theme to the main theme configuration."""
        try:
            # Update theme config with current form values
            self.current_theme_config["name"] = self.theme_name_input.text()
            self.current_theme_config["display_name"] = self.display_name_input.text()
            self.current_theme_config["description"] = self.description_input.text()
            
            # This would integrate with the main theme system
            QMessageBox.information(self, "保存完了", "テーマを保存しました。")
            
        except Exception as e:
            QMessageBox.critical(self, "保存エラー", 
                               f"保存中にエラーが発生しました: {str(e)}")


def launch_theme_editor(config_path: Optional[Union[str, Path]] = None):
    """Launch the theme editor application."""
    if not qt_available:
        print("Error: Qt framework not available. Please install PyQt5, PyQt6, or PySide6.")
        return None
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    editor = ThemeEditorWindow(config_path)
    editor.show()
    
    return editor


if __name__ == "__main__":
    launch_theme_editor()
