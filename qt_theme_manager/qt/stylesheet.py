"""
QSS stylesheet generation module.
Converts theme configuration to PyQt5/PySide6 QSS stylesheets.
Supports both basic and advanced styling modes.
"""

from typing import Any, Dict

# SVG icons as base64 encoded data for advanced mode
CHECKMARK_SVG = (
    "PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIg"
    "ZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4K"
    "PHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9r"
    "ZS13aWR0aD0iMTIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2lu"
    "PSJyb3VuZCIvPgo8L3N2Zz4K"
)


class StylesheetGenerator:
    """Enhanced generator for PyQt5/PySide6 QSS stylesheets from \
theme configurations with basic and advanced modes."""

    def __init__(
        self, theme_config: Dict[str, Any], advanced_mode: bool = False
    ):
        """
        Initialize stylesheet generator with theme configuration.

        Args:
            theme_config: Theme configuration dictionary
            advanced_mode: Enable advanced styling features (default: False)
        """
        self.theme_config = theme_config
        self.advanced_mode = advanced_mode

    def generate_qss(self) -> str:
        """
        Generate complete QSS stylesheet from theme configuration.

        Returns:
            Complete QSS stylesheet string
        """
        if self.advanced_mode:
            return self._generate_advanced_qss()
        else:
            return self._generate_basic_qss()

    def _generate_basic_qss(self) -> str:
        """Generate basic QSS stylesheet."""
        qss_parts = [
            self._generate_base_styles(),
            self._generate_button_styles(),
            self._generate_input_styles(),
            self._generate_panel_styles(),
            self._generate_toolbar_styles(),
            self._generate_status_styles(),
            self._generate_text_styles(),
        ]

        return "\n\n".join(filter(None, qss_parts))

    def _generate_advanced_qss(self) -> str:
        """Generate advanced QSS stylesheet with comprehensive \
component support."""
        qss_parts = [
            self._generate_base_styles(),
            self._generate_enhanced_button_styles(),
            self._generate_enhanced_input_styles(),
            self._generate_enhanced_panel_styles(),
            self._generate_enhanced_menu_styles(),
            self._generate_enhanced_progress_styles(),
            self._generate_enhanced_scrollbar_styles(),
            self._generate_enhanced_list_styles(),
            self._generate_enhanced_tab_styles(),
            self._generate_toolbar_styles(),
            self._generate_status_styles(),
            self._generate_text_styles(),
            self._generate_checkbox_radio_styles(),
        ]

        return "\n\n".join(filter(None, qss_parts))

    def _generate_base_styles(self) -> str:
        """Generate base widget styles."""
        bg_color = self.theme_config.get("backgroundColor", "#ffffff")
        text_color = self.theme_config.get("textColor", "#000000")

        return f"""
/* Base Widget Styles */
QWidget {{
    background-color: {bg_color};
    color: {text_color};
    font-family: 'Segoe UI', 'Meiryo', sans-serif;
    font-size: 14px;
}}

QMainWindow {{
    background-color: {bg_color};
    color: {text_color};
}}"""

    def _generate_button_styles(self) -> str:
        """Generate button styles."""
        button_config = self.theme_config.get("button", {})

        bg = button_config.get("background", "#f0f0f0")
        text = button_config.get("text", "#000000")
        hover = button_config.get("hover", "#e0e0e0")
        pressed = button_config.get("pressed", "#d0d0d0")
        border = button_config.get("border", "#cccccc")

        return f"""
/* Button Styles */
QPushButton {{
    background-color: {bg};
    color: {text};
    border: 1px solid {border};
    border-radius: 4px;
    padding: 6px 12px;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: {hover};
}}

QPushButton:pressed {{
    background-color: {pressed};
}}

QPushButton:disabled {{
    background-color: #e0e0e0;
    color: #888888;
    border-color: #d0d0d0;
}}

QPushButton[class="current_theme"] {{
    background-color: {hover};
    border: 2px solid {text};
    font-weight: bold;
}}"""

    def _generate_input_styles(self) -> str:
        """Generate input field styles."""
        input_config = self.theme_config.get("input", {})

        bg = input_config.get("background", "#ffffff")
        text = input_config.get("text", "#000000")
        border = input_config.get("border", "#cccccc")
        focus = input_config.get("focus", "#0078d4")
        placeholder = input_config.get("placeholder", "#888888")

        return f"""
/* Input Field Styles */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {bg};
    color: {text};
    border: 1px solid {border};
    border-radius: 4px;
    padding: 6px;
    selection-background-color: {focus};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {focus};
    outline: none;
}}

QLineEdit::placeholder {{
    color: {placeholder};
}}

QComboBox {{
    background-color: {bg};
    color: {text};
    border: 1px solid {border};
    border-radius: 4px;
    padding: 6px;
}}

QComboBox:focus {{
    border-color: {focus};
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid {border};
}}"""

    def _generate_panel_styles(self) -> str:
        """Generate panel and group box styles."""
        panel_config = self.theme_config.get("panel", {})

        bg = panel_config.get("background", "#f8f8f8")
        border = panel_config.get("border", "#ddd")

        header_config = panel_config.get("header", {})
        header_bg = header_config.get("background", "#e2e8f0")
        header_text = header_config.get("text", "#2d3748")
        header_border = header_config.get("border", "#cbd5e0")

        # ゼブラスタイル用の控えめな交互色
        zebra_config = panel_config.get("zebra", {})
        zebra_bg = zebra_config.get(
            "alternate", bg
        )  # デフォルトは通常背景と同色（差なし）

        return f"""
/* Panel and GroupBox Styles */
QGroupBox {{
    background-color: {bg};
    border: 1px solid {border};
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 10px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    background-color: {header_bg};
    color: {header_text};
    border: 1px solid {header_border};
    border-radius: 4px;
}}

QFrame {{
    background-color: {bg};
    border: 1px solid {border};
    border-radius: 4px;
}}

QListWidget, QTreeWidget, QTableWidget {{
    background-color: {bg};
    border: 1px solid {border};
    border-radius: 4px;
    alternate-background-color: {zebra_bg};
}}"""

    def _generate_toolbar_styles(self) -> str:
        """Generate toolbar styles."""
        toolbar_config = self.theme_config.get("toolbar", {})

        bg = toolbar_config.get("background", "#f7fafc")
        text = toolbar_config.get("text", "#2d3748")
        border = toolbar_config.get("border", "#e2e8f0")

        button_config = toolbar_config.get("button", {})
        btn_bg = button_config.get("background", "#ffffff")
        btn_text = button_config.get("text", "#2d3748")
        btn_hover = button_config.get("hover", "#0078d4")
        btn_pressed = button_config.get("pressed", "#e2e8f0")

        return f"""
/* Toolbar Styles */
QToolBar {{
    background-color: {bg};
    color: {text};
    border: 1px solid {border};
    border-radius: 4px;
    spacing: 2px;
}}

QToolButton {{
    background-color: {btn_bg};
    color: {btn_text};
    border: 1px solid {border};
    border-radius: 4px;
    padding: 4px;
    margin: 1px;
}}

QToolButton:hover {{
    background-color: {btn_hover};
    color: white;
}}

QToolButton:pressed {{
    background-color: {btn_pressed};
}}"""

    def _generate_status_styles(self) -> str:
        """Generate status bar styles."""
        status_config = self.theme_config.get("status", {})

        bg = status_config.get("background", "#f7fafc")
        text = status_config.get("text", "#4a5568")
        border = status_config.get("border", "#e2e8f0")

        return f"""
/* Status Bar Styles */
QStatusBar {{
    background-color: {bg};
    color: {text};
    border-top: 1px solid {border};
}}

QStatusBar::item {{
    border: none;
}}"""

    def _generate_text_styles(self) -> str:
        """Generate text-specific styles."""
        text_config = self.theme_config.get("text", {})

        primary = text_config.get("primary", "#2d3748")
        secondary = text_config.get("secondary", "#4a5568")
        muted = text_config.get("muted", "#718096")
        heading = text_config.get("heading", "#1a202c")
        link = text_config.get("link", "#0078d4")
        success = text_config.get("success", "#38a169")
        warning = text_config.get("warning", "#d69e2e")
        error = text_config.get("error", "#e53e3e")

        return f"""
/* Text Styles */
QLabel {{
    color: {primary};
}}

QLabel[class="secondary"] {{
    color: {secondary};
}}

QLabel[class="muted"] {{
    color: {muted};
}}

QLabel[class="heading"] {{
    color: {heading};
    font-weight: bold;
    font-size: 16px;
}}

QLabel[class="link"] {{
    color: {link};
    text-decoration: underline;
}}

QLabel[class="success"] {{
    color: {success};
}}

QLabel[class="warning"] {{
    color: {warning};
}}

QLabel[class="error"] {{
    color: {error};
}}"""

    def _generate_enhanced_button_styles(self) -> str:
        """Generate enhanced button styles with hover and pressed states."""
        button_config = self.theme_config.get("button", {})

        normal_color = button_config.get(
            "normal", self.theme_config.get("primaryColor", "#4a90e2")
        )
        hover_color = button_config.get("hover", "#5ba0f2")
        pressed_color = button_config.get("pressed", "#357abd")
        disabled_color = button_config.get("disabled", "#a0a0a0")
        border_color = button_config.get("border", "#2c5aa0")

        # Calculate optimal text colors (simplified for library version)
        normal_text = "#ffffff"  # Default to white for dark buttons
        hover_text = "#ffffff"
        pressed_text = "#ffffff"
        disabled_text = "#ffffff"

        return f"""
/* Enhanced Button Styles */
QPushButton {{
    background-color: {normal_color};
    color: {normal_text};
    border: 1px solid {border_color};
    padding: 6px 12px;
    border-radius: 4px;
    font-weight: 500;
    min-height: 16px;
}}

QPushButton:hover {{
    background-color: {hover_color};
    color: {hover_text};
    border-color: {hover_color};
}}

QPushButton:pressed {{
    background-color: {pressed_color};
    color: {pressed_text};
    border-color: {pressed_color};
}}

QPushButton:disabled {{
    background-color: {disabled_color};
    color: {disabled_text};
    border-color: {disabled_color};
}}

QPushButton[class="primary"] {{
    background-color: {normal_color};
    color: {normal_text};
    font-weight: bold;
    border: 2px solid {border_color};
}}

QPushButton[class="primary"]:hover {{
    background-color: {hover_color};
    color: {hover_text};
}}"""

    def _generate_enhanced_input_styles(self) -> str:
        """Generate enhanced input field styles."""
        input_config = self.theme_config.get("input", {})
        bg_color = self.theme_config.get("backgroundColor", "#ffffff")
        text_color = self.theme_config.get("textColor", "#000000")

        normal_bg = input_config.get("background", bg_color)
        normal_text = input_config.get("text", text_color)
        border_color = input_config.get("border", "#cccccc")
        focus_color = input_config.get("focus", "#0078d4")
        placeholder_color = input_config.get("placeholder", "#888888")
        error_color = input_config.get("error", "#e53e3e")
        success_color = input_config.get("success", "#38a169")

        return f"""
/* Enhanced Input Field Styles */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {normal_bg};
    color: {normal_text};
    border: 2px solid {border_color};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    selection-background-color: {focus_color};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {focus_color};
    outline: none;
    box-shadow: 0 0 0 2px {focus_color}33;
}}

QLineEdit::placeholder {{
    color: {placeholder_color};
    font-style: italic;
}}

QLineEdit[class="error"] {{
    border-color: {error_color};
    background-color: {error_color}11;
}}

QLineEdit[class="success"] {{
    border-color: {success_color};
    background-color: {success_color}11;
}}

QComboBox {{
    background-color: {normal_bg};
    color: {normal_text};
    border: 2px solid {border_color};
    border-radius: 6px;
    padding: 8px 12px;
    min-width: 100px;
}}

QComboBox:focus {{
    border-color: {focus_color};
    box-shadow: 0 0 0 2px {focus_color}33;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid {border_color};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 4px solid {text_color};
    margin-right: 8px;
}}"""

    def _generate_enhanced_panel_styles(self) -> str:
        """Generate enhanced panel and group box styles."""
        panel_config = self.theme_config.get("panel", {})
        bg_color = self.theme_config.get("backgroundColor", "#ffffff")
        text_color = self.theme_config.get("textColor", "#000000")

        bg = panel_config.get("background", bg_color)
        border = panel_config.get("border", "#ddd")
        # shadow = panel_config.get("shadow", "#00000011")  # Unused for now

        header_config = panel_config.get("header", {})
        header_bg = header_config.get("background", "#e2e8f0")
        header_text = header_config.get("text", "#2d3748")
        header_border = header_config.get("border", "#cbd5e0")

        zebra_config = panel_config.get("zebra", {})
        zebra_bg = zebra_config.get("alternate", bg)

        return f"""
/* Enhanced Panel and GroupBox Styles */
QGroupBox {{
    background-color: {bg};
    border: 2px solid {border};
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: bold;
    color: {text_color};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 8px;
    background-color: {header_bg};
    color: {header_text};
    border: 1px solid {header_border};
    border-radius: 6px;
    margin-left: 8px;
}}

QFrame {{
    background-color: {bg};
    border: 2px solid {border};
    border-radius: 8px;
}}

QFrame[frameShape="4"] {{
    border: 1px solid {border};
    border-radius: 0px;
}}

QListWidget, QTreeWidget, QTableWidget {{
    background-color: {bg};
    border: 2px solid {border};
    border-radius: 8px;
    alternate-background-color: {zebra_bg};
    gridline-color: {border};
    outline: none;
}}

QListWidget::item, QTreeWidget::item, QTableWidget::item {{
    padding: 6px;
    border: none;
    border-radius: 4px;
}}

QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {{
    background-color: {header_bg};
    color: {header_text};
}}

QListWidget::item:hover, QTreeWidget::item:hover, QTableWidget::item:hover {{
    background-color: {header_bg}66;
}}"""

    def _generate_enhanced_menu_styles(self) -> str:
        """Generate enhanced menu styles."""
        menu_config = self.theme_config.get("menu", {})
        bg_color = self.theme_config.get("backgroundColor", "#ffffff")
        text_color = self.theme_config.get("textColor", "#000000")

        bg = menu_config.get("background", bg_color)
        text = menu_config.get("text", text_color)
        border = menu_config.get("border", "#cccccc")
        hover = menu_config.get("hover", "#e2e8f0")
        separator = menu_config.get("separator", "#e2e8f0")

        return f"""
/* Enhanced Menu Styles */
QMenuBar {{
    background-color: {bg};
    color: {text};
    border-bottom: 1px solid {border};
    padding: 4px;
}}

QMenuBar::item {{
    background-color: transparent;
    padding: 6px 12px;
    border-radius: 4px;
}}

QMenuBar::item:selected {{
    background-color: {hover};
}}

QMenu {{
    background-color: {bg};
    color: {text};
    border: 1px solid {border};
    border-radius: 6px;
    padding: 4px 0px;
}}

QMenu::item {{
    padding: 8px 24px;
    border-radius: 4px;
    margin: 1px 4px;
}}

QMenu::item:selected {{
    background-color: {hover};
}}

QMenu::separator {{
    height: 1px;
    background-color: {separator};
    margin: 4px 8px;
}}"""

    def _generate_enhanced_progress_styles(self) -> str:
        """Generate enhanced progress bar styles."""
        progress_config = self.theme_config.get("progress", {})
        bg_color = self.theme_config.get("backgroundColor", "#ffffff")
        text_color = self.theme_config.get("textColor", "#000000")

        bg = progress_config.get("background", "#e2e8f0")
        bar = progress_config.get("bar", "#4a90e2")
        text = progress_config.get("text", text_color)
        border = progress_config.get("border", "#cbd5e0")

        return f"""
/* Enhanced Progress Bar Styles */
QProgressBar {{
    background-color: {bg};
    color: {text};
    border: 2px solid {border};
    border-radius: 6px;
    text-align: center;
    font-weight: bold;
}}

QProgressBar::chunk {{
    background-color: {bar};
    border-radius: 4px;
    margin: 2px;
}}

QProgressBar[textVisible="false"] {{
    min-height: 20px;
}}"""

    def _generate_enhanced_scrollbar_styles(self) -> str:
        """Generate enhanced scrollbar styles."""
        scrollbar_config = self.theme_config.get("scrollbar", {})
        bg_color = self.theme_config.get("backgroundColor", "#ffffff")
        text_color = self.theme_config.get("textColor", "#000000")

        bg = scrollbar_config.get("background", "#f7fafc")
        handle = scrollbar_config.get("handle", "#cbd5e0")
        handle_hover = scrollbar_config.get("handle_hover", "#a0aec0")
        border = scrollbar_config.get("border", "#e2e8f0")

        return f"""
/* Enhanced Scrollbar Styles */
QScrollBar:vertical {{
    background-color: {bg};
    width: 12px;
    border-radius: 6px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {handle};
    border-radius: 6px;
    min-height: 20px;
    margin: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {handle_hover};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {bg};
    height: 12px;
    border-radius: 6px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: {handle};
    border-radius: 6px;
    min-width: 20px;
    margin: 2px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {handle_hover};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}"""

    def _generate_enhanced_list_styles(self) -> str:
        """Generate enhanced list and tree styles."""
        list_config = self.theme_config.get("list", {})
        bg_color = self.theme_config.get("backgroundColor", "#ffffff")
        text_color = self.theme_config.get("textColor", "#000000")

        bg = list_config.get("background", bg_color)
        text = list_config.get("text", text_color)
        border = list_config.get("border", "#e2e8f0")
        selection = list_config.get("selection", "#4a90e2")
        selection_text = list_config.get("selection_text", "#ffffff")

        return f"""
/* Enhanced List and Tree Styles */
QListView, QTreeView {{
    background-color: {bg};
    color: {text};
    border: 2px solid {border};
    border-radius: 8px;
    outline: none;
    alternate-background-color: {bg}ee;
}}

QListView::item, QTreeView::item {{
    padding: 8px;
    border: none;
    border-radius: 4px;
    margin: 1px 4px;
}}

QListView::item:selected, QTreeView::item:selected {{
    background-color: {selection};
    color: {selection_text};
}}

QListView::item:hover, QTreeView::item:hover {{
    background-color: {selection}66;
    color: {text};
}}

QTreeView::branch {{
    background-color: transparent;
}}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {{
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgNkw5IDZMOSA3TDQgN1oiIGZpbGw9IiM0NTQ1NDUiLz4KPC9zdmc+);
}}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {{
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgN0g5VjZINFY3WiIgZmlsbD0iIzQ1NDU0NSIvPgo8L3N2Zz4=);
}}"""

    def _generate_enhanced_tab_styles(self) -> str:
        """Generate enhanced tab styles."""
        tab_config = self.theme_config.get("tab", {})
        bg_color = self.theme_config.get("backgroundColor", "#ffffff")
        text_color = self.theme_config.get("textColor", "#000000")

        bg = tab_config.get("background", bg_color)
        text = tab_config.get("text", text_color)
        selected = tab_config.get("selected", "#4a90e2")
        selected_text = tab_config.get("selected_text", "#ffffff")
        border = tab_config.get("border", "#cccccc")

        return f"""
/* Enhanced Tab Styles */
QTabWidget::pane {{
    background-color: {bg};
    border: 1px solid {border};
    border-radius: 4px;
    margin-top: 2px;
}}

QTabWidget::tab-bar {{
    alignment: left;
}}

QTabBar::tab {{
    background-color: #e0e0e0;
    color: {text};
    border: 1px solid {border};
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    font-weight: 500;
}}

QTabBar::tab:selected {{
    background-color: {selected};
    color: {selected_text};
    border-bottom-color: {bg};
}}

QTabBar::tab:hover {{
    background-color: {selected}66;
    color: {text};
}}

QTabBar::tab:!selected {{
    margin-top: 2px;
}}"""

    def _generate_checkbox_radio_styles(self) -> str:
        """Generate enhanced checkbox and radio button styles."""
        button_config = self.theme_config.get("button", {})
        bg_color = self.theme_config.get("backgroundColor", "#ffffff")
        text_color = self.theme_config.get("textColor", "#000000")

        normal_color = button_config.get(
            "normal", self.theme_config.get("primaryColor", "#4a90e2")
        )
        bg = bg_color
        text = text_color

        return f"""
/* Enhanced Checkbox and Radio Styles */
QCheckBox, QRadioButton {{
    color: {text};
    font-weight: 500;
    spacing: 8px;
}}

QCheckBox::indicator, QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border: 2px solid #cccccc;
    background-color: {bg};
}}

QCheckBox::indicator {{
    border-radius: 3px;
}}

QRadioButton::indicator {{
    border-radius: 8px;
}}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
    background-color: {normal_color};
    border-color: {normal_color};
}}

QCheckBox::indicator:checked {{
    image: url(data:image/svg+xml;base64,{CHECKMARK_SVG});
}}

QRadioButton::indicator:checked {{
    border: 3px solid {bg};
    background-color: {normal_color};
}}

QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
    border-color: {normal_color};
}}

QCheckBox:disabled, QRadioButton:disabled {{
    color: #999999;
}}

QCheckBox::indicator:disabled, QRadioButton::indicator:disabled {{
    border-color: #cccccc;
    background-color: #f5f5f5;
}}"""

    def generate_widget_qss(self, widget_type: str) -> str:
        """
        Generate QSS for specific widget type.

        Args:
            widget_type: Type of widget ('button', 'input', 'panel', etc.)

        Returns:
            QSS string for specific widget type
        """
        generators = {
            "base": self._generate_base_styles,
            "button": self._generate_button_styles,
            "input": self._generate_input_styles,
            "panel": self._generate_panel_styles,
            "toolbar": self._generate_toolbar_styles,
            "status": self._generate_status_styles,
            "text": self._generate_text_styles,
        }

        generator = generators.get(widget_type)
        if generator:
            return generator()
        else:
            raise ValueError(f"Unsupported widget type: {widget_type}")

    @staticmethod
    def validate_theme_config(theme_config: Dict[str, Any]) -> bool:
        """
        Validate theme configuration structure.

        Args:
            theme_config: Theme configuration to validate

        Returns:
            True if valid, False otherwise
        """
        required_keys = [
            "name",
            "display_name",
            "backgroundColor",
            "textColor",
        ]

        for key in required_keys:
            if key not in theme_config:
                return False

        return True
