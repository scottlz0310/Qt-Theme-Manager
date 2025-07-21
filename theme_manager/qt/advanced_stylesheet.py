"""
Enhanced QSS stylesheet generation for comprehensive theme components.
Supports advanced component styling with the theme editor.
"""

from typing import Dict, Any
from .stylesheet import StylesheetGenerator


class AdvancedStylesheetGenerator(StylesheetGenerator):
    """Enhanced stylesheet generator with comprehensive component support."""
    
    def generate_qss(self) -> str:
        """Generate complete QSS stylesheet with enhanced component support."""
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
        ]
        
        return "\n\n".join(filter(None, qss_parts))
    
    def _generate_enhanced_button_styles(self) -> str:
        """Generate enhanced button styles with hover and pressed states."""
        button_config = self.theme_config.get("button", {})
        
        normal_color = button_config.get("normal", self.theme_config.get("primaryColor", "#4a90e2"))
        hover_color = button_config.get("hover", "#5ba0f2")
        pressed_color = button_config.get("pressed", "#357abd") 
        disabled_color = button_config.get("disabled", "#a0a0a0")
        border_color = button_config.get("border", "#2c5aa0")
        
        # Calculate optimal text colors
        from .theme_editor import ColorUtils
        normal_text = ColorUtils.get_optimal_text_color(normal_color)
        hover_text = ColorUtils.get_optimal_text_color(hover_color)
        pressed_text = ColorUtils.get_optimal_text_color(pressed_color)
        disabled_text = ColorUtils.get_optimal_text_color(disabled_color)
        
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
    /* QSS doesn't support opacity, disabled state handled by color */
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
    /* Enhanced visual feedback through color and border */
    border: 2px solid {hover_color};
}}
"""
    
    def _generate_enhanced_input_styles(self) -> str:
        """Generate enhanced input field styles."""
        input_config = self.theme_config.get("input", {})
        
        bg_color = input_config.get("background", "#ffffff")
        text_color = input_config.get("text", "#000000")
        border_color = input_config.get("border", "#cccccc")
        focus_color = input_config.get("focus", "#4a90e2")
        placeholder_color = input_config.get("placeholder", "#999999")
        selection_color = input_config.get("selection", "#4a90e2")
        
        return f"""
/* Enhanced Input Styles */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {{
    background-color: {bg_color};
    color: {text_color};
    border: 2px solid {border_color};
    padding: 6px 8px;
    border-radius: 4px;
    font-size: 14px;
    selection-background-color: {selection_color};
    selection-color: white;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, 
QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {focus_color};
    outline: none;
    /* QSS doesn't support box-shadow, using border instead */
    border: 2px solid {focus_color};
}}

QLineEdit::placeholder, QTextEdit::placeholder, QPlainTextEdit::placeholder {{
    color: {placeholder_color};
}}

QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    background-color: {border_color};
    border: none;
    width: 16px;
    border-radius: 2px;
}}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background-color: {focus_color};
}}
"""
    
    def _generate_enhanced_panel_styles(self) -> str:
        """Generate enhanced panel and group box styles."""
        panel_config = self.theme_config.get("panel", {})
        
        bg_color = panel_config.get("background", "#f5f5f5")
        border_color = panel_config.get("border", "#cccccc")
        title_bg = panel_config.get("title_background", "#e0e0e0")
        title_text = panel_config.get("title_text", "#333333")
        
        return f"""
/* Enhanced Panel Styles */
QGroupBox {{
    background-color: {bg_color};
    border: 2px solid {border_color};
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: 500;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 8px;
    padding: 4px 8px;
    background-color: {title_bg};
    color: {title_text};
    border: 1px solid {border_color};
    border-radius: 3px;
    font-weight: bold;
}}

QFrame {{
    background-color: {bg_color};
    border: 1px solid {border_color};
    border-radius: 4px;
}}

QFrame[frameShape="4"] {{ /* Box frame */
    border: 2px solid {border_color};
}}

QFrame[frameShape="5"] {{ /* Panel frame */
    border: 1px inset {border_color};
}}
"""
    
    def _generate_enhanced_menu_styles(self) -> str:
        """Generate enhanced menu and combo box styles."""
        menu_config = self.theme_config.get("menu", {})
        
        bg_color = menu_config.get("background", "#ffffff")
        text_color = menu_config.get("text", "#000000")
        hover_color = menu_config.get("hover", "#e0e0e0")
        selected_color = menu_config.get("selected", "#4a90e2")
        selected_text = menu_config.get("selected_text", "#ffffff")
        separator_color = menu_config.get("separator", "#cccccc")
        
        return f"""
/* Enhanced Menu Styles */
QComboBox {{
    background-color: {bg_color};
    color: {text_color};
    border: 2px solid {separator_color};
    border-radius: 4px;
    padding: 6px 8px;
    min-width: 80px;
}}

QComboBox:hover {{
    border-color: {selected_color};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
    background-color: transparent;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid {text_color};
    width: 0px;
    height: 0px;
}}

QComboBox QAbstractItemView {{
    background-color: {bg_color};
    color: {text_color};
    border: 1px solid {separator_color};
    border-radius: 4px;
    selection-background-color: {selected_color};
    selection-color: {selected_text};
    outline: none;
    padding: 4px;
}}

QComboBox QAbstractItemView::item {{
    padding: 8px;
    border: none;
    border-radius: 2px;
    margin: 1px;
}}

QComboBox QAbstractItemView::item:hover {{
    background-color: {hover_color};
}}

QComboBox QAbstractItemView::item:selected {{
    background-color: {selected_color};
    color: {selected_text};
}}

QMenu {{
    background-color: {bg_color};
    color: {text_color};
    border: 1px solid {separator_color};
    border-radius: 4px;
    padding: 4px;
}}

QMenu::item {{
    padding: 8px 16px;
    border-radius: 2px;
    margin: 1px;
}}

QMenu::item:selected {{
    background-color: {selected_color};
    color: {selected_text};
}}

QMenu::separator {{
    height: 1px;
    background-color: {separator_color};
    margin: 4px 8px;
}}
"""
    
    def _generate_enhanced_progress_styles(self) -> str:
        """Generate enhanced progress bar and slider styles."""
        progress_config = self.theme_config.get("progress", {})
        
        bg_color = progress_config.get("background", "#f0f0f0")
        chunk_color = progress_config.get("chunk", "#4a90e2")
        groove_color = progress_config.get("groove", "#e0e0e0")
        handle_color = progress_config.get("handle", "#4a90e2")
        
        return f"""
/* Enhanced Progress Styles */
QProgressBar {{
    background-color: {bg_color};
    border: 1px solid {groove_color};
    border-radius: 8px;
    height: 16px;
    text-align: center;
    font-weight: bold;
}}

QProgressBar::chunk {{
    background-color: {chunk_color};
    border-radius: 7px;
    margin: 1px;
}}

QSlider::groove:horizontal {{
    background-color: {groove_color};
    height: 6px;
    border-radius: 3px;
    margin: 0px;
}}

QSlider::handle:horizontal {{
    background-color: {handle_color};
    border: 2px solid {handle_color};
    width: 16px;
    height: 16px;
    margin: -8px 0px;
    border-radius: 8px;
}}

QSlider::handle:horizontal:hover {{
    background-color: {handle_color};
    border-color: {handle_color};
    /* QSS doesn't support transform:scale, using padding for visual feedback */
    padding: 1px;
}}

QSlider::groove:vertical {{
    background-color: {groove_color};
    width: 6px;
    border-radius: 3px;
    margin: 0px;
}}

QSlider::handle:vertical {{
    background-color: {handle_color};
    border: 2px solid {handle_color};
    width: 16px;
    height: 16px;
    margin: 0px -8px;
    border-radius: 8px;
}}

QSlider::sub-page:horizontal {{
    background-color: {chunk_color};
    border-radius: 3px;
}}

QSlider::add-page:vertical {{
    background-color: {chunk_color};
    border-radius: 3px;
}}
"""
    
    def _generate_enhanced_scrollbar_styles(self) -> str:
        """Generate enhanced scrollbar styles."""
        scrollbar_config = self.theme_config.get("scrollbar", {})
        
        bg_color = scrollbar_config.get("background", "#f8f8f8")
        handle_color = scrollbar_config.get("handle", "#c0c0c0")
        handle_hover = scrollbar_config.get("handle_hover", "#a0a0a0")
        handle_pressed = scrollbar_config.get("handle_pressed", "#808080")
        
        return f"""
/* Enhanced Scrollbar Styles */
QScrollBar:vertical {{
    background-color: {bg_color};
    width: 12px;
    border: none;
    border-radius: 6px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {handle_color};
    border: none;
    border-radius: 6px;
    min-height: 20px;
    margin: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {handle_hover};
}}

QScrollBar::handle:vertical:pressed {{
    background-color: {handle_pressed};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    background: none;
    border: none;
    width: 0px;
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {bg_color};
    height: 12px;
    border: none;
    border-radius: 6px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: {handle_color};
    border: none;
    border-radius: 6px;
    min-width: 20px;
    margin: 2px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {handle_hover};
}}

QScrollBar::handle:horizontal:pressed {{
    background-color: {handle_pressed};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    background: none;
    border: none;
    width: 0px;
    height: 0px;
}}
"""
    
    def _generate_enhanced_list_styles(self) -> str:
        """Generate enhanced list widget styles."""
        menu_config = self.theme_config.get("menu", {})
        
        bg_color = menu_config.get("background", "#ffffff")
        text_color = menu_config.get("text", "#000000")
        hover_color = menu_config.get("hover", "#e0e0e0")
        selected_color = menu_config.get("selected", "#4a90e2")
        selected_text = menu_config.get("selected_text", "#ffffff")
        
        return f"""
/* Enhanced List Styles */
QListWidget, QTreeWidget, QTableWidget {{
    background-color: {bg_color};
    color: {text_color};
    border: 1px solid #cccccc;
    border-radius: 4px;
    selection-background-color: {selected_color};
    selection-color: {selected_text};
    outline: none;
    gridline-color: #e0e0e0;
}}

QListWidget::item, QTreeWidget::item, QTableWidget::item {{
    padding: 6px;
    border: none;
    border-radius: 2px;
    margin: 1px;
}}

QListWidget::item:hover, QTreeWidget::item:hover, QTableWidget::item:hover {{
    background-color: {hover_color};
}}

QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {{
    background-color: {selected_color};
    color: {selected_text};
}}

QHeaderView::section {{
    background-color: #f5f5f5;
    color: {text_color};
    border: 1px solid #cccccc;
    padding: 8px;
    font-weight: bold;
}}

QHeaderView::section:hover {{
    background-color: {hover_color};
}}
"""
    
    def _generate_enhanced_tab_styles(self) -> str:
        """Generate enhanced tab widget styles."""
        panel_config = self.theme_config.get("panel", {})
        menu_config = self.theme_config.get("menu", {})
        
        bg_color = panel_config.get("background", "#f5f5f5")
        selected_color = menu_config.get("selected", "#4a90e2")
        selected_text = menu_config.get("selected_text", "#ffffff")
        text_color = menu_config.get("text", "#000000")
        
        return f"""
/* Enhanced Tab Styles */
QTabWidget::pane {{
    background-color: {bg_color};
    border: 1px solid #cccccc;
    border-radius: 4px;
    margin-top: 2px;
}}

QTabWidget::tab-bar {{
    alignment: left;
}}

QTabBar::tab {{
    background-color: #e0e0e0;
    color: {text_color};
    border: 1px solid #cccccc;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    font-weight: 500;
}}

QTabBar::tab:selected {{
    background-color: {selected_color};
    color: {selected_text};
    border-bottom-color: {bg_color};
}}

QTabBar::tab:hover {{
    background-color: {selected_color}66;
    color: {text_color};
}}

QTabBar::tab:!selected {{
    margin-top: 2px;
}}
"""

    def _generate_checkbox_radio_styles(self) -> str:
        """Generate enhanced checkbox and radio button styles."""
        button_config = self.theme_config.get("button", {})
        
        normal_color = button_config.get("normal", self.theme_config.get("primaryColor", "#4a90e2"))
        bg_color = self.theme_config.get("backgroundColor", "#ffffff")
        text_color = self.theme_config.get("textColor", "#000000")
        
        return f"""
/* Enhanced Checkbox and Radio Styles */
QCheckBox, QRadioButton {{
    color: {text_color};
    font-weight: 500;
    spacing: 8px;
}}

QCheckBox::indicator, QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border: 2px solid #cccccc;
    background-color: {bg_color};
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
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
}}

QRadioButton::indicator:checked {{
    border: 3px solid {bg_color};
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
}}
"""
