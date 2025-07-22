"""
QSS stylesheet generation module.
Converts theme configuration to PyQt5/PySide6 QSS stylesheets.
"""

from typing import Dict, Any


class StylesheetGenerator:
    """Generator for PyQt5/PySide6 QSS stylesheets from theme configurations."""
    
    def __init__(self, theme_config: Dict[str, Any]):
        """
        Initialize stylesheet generator with theme configuration.
        
        Args:
            theme_config: Theme configuration dictionary
        """
        self.theme_config = theme_config
    
    def generate_qss(self) -> str:
        """
        Generate complete QSS stylesheet from theme configuration.
        
        Returns:
            Complete QSS stylesheet string
        """
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
        zebra_bg = zebra_config.get("alternate", bg)  # デフォルトは通常背景と同色（差なし）
        
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
    
    def generate_widget_qss(self, widget_type: str) -> str:
        """
        Generate QSS for specific widget type.
        
        Args:
            widget_type: Type of widget ('button', 'input', 'panel', etc.)
            
        Returns:
            QSS string for specific widget type
        """
        generators = {
            'base': self._generate_base_styles,
            'button': self._generate_button_styles,
            'input': self._generate_input_styles,
            'panel': self._generate_panel_styles,
            'toolbar': self._generate_toolbar_styles,
            'status': self._generate_status_styles,
            'text': self._generate_text_styles,
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
        required_keys = ["name", "display_name", "backgroundColor", "textColor"]
        
        for key in required_keys:
            if key not in theme_config:
                return False
        
        return True
