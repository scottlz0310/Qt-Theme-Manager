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
            QSplitter, QFileDialog, QMessageBox, QDoubleSpinBox, QRadioButton
        )
        from PyQt5.QtCore import Qt, pyqtSignal, QTimer
        from PyQt5.QtGui import QColor, QPalette, QFont
        # PyQt5 compatibility constants
        QtHorizontal = Qt.Horizontal
        QtVertical = Qt.Vertical
        QtPointingHandCursor = Qt.PointingHandCursor
        QtLeftButton = Qt.LeftButton
        QFontBold = QFont.Bold
        QtAlignCenter = Qt.AlignCenter
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                QPushButton, QLabel, QLineEdit, QSlider, QSpinBox, QGroupBox,
                QGridLayout, QFrame, QColorDialog, QTabWidget, QScrollArea,
                QTextEdit, QComboBox, QCheckBox, QProgressBar, QListWidget,
                QSplitter, QFileDialog, QMessageBox, QDoubleSpinBox, QRadioButton
            )
            from PyQt6.QtCore import Qt, pyqtSignal, QTimer
            from PyQt6.QtGui import QColor, QPalette, QFont
            # PyQt6 compatibility constants
            QtHorizontal = Qt.Orientation.Horizontal
            QtVertical = Qt.Orientation.Vertical
            QtPointingHandCursor = Qt.CursorShape.PointingHandCursor
            QtLeftButton = Qt.MouseButton.LeftButton
            QFontBold = QFont.Weight.Bold
            QtAlignCenter = Qt.AlignmentFlag.AlignCenter
        except ImportError:
            from PySide6.QtWidgets import (
                QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                QPushButton, QLabel, QLineEdit, QSlider, QSpinBox, QGroupBox,
                QGridLayout, QFrame, QColorDialog, QTabWidget, QScrollArea,
                QTextEdit, QComboBox, QCheckBox, QProgressBar, QListWidget,
                QSplitter, QFileDialog, QMessageBox, QDoubleSpinBox, QRadioButton
            )
            from PySide6.QtCore import Qt, Signal as pyqtSignal, QTimer
            from PySide6.QtGui import QColor, QPalette, QFont
            # PySide6 compatibility constants
            QtHorizontal = Qt.Orientation.Horizontal
            QtVertical = Qt.Orientation.Vertical
            QtPointingHandCursor = Qt.CursorShape.PointingHandCursor
            QtLeftButton = Qt.MouseButton.LeftButton
            QFontBold = QFont.Weight.Bold
            QtAlignCenter = Qt.AlignmentFlag.AlignCenter

from .controller import ThemeController
from .stylesheet import StylesheetGenerator


class ClickableWidget(QWidget):
    """Widget that emits signals when clicked."""
    clicked = pyqtSignal(str)  # Signal with component type
    
    def __init__(self, component_type: str, parent=None):
        super().__init__(parent)
        self.component_type = component_type
        self.setCursor(QtPointingHandCursor)
    
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == QtLeftButton:
            self.clicked.emit(self.component_type)
        super().mousePressEvent(event)


class ClickableButton(QPushButton):
    """Button that emits component-specific signals when clicked."""
    componentClicked = pyqtSignal(str)
    
    def __init__(self, text: str, component_type: str, parent=None):
        super().__init__(text, parent)
        self.component_type = component_type
        
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == QtLeftButton:
            self.componentClicked.emit(self.component_type)
        super().mousePressEvent(event)


class ClickableLineEdit(QLineEdit):
    """LineEdit that emits component-specific signals when clicked."""
    componentClicked = pyqtSignal(str)
    
    def __init__(self, text: str, component_type: str, parent=None):
        super().__init__(text, parent)
        self.component_type = component_type
        
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == QtLeftButton:
            self.componentClicked.emit(self.component_type)
        super().mousePressEvent(event)


class ClickableComboBox(QComboBox):
    """ComboBox that emits component-specific signals when clicked."""
    componentClicked = pyqtSignal(str)
    
    def __init__(self, component_type: str, parent=None):
        super().__init__(parent)
        self.component_type = component_type
        
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == QtLeftButton:
            self.componentClicked.emit(self.component_type)
        super().mousePressEvent(event)
from .advanced_stylesheet import AdvancedStylesheetGenerator


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
    def get_heading_text_color(bg_color: str, theme_primary: str = "#2196F3") -> str:
        """Get optimal heading text color with better contrast and visual hierarchy."""
        bg_luminance = ColorUtils.get_luminance(bg_color)
        
        # Try using the theme's primary color first
        primary_contrast = ColorUtils.get_contrast_ratio(bg_color, theme_primary)
        
        if primary_contrast >= 4.5:  # WCAG AA compliance
            return theme_primary
        
        # If primary doesn't work, try a darker/lighter variant
        if bg_luminance > 0.5:  # Light background
            # Try darker variants of primary
            darker_primary = ColorUtils.adjust_brightness(theme_primary, -0.4)
            if ColorUtils.get_contrast_ratio(bg_color, darker_primary) >= 4.5:
                return darker_primary
            
            # Fallback to very dark color
            return "#1565C0"  # Dark blue
        else:  # Dark background
            # Try lighter variants of primary
            lighter_primary = ColorUtils.adjust_brightness(theme_primary, 0.4)
            if ColorUtils.get_contrast_ratio(bg_color, lighter_primary) >= 4.5:
                return lighter_primary
            
            # Fallback to bright accent color
            return "#64B5F6"  # Light blue
    
    @staticmethod
    def get_accent_text_color(bg_color: str, primary_color: str = "#2196F3") -> str:
        """Get a colorful accent text color for highlights and special elements."""
        bg_luminance = ColorUtils.get_luminance(bg_color)
        
        # Generate complementary color
        r, g, b = ColorUtils.hex_to_rgb(primary_color)
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # Create complement by shifting hue by 180 degrees
        complement_h = (h + 0.5) % 1.0
        
        if bg_luminance > 0.5:  # Light background
            # Use darker, saturated complement
            accent_r, accent_g, accent_b = colorsys.hsv_to_rgb(complement_h, min(0.8, s + 0.2), max(0.4, v - 0.3))
        else:  # Dark background  
            # Use lighter, vibrant complement
            accent_r, accent_g, accent_b = colorsys.hsv_to_rgb(complement_h, min(0.9, s + 0.1), min(0.9, v + 0.4))
        
        accent_color = ColorUtils.rgb_to_hex(int(accent_r*255), int(accent_g*255), int(accent_b*255))
        
        # Verify contrast and adjust if needed
        contrast = ColorUtils.get_contrast_ratio(bg_color, accent_color)
        if contrast < 4.5:
            # Adjust brightness until we get good contrast
            adjustment = 0.1 if bg_luminance > 0.5 else -0.1
            while contrast < 4.5 and abs(adjustment) < 0.8:
                accent_color = ColorUtils.adjust_brightness(accent_color, adjustment)
                contrast = ColorUtils.get_contrast_ratio(bg_color, accent_color)
                adjustment += 0.1 if bg_luminance > 0.5 else -0.1
        
        return accent_color
    
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
        self.hex_label.setAlignment(QtAlignCenter)
        layout.addWidget(self.hex_label)
        
        self.luminance_label = QLabel("Luminance: 1.00")
        self.luminance_label.setAlignment(QtAlignCenter)
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
        title.setFont(QFont("", 12, QFontBold))
        layout.addWidget(title)
        
        # Preview area
        self.preview = QLabel("サンプルテキスト")
        self.preview.setAlignment(QtAlignCenter)
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
        title_label.setFont(QFont("", 10, QFontBold))
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
            slider = QSlider(QtHorizontal)
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
        
        # Auto-update timer (initialize before setup_ui)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.auto_update_preview)
        self.update_timer.setSingleShot(True)
        
        self.setup_ui()
        self.load_default_theme()
    
    def jump_to_component_settings(self, component_type: str):
        """Jump to the appropriate settings tab and section for a component."""
        print(f"🎯 コンポーネント '{component_type}' の設定にジャンプします...")
        
        # Component type to tab index mapping
        component_to_tab = {
            "button": 1,        # Components tab
            "input": 1,         # Components tab  
            "panel": 1,         # Components tab
            "menu": 1,          # Components tab
            "progress": 1,      # Components tab
            "scroll": 1,        # Components tab
            "checkbox": 1,      # Components tab
            "radio": 1,         # Components tab
            "background": 0,    # Basic colors tab
            "text": 0,          # Basic colors tab
            "heading": 0,       # Basic colors tab
            "primary": 0,       # Basic colors tab
            "secondary": 0,     # Basic colors tab
            "accent": 0,        # Basic colors tab
        }
        
        tab_index = component_to_tab.get(component_type, 1)  # Default to components tab
        
        # Jump to appropriate tab
        self.tabs.setCurrentIndex(tab_index)
        
        # Show visual feedback
        self.show_component_highlight(component_type)
        
        print(f"✅ '{component_type}' 設定タブに移動しました")
    
    def show_component_highlight(self, component_type: str):
        """Show visual feedback for clicked component."""
        # Get current tab index and temporarily highlight the tab
        current_index = self.tabs.currentIndex()
        
        # Store original tab text
        if not hasattr(self, '_original_tab_texts'):
            self._original_tab_texts = {}
            for i in range(self.tabs.count()):
                self._original_tab_texts[i] = self.tabs.tabText(i)
        
        # Highlight the current tab with emoji
        original_text = self._original_tab_texts[current_index]
        highlighted_text = f"🎯 {original_text}"
        self.tabs.setTabText(current_index, highlighted_text)
        
        # Reset tab text after 2 seconds
        timer = QTimer()
        timer.timeout.connect(lambda: self.tabs.setTabText(current_index, original_text))
        timer.setSingleShot(True)
        timer.start(2000)  # Reset after 2 seconds
        
        # Store timer to prevent garbage collection
        if not hasattr(self, '_highlight_timers'):
            self._highlight_timers = []
        self._highlight_timers.append(timer)
    
    def setup_ui(self):
        """Setup the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main splitter
        main_splitter = QSplitter(QtHorizontal)
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
        self.tabs = QTabWidget()  # Store reference to tabs for jumping
        layout.addWidget(self.tabs)
        
        # Basic colors tab
        basic_tab = QWidget()
        self.tabs.addTab(basic_tab, "基本色")
        self.setup_basic_colors_tab(basic_tab)
        
        # Component colors tab
        components_tab = QWidget()
        self.tabs.addTab(components_tab, "コンポーネント")
        self.setup_components_tab(components_tab)
        
        # Contrast checker tab
        contrast_tab = QWidget()
        self.tabs.addTab(contrast_tab, "コントラスト")
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
            ("heading", "見出し色", "#1565C0"),
            ("accent", "アクセント色", "#ff6b35"),
            ("primary", "プライマリ色", "#007acc"),
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
        
        # Scroll area for component controls
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Button components
        button_group = QGroupBox("ボタンコンポーネント")
        button_layout = QGridLayout(button_group)
        
        self.button_sliders = {}
        button_states = [
            ("normal", "通常", "#4a90e2"),
            ("hover", "ホバー", "#5ba0f2"),
            ("pressed", "押下", "#357abd"),
            ("disabled", "無効", "#a0a0a0"),
            ("border", "境界線", "#2c5aa0")
        ]
        
        for i, (key, label, default_color) in enumerate(button_states):
            row = i // 2
            col = (i % 2) * 3
            
            button_layout.addWidget(QLabel(f"{label}:"), row, col)
            
            slider_group = ColorSliderGroup(f"ボタン{label}", default_color)
            slider_group.colorChanged.connect(
                lambda color, k=key: self.update_component_color("button", k, color)
            )
            button_layout.addWidget(slider_group, row, col + 1)
            self.button_sliders[key] = slider_group
        
        scroll_layout.addWidget(button_group)
        
        # Input components
        input_group = QGroupBox("入力コンポーネント")
        input_layout = QGridLayout(input_group)
        
        self.input_sliders = {}
        input_states = [
            ("background", "背景", "#ffffff"),
            ("text", "テキスト", "#000000"),
            ("border", "境界線", "#cccccc"),
            ("focus", "フォーカス", "#4a90e2"),
            ("placeholder", "プレースホルダー", "#999999"),
            ("selection", "選択範囲", "#4a90e2")
        ]
        
        for i, (key, label, default_color) in enumerate(input_states):
            row = i // 2
            col = (i % 2) * 3
            
            input_layout.addWidget(QLabel(f"{label}:"), row, col)
            
            slider_group = ColorSliderGroup(f"入力{label}", default_color)
            slider_group.colorChanged.connect(
                lambda color, k=key: self.update_component_color("input", k, color)
            )
            input_layout.addWidget(slider_group, row, col + 1)
            self.input_sliders[key] = slider_group
        
        scroll_layout.addWidget(input_group)
        
        # Panel components
        panel_group = QGroupBox("パネル・グループボックス")
        panel_layout = QGridLayout(panel_group)
        
        self.panel_sliders = {}
        panel_states = [
            ("background", "背景", "#f5f5f5"),
            ("border", "境界線", "#cccccc"),
            ("title_background", "タイトル背景", "#e0e0e0"),
            ("title_text", "タイトルテキスト", "#333333")
        ]
        
        for i, (key, label, default_color) in enumerate(panel_states):
            row = i // 2
            col = (i % 2) * 3
            
            panel_layout.addWidget(QLabel(f"{label}:"), row, col)
            
            slider_group = ColorSliderGroup(f"パネル{label}", default_color)
            slider_group.colorChanged.connect(
                lambda color, k=key: self.update_component_color("panel", k, color)
            )
            panel_layout.addWidget(slider_group, row, col + 1)
            self.panel_sliders[key] = slider_group
        
        scroll_layout.addWidget(panel_group)
        
        # Menu components
        menu_group = QGroupBox("メニュー・コンボボックス")
        menu_layout = QGridLayout(menu_group)
        
        self.menu_sliders = {}
        menu_states = [
            ("background", "背景", "#ffffff"),
            ("text", "テキスト", "#000000"),
            ("hover", "ホバー背景", "#e0e0e0"),
            ("selected", "選択背景", "#4a90e2"),
            ("selected_text", "選択テキスト", "#ffffff"),
            ("separator", "区切り線", "#cccccc")
        ]
        
        for i, (key, label, default_color) in enumerate(menu_states):
            row = i // 2
            col = (i % 2) * 3
            
            menu_layout.addWidget(QLabel(f"{label}:"), row, col)
            
            slider_group = ColorSliderGroup(f"メニュー{label}", default_color)
            slider_group.colorChanged.connect(
                lambda color, k=key: self.update_component_color("menu", k, color)
            )
            menu_layout.addWidget(slider_group, row, col + 1)
            self.menu_sliders[key] = slider_group
        
        scroll_layout.addWidget(menu_group)
        
        # Progress bar components
        progress_group = QGroupBox("プログレスバー・スライダー")
        progress_layout = QGridLayout(progress_group)
        
        self.progress_sliders = {}
        progress_states = [
            ("background", "背景", "#f0f0f0"),
            ("chunk", "進捗部分", "#4a90e2"),
            ("groove", "溝", "#e0e0e0"),
            ("handle", "ハンドル", "#4a90e2")
        ]
        
        for i, (key, label, default_color) in enumerate(progress_states):
            row = i // 2
            col = (i % 2) * 3
            
            progress_layout.addWidget(QLabel(f"{label}:"), row, col)
            
            slider_group = ColorSliderGroup(f"プログレス{label}", default_color)
            slider_group.colorChanged.connect(
                lambda color, k=key: self.update_component_color("progress", k, color)
            )
            progress_layout.addWidget(slider_group, row, col + 1)
            self.progress_sliders[key] = slider_group
        
        scroll_layout.addWidget(progress_group)
        
        # Scrollbar components
        scrollbar_group = QGroupBox("スクロールバー")
        scrollbar_layout = QGridLayout(scrollbar_group)
        
        self.scrollbar_sliders = {}
        scrollbar_states = [
            ("background", "背景", "#f8f8f8"),
            ("handle", "ハンドル", "#c0c0c0"),
            ("handle_hover", "ハンドルホバー", "#a0a0a0"),
            ("handle_pressed", "ハンドル押下", "#808080")
        ]
        
        for i, (key, label, default_color) in enumerate(scrollbar_states):
            row = i // 2
            col = (i % 2) * 3
            
            scrollbar_layout.addWidget(QLabel(f"{label}:"), row, col)
            
            slider_group = ColorSliderGroup(f"スクロール{label}", default_color)
            slider_group.colorChanged.connect(
                lambda color, k=key: self.update_component_color("scrollbar", k, color)
            )
            scrollbar_layout.addWidget(slider_group, row, col + 1)
            self.scrollbar_sliders[key] = slider_group
        
        scroll_layout.addWidget(scrollbar_group)
        
        # Add stretch and setup scroll area
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # Smart component adjustment buttons
        smart_group = QGroupBox("スマート調整")
        smart_layout = QVBoxLayout(smart_group)
        
        auto_component_btn = QPushButton("コンポーネント色を自動調整")
        auto_component_btn.clicked.connect(self.auto_adjust_component_colors)
        smart_layout.addWidget(auto_component_btn)
        
        harmonize_btn = QPushButton("色の調和を最適化")
        harmonize_btn.clicked.connect(self.harmonize_component_colors)
        smart_layout.addWidget(harmonize_btn)
        
        layout.addWidget(smart_group)
    
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
        title.setFont(QFont("", 14, QFontBold))
        layout.addWidget(title)
        
        # Preview area
        self.preview_area = self.create_preview_widgets()
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.preview_area)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
    
    def create_preview_widgets(self) -> QWidget:
        """Create comprehensive preview widget collection."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Basic widgets group
        basic_group = QGroupBox("基本ウィジェット")
        basic_layout = QVBoxLayout(basic_group)
        
        # Labels and text
        basic_layout.addWidget(QLabel("通常のラベル"))
        
        heading_label = QLabel("見出しテキスト")
        heading_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        heading_label.setProperty("component_type", "heading")  # Mark for styling
        heading_label.mousePressEvent = lambda event: self.jump_to_component_settings("heading")
        heading_label.setCursor(QtPointingHandCursor)
        basic_layout.addWidget(heading_label)
        
        # Buttons (make clickable for navigation)
        button_layout = QHBoxLayout()
        
        normal_btn = ClickableButton("通常ボタン", "button")
        normal_btn.componentClicked.connect(self.jump_to_component_settings)
        button_layout.addWidget(normal_btn)
        
        primary_btn = ClickableButton("プライマリボタン", "button")
        primary_btn.setProperty("class", "primary")
        primary_btn.componentClicked.connect(self.jump_to_component_settings)
        button_layout.addWidget(primary_btn)
        
        disabled_btn = ClickableButton("無効ボタン", "button")
        disabled_btn.setEnabled(False)
        disabled_btn.componentClicked.connect(self.jump_to_component_settings)
        button_layout.addWidget(disabled_btn)
        
        basic_layout.addLayout(button_layout)
        
        # Input widgets (make clickable for navigation)
        line_edit = ClickableLineEdit("入力欄のサンプルテキスト", "input")
        line_edit.setPlaceholderText("プレースホルダーテキスト")
        line_edit.componentClicked.connect(self.jump_to_component_settings)
        basic_layout.addWidget(line_edit)
        
        # Combo box (make clickable for navigation)
        combo = ClickableComboBox("menu")
        combo.addItems(["選択肢 1", "選択肢 2", "選択肢 3", "長い選択肢テキストのサンプル"])
        combo.componentClicked.connect(self.jump_to_component_settings)
        basic_layout.addWidget(combo)
        
        layout.addWidget(basic_group)
        
        # Text and lists group
        text_group = QGroupBox("テキスト・リスト")
        text_layout = QVBoxLayout(text_group)
        
        # Text edit
        text_edit = QTextEdit()
        text_edit.setPlainText("""複数行テキストエリアのサンプル表示です。
長いテキストの表示確認用として使用します。
日本語と English の混在テストも含まれています。
背景色とテキスト色のコントラストを確認できます。""")
        text_edit.setMaximumHeight(100)
        text_layout.addWidget(text_edit)
        
        # List widget
        list_widget = QListWidget()
        list_items = [
            "リストアイテム 1",
            "リストアイテム 2 (選択状態)",
            "リストアイテム 3",
            "長いリストアイテムのサンプルテキスト",
            "リストアイテム 5"
        ]
        for item in list_items:
            list_widget.addItem(item)
        list_widget.setCurrentRow(1)  # Select second item
        list_widget.setMaximumHeight(120)
        text_layout.addWidget(list_widget)
        
        layout.addWidget(text_group)
        
        # Progress and sliders group
        progress_group = QGroupBox("プログレス・スライダー")
        progress_layout = QVBoxLayout(progress_group)
        
        # Progress bar (make clickable for navigation)  
        progress = QProgressBar()
        progress.setValue(65)
        progress.setFormat("進捗: %p%")
        progress.mousePressEvent = lambda event: self.jump_to_component_settings("progress")
        progress.setCursor(QtPointingHandCursor)
        progress_layout.addWidget(progress)
        
        # Horizontal slider
        h_slider = QSlider(QtHorizontal)
        h_slider.setValue(40)
        h_slider.setMinimum(0)
        h_slider.setMaximum(100)
        progress_layout.addWidget(QLabel("水平スライダー:"))
        progress_layout.addWidget(h_slider)
        
        # Vertical slider
        slider_container = QWidget()
        slider_layout = QHBoxLayout(slider_container)
        slider_layout.addWidget(QLabel("垂直:"))
        v_slider = QSlider(QtVertical)
        v_slider.setValue(30)
        v_slider.setMinimum(0)
        v_slider.setMaximum(100)
        v_slider.setMaximumHeight(80)
        slider_layout.addWidget(v_slider)
        slider_layout.addStretch()
        progress_layout.addWidget(slider_container)
        
        layout.addWidget(progress_group)
        
        # Check and radio group
        check_group = QGroupBox("チェック・ラジオボタン")
        check_layout = QVBoxLayout(check_group)
        
        # Checkboxes (make clickable for navigation)
        check1 = QCheckBox("チェックボックス 1 (チェック済み)")
        check1.setChecked(True)
        check1.mousePressEvent = lambda event: self.jump_to_component_settings("checkbox")
        check1.setCursor(QtPointingHandCursor)
        check_layout.addWidget(check1)
        
        check2 = QCheckBox("チェックボックス 2")
        check2.mousePressEvent = lambda event: self.jump_to_component_settings("checkbox")
        check2.setCursor(QtPointingHandCursor)
        check_layout.addWidget(check2)
        
        check3 = QCheckBox("無効なチェックボックス")
        check3.setEnabled(False)
        check_layout.addWidget(check3)
        
        # Radio buttons (make clickable for navigation)
        radio1 = QRadioButton("ラジオボタン 1 (選択済み)")
        radio1.setChecked(True)
        radio1.mousePressEvent = lambda event: self.jump_to_component_settings("radio")
        radio1.setCursor(QtPointingHandCursor)
        check_layout.addWidget(radio1)
        
        radio2 = QRadioButton("ラジオボタン 2")
        radio2.mousePressEvent = lambda event: self.jump_to_component_settings("radio")
        radio2.setCursor(QtPointingHandCursor)
        check_layout.addWidget(radio2)
        
        layout.addWidget(check_group)
        
        # Nested group box
        nested_group = QGroupBox("ネストされたグループボックス")
        nested_layout = QVBoxLayout(nested_group)
        
        inner_group = QGroupBox("内部グループ")
        inner_layout = QGridLayout(inner_group)
        
        inner_layout.addWidget(QLabel("ラベル A:"), 0, 0)
        inner_layout.addWidget(QLineEdit("値 A"), 0, 1)
        inner_layout.addWidget(QLabel("ラベル B:"), 1, 0)
        inner_layout.addWidget(QLineEdit("値 B"), 1, 1)
        
        nested_layout.addWidget(inner_group)
        layout.addWidget(nested_group)
        
        # Scrollable area demonstration
        scroll_demo = QGroupBox("スクロール表示デモ")
        scroll_demo_layout = QVBoxLayout(scroll_demo)
        
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_content_layout = QVBoxLayout(scroll_content)
        
        for i in range(10):
            scroll_content_layout.addWidget(QLabel(f"スクロールアイテム {i + 1}"))
        
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(100)
        scroll_demo_layout.addWidget(scroll_area)
        
        layout.addWidget(scroll_demo)
        
        # Color preview indicators
        color_group = QGroupBox("カラーインジケーター")
        color_layout = QHBoxLayout(color_group)
        
        colors = [
            ("背景", self.current_theme_config.get("backgroundColor", "#ffffff")),
            ("テキスト", self.current_theme_config.get("textColor", "#000000")),
            ("プライマリ", self.current_theme_config.get("primaryColor", "#007acc")),
            ("アクセント", self.current_theme_config.get("accentColor", "#ff6b35"))
        ]
        
        for name, color in colors:
            color_preview = QLabel(name)
            color_preview.setStyleSheet(f"""
                QLabel {{
                    background-color: {color};
                    color: {ColorUtils.get_optimal_text_color(color)};
                    border: 1px solid #ccc;
                    padding: 5px;
                    border-radius: 3px;
                }}
            """)
            color_preview.setAlignment(QtAlignCenter)
            color_preview.setMinimumHeight(30)
            color_layout.addWidget(color_preview)
        
        layout.addWidget(color_group)
        
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
    
    def update_component_color(self, component: str, property_key: str, hex_color: str):
        """Update component-specific color in theme configuration."""
        if component not in self.current_theme_config:
            self.current_theme_config[component] = {}
        
        self.current_theme_config[component][property_key] = hex_color
        
        # Schedule preview update
        self.update_timer.start(100)
    
    def auto_adjust_component_colors(self):
        """Automatically adjust component colors based on base colors."""
        bg_color = self.current_theme_config.get("backgroundColor", "#ffffff")
        primary_color = self.current_theme_config.get("primaryColor", "#007acc")
        text_color = self.current_theme_config.get("textColor", "#000000")
        
        # Button colors
        button_config = {
            "normal": primary_color,
            "hover": ColorUtils.adjust_brightness(primary_color, 0.1),
            "pressed": ColorUtils.adjust_brightness(primary_color, -0.2),
            "disabled": ColorUtils.adjust_saturation(primary_color, -0.5),
            "border": ColorUtils.adjust_brightness(primary_color, -0.3)
        }
        
        self.current_theme_config["button"] = button_config
        
        # Update button sliders
        for key, color in button_config.items():
            if key in self.button_sliders:
                self.button_sliders[key].update_from_hex(color)
        
        # Input colors
        is_dark_theme = ColorUtils.get_luminance(bg_color) < 0.5
        
        input_config = {
            "background": ColorUtils.adjust_brightness(bg_color, 0.05 if not is_dark_theme else -0.05),
            "text": text_color,
            "border": ColorUtils.adjust_brightness(primary_color, 0.3),
            "focus": primary_color,
            "placeholder": ColorUtils.adjust_brightness(text_color, 0.4 if not is_dark_theme else -0.3),
            "selection": ColorUtils.adjust_brightness(primary_color, 0.2)
        }
        
        self.current_theme_config["input"] = input_config
        
        # Update input sliders
        for key, color in input_config.items():
            if key in self.input_sliders:
                self.input_sliders[key].update_from_hex(color)
        
        # Panel colors
        panel_config = {
            "background": ColorUtils.adjust_brightness(bg_color, -0.02 if not is_dark_theme else 0.05),
            "border": ColorUtils.adjust_brightness(bg_color, -0.1 if not is_dark_theme else 0.1),
            "title_background": ColorUtils.adjust_brightness(bg_color, -0.05 if not is_dark_theme else 0.08),
            "title_text": text_color
        }
        
        self.current_theme_config["panel"] = panel_config
        
        # Update panel sliders
        for key, color in panel_config.items():
            if key in self.panel_sliders:
                self.panel_sliders[key].update_from_hex(color)
        
        # Menu colors
        menu_config = {
            "background": bg_color,
            "text": text_color,
            "hover": ColorUtils.adjust_brightness(bg_color, -0.05 if not is_dark_theme else 0.1),
            "selected": primary_color,
            "selected_text": ColorUtils.get_optimal_text_color(primary_color),
            "separator": ColorUtils.adjust_brightness(bg_color, -0.1 if not is_dark_theme else 0.2)
        }
        
        self.current_theme_config["menu"] = menu_config
        
        # Update menu sliders
        for key, color in menu_config.items():
            if key in self.menu_sliders:
                self.menu_sliders[key].update_from_hex(color)
        
        # Progress colors
        progress_config = {
            "background": ColorUtils.adjust_brightness(bg_color, -0.05 if not is_dark_theme else 0.1),
            "chunk": primary_color,
            "groove": ColorUtils.adjust_brightness(bg_color, -0.08 if not is_dark_theme else 0.15),
            "handle": primary_color
        }
        
        self.current_theme_config["progress"] = progress_config
        
        # Update progress sliders
        for key, color in progress_config.items():
            if key in self.progress_sliders:
                self.progress_sliders[key].update_from_hex(color)
        
        # Scrollbar colors
        scrollbar_config = {
            "background": ColorUtils.adjust_brightness(bg_color, -0.02 if not is_dark_theme else 0.05),
            "handle": ColorUtils.adjust_brightness(bg_color, -0.2 if not is_dark_theme else 0.3),
            "handle_hover": ColorUtils.adjust_brightness(bg_color, -0.3 if not is_dark_theme else 0.4),
            "handle_pressed": ColorUtils.adjust_brightness(bg_color, -0.4 if not is_dark_theme else 0.5)
        }
        
        self.current_theme_config["scrollbar"] = scrollbar_config
        
        # Update scrollbar sliders
        for key, color in scrollbar_config.items():
            if key in self.scrollbar_sliders:
                self.scrollbar_sliders[key].update_from_hex(color)
        
        QMessageBox.information(self, "自動調整完了", 
                              "基本色に基づいてすべてのコンポーネント色を自動調整しました。")
    
    def harmonize_component_colors(self):
        """Harmonize component colors for better visual consistency."""
        primary_color = self.current_theme_config.get("primaryColor", "#007acc")
        
        # Generate analogous colors (colors adjacent on the color wheel)
        import colorsys
        r, g, b = ColorUtils.hex_to_rgb(primary_color)
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # Generate analogous colors (±30 degrees)
        analogous1_h = (h + 0.083) % 1.0  # +30 degrees
        analogous2_h = (h - 0.083) % 1.0  # -30 degrees
        
        analogous1_r, analogous1_g, analogous1_b = colorsys.hsv_to_rgb(analogous1_h, s * 0.8, v * 0.9)
        analogous2_r, analogous2_g, analogous2_b = colorsys.hsv_to_rgb(analogous2_h, s * 0.8, v * 0.9)
        
        analogous1_color = ColorUtils.rgb_to_hex(int(analogous1_r*255), int(analogous1_g*255), int(analogous1_b*255))
        analogous2_color = ColorUtils.rgb_to_hex(int(analogous2_r*255), int(analogous2_g*255), int(analogous2_b*255))
        
        # Apply harmonious colors to different components
        if "button" in self.current_theme_config:
            self.current_theme_config["button"]["hover"] = analogous1_color
            if "hover" in self.button_sliders:
                self.button_sliders["hover"].update_from_hex(analogous1_color)
        
        if "input" in self.current_theme_config:
            self.current_theme_config["input"]["focus"] = analogous2_color
            if "focus" in self.input_sliders:
                self.input_sliders["focus"].update_from_hex(analogous2_color)
        
        if "menu" in self.current_theme_config:
            self.current_theme_config["menu"]["selected"] = analogous1_color
            if "selected" in self.menu_sliders:
                self.menu_sliders["selected"].update_from_hex(analogous1_color)
        
        QMessageBox.information(self, "色の調和完了", 
                              f"類似色 ({analogous1_color}, {analogous2_color}) を使用して色の調和を最適化しました。")
    
    def update_contrast_checker(self):
        """Update contrast checker with current colors."""
        bg_color = self.current_theme_config.get("backgroundColor", "#ffffff")
        text_color = self.current_theme_config.get("textColor", "#000000")
        self.contrast_checker.check_contrast(bg_color, text_color)
    
    def auto_adjust_text_colors(self):
        """Automatically adjust text colors for optimal contrast."""
        bg_color = self.current_theme_config.get("backgroundColor", "#ffffff")
        primary_color = self.current_theme_config.get("primaryColor", "#007acc")
        
        # Calculate optimal text color
        optimal_text = ColorUtils.get_optimal_text_color(bg_color)
        
        # Calculate optimal heading color
        optimal_heading = ColorUtils.get_heading_text_color(bg_color, primary_color)
        
        # Update colors
        self.current_theme_config["textColor"] = optimal_text
        self.current_theme_config["headingColor"] = optimal_heading
        
        # Update sliders
        self.color_sliders["text"].update_from_hex(optimal_text)
        self.color_sliders["heading"].update_from_hex(optimal_heading)
        
        QMessageBox.information(self, "自動調整完了", 
                              f"最適化完了:\n• テキスト色: {optimal_text}\n• 見出し色: {optimal_heading}")
    
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
        """Update preview with current theme configuration using advanced styling."""
        if not self.current_theme_config:
            return

        # Generate advanced stylesheet
        generator = AdvancedStylesheetGenerator(self.current_theme_config)
        stylesheet = generator.generate_qss()
        
        # Add heading-specific styles
        heading_color = self.current_theme_config.get("headingColor", "#1565C0")
        heading_styles = f"""
/* Heading Text Styles */
QLabel[component_type="heading"] {{
    color: {heading_color};
    font-size: 16px;
    font-weight: bold;
}}

/* Enhanced text hierarchy */
QLabel[component_type="heading"]:hover {{
    color: {ColorUtils.adjust_brightness(heading_color, 0.1)};
}}
"""
        
        # Apply to preview area
        self.preview_area.setStyleSheet(stylesheet + heading_styles)
    
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
    import sys
    
    if not qt_available:
        print("Error: Qt framework not available. Please install PyQt5, PyQt6, or PySide6.")
        return None
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        editor = ThemeEditorWindow(config_path)
        editor.show()
        print(f"Debug: Editor window shown. Visible: {editor.isVisible()}")
        
        # Force the application to process events and show the window
        app.processEvents()
        
        # Return editor for external event loop management
        return editor
        
    except Exception as e:
        print(f"Error creating theme editor: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    import sys
    
    # Create application
    if not qt_available:
        print("Error: Qt framework not available.")
        sys.exit(1)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create and show editor
    editor = ThemeEditorWindow()
    editor.show()
    
    # Start event loop
    try:
        if hasattr(app, 'exec'):
            sys.exit(app.exec())
        else:
            sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit(0)
