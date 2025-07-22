"""
GUI preview module for theme visualization.
Provides sample widget window to preview themes with theme switching buttons.
"""

from typing import Optional, Union
from pathlib import Path

# Import Qt availability from controller
from .controller import qt_available, qt_framework

# Import handling for Qt libraries  
if qt_available:
    try:
        from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QListWidget,
            QGroupBox, QFrame, QToolBar, QStatusBar, QListWidgetItem, QScrollArea,
            QGridLayout, QAction
        )
        from PyQt5.QtCore import Qt
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QListWidget,
                QGroupBox, QFrame, QToolBar, QStatusBar, QListWidgetItem, QScrollArea,
                QGridLayout
            )
            from PyQt6.QtCore import Qt
            from PyQt6.QtGui import QAction
        except ImportError:
            from PySide6.QtWidgets import (
                QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, QListWidget,
                QGroupBox, QFrame, QToolBar, QStatusBar, QListWidgetItem, QScrollArea,
                QGridLayout
            )
            from PySide6.QtCore import Qt
            from PySide6.QtGui import QAction

from .controller import ThemeController


class ThemePreviewWindow(QMainWindow if qt_available else object):
    """Preview window for theme visualization."""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize preview window.
        
        Args:
            config_path: Path to theme configuration file
        """
        if not qt_available:
            raise RuntimeError("Qt framework not available. Install PyQt5 or PySide6.")
        
        super().__init__()
        
        self.controller = ThemeController(config_path)
        
        self.setWindowTitle("ThemeManager Preview")
        self.setGeometry(100, 100, 800, 600)
        
        # Create UI
        self._create_ui()
        
        # Apply current theme
        self._apply_current_theme()
    
    def _create_ui(self):
        """Create the preview UI with sample widgets and theme buttons."""
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left side: Theme selection buttons
        self._create_theme_buttons(main_layout)
        
        # Right side: Preview area  
        self._create_preview_area(main_layout)
    
    def _create_theme_buttons(self, main_layout):
        """Create theme selection buttons on the left side."""
        
        # Theme buttons container
        theme_container = QWidget()
        theme_layout = QVBoxLayout(theme_container)
        
        # Title
        theme_title = QLabel("Theme Selection")
        theme_title.setProperty("class", "heading")
        theme_layout.addWidget(theme_title)
        
        # Get available themes
        themes = self.controller.get_available_themes()
        current_theme = self.controller.get_current_theme_name()
        
        # Create buttons in a scrollable area
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        self.theme_buttons = {}
        
        # Create button for each theme
        for theme_name, theme_config in themes.items():
            display_name = theme_config.get("display_name", theme_name)
            description = theme_config.get("description", "")
            
            # Create theme button
            btn = QPushButton(f"{display_name}\n({theme_name})")
            btn.setToolTip(description)
            btn.setMinimumHeight(60)
            btn.setProperty("theme_name", theme_name)
            
            # Highlight current theme
            if theme_name == current_theme:
                btn.setProperty("class", "current_theme")
            
            # Connect button click
            btn.clicked.connect(lambda checked, name=theme_name: self._on_theme_button_clicked(name))
            
            self.theme_buttons[theme_name] = btn
            scroll_layout.addWidget(btn)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumWidth(250)
        
        theme_layout.addWidget(scroll_area)
        theme_container.setMaximumWidth(250)
        
        main_layout.addWidget(theme_container)
    
    def _create_preview_area(self, main_layout):
        """Create preview area with sample widgets."""
        
        # Preview container
        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        
        # Preview title
        preview_title = QLabel("Preview")
        preview_title.setProperty("class", "heading")
        preview_layout.addWidget(preview_title)
        
        # Current theme info
        current_theme = self.controller.get_current_theme_name()
        themes = self.controller.get_available_themes()
        if current_theme in themes:
            theme_config = themes[current_theme]
            display_name = theme_config.get("display_name", current_theme)
            self.current_theme_label = QLabel(f"Current Theme: {display_name}")
        else:
            self.current_theme_label = QLabel(f"Current Theme: {current_theme}")
        
        self.current_theme_label.setProperty("class", "secondary")
        preview_layout.addWidget(self.current_theme_label)
        
        # Sample widgets
        
        # Basic widgets group
        basic_group = QGroupBox("Basic Widgets")
        basic_layout = QVBoxLayout(basic_group)
        
        basic_layout.addWidget(QLabel("Label Text"))
        
        line_edit = QLineEdit("Input Field")
        line_edit.setPlaceholderText("プレースホルダーテキスト")
        basic_layout.addWidget(line_edit)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(QPushButton("通常ボタン"))
        button_layout.addWidget(QPushButton("プライマリボタン"))
        disabled_btn = QPushButton("無効ボタン")
        disabled_btn.setEnabled(False)
        button_layout.addWidget(disabled_btn)
        basic_layout.addLayout(button_layout)
        
        preview_layout.addWidget(basic_group)
        
        # List and combo group
        list_group = QGroupBox("リストとコンボボックス")
        list_layout = QVBoxLayout(list_group)
        
        combo = QComboBox()
        combo.addItems(["オプション1", "オプション2", "オプション3"])
        list_layout.addWidget(QLabel("コンボボックス:"))
        list_layout.addWidget(combo)
        
        list_widget = QListWidget()
        list_widget.setAlternatingRowColors(True)  # ゼブラスタイル有効化
        for i in range(8):
            list_widget.addItem(f"リストアイテム {i+1} - ゼブラスタイル表示")
        list_widget.setMaximumHeight(120)
        list_layout.addWidget(QLabel("リストウィジェット:"))
        list_layout.addWidget(list_widget)
        
        preview_layout.addWidget(list_group)
        
        # Text area group
        text_group = QGroupBox("テキストエリア")
        text_layout = QVBoxLayout(text_group)
        
        text_edit = QTextEdit()
        text_edit.setPlainText("これはサンプルテキストエリアです。\nテーマの表示を確認できます。")
        text_edit.setMaximumHeight(80)
        text_layout.addWidget(text_edit)
        
        preview_layout.addWidget(text_group)
        
        # Text color samples
        color_group = QGroupBox("テキストカラーサンプル")
        color_layout = QVBoxLayout(color_group)
        
        color_layout.addWidget(QLabel("通常テキスト"))
        
        secondary_label = QLabel("セカンダリテキスト")
        secondary_label.setProperty("class", "secondary")
        color_layout.addWidget(secondary_label)
        
        muted_label = QLabel("ミュートテキスト")
        muted_label.setProperty("class", "muted")
        color_layout.addWidget(muted_label)
        
        success_label = QLabel("成功メッセージ")
        success_label.setProperty("class", "success")
        color_layout.addWidget(success_label)
        
        warning_label = QLabel("警告メッセージ")
        warning_label.setProperty("class", "warning")
        color_layout.addWidget(warning_label)
        
        error_label = QLabel("エラーメッセージ")
        error_label.setProperty("class", "error")
        color_layout.addWidget(error_label)
        
        preview_layout.addWidget(color_group)
        
        preview_layout.addStretch()
        
        main_layout.addWidget(preview_container)
    
    def _create_toolbar(self):
        """Create toolbar with sample actions."""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # Sample actions
        action1 = QAction("Action 1", self)
        action2 = QAction("Action 2", self)
        action3 = QAction("Action 3", self)
        
        toolbar.addAction(action1)
        toolbar.addAction(action2)
        toolbar.addSeparator()
        toolbar.addAction(action3)
    
    def _create_status_bar(self):
        """Create status bar."""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready - Theme preview active")
    
    def _on_theme_button_clicked(self, theme_name: str):
        """Handle theme button click."""
        try:
            # Apply the selected theme
            success = self.controller.set_theme(theme_name)
            if success:
                # Update current theme label
                themes = self.controller.get_available_themes()
                if theme_name in themes:
                    theme_config = themes[theme_name]
                    display_name = theme_config.get("display_name", theme_name)
                    self.current_theme_label.setText(f"現在のテーマ: {display_name}")
                else:
                    self.current_theme_label.setText(f"現在のテーマ: {theme_name}")
                
                # Update button styles
                self._update_theme_button_styles(theme_name)
                
                # Apply theme to this window
                self._apply_current_theme()
                
                # Update status bar
                self.statusBar().showMessage(f"テーマを '{theme_name}' に変更しました")
            else:
                self.statusBar().showMessage(f"テーマ '{theme_name}' の適用に失敗しました")
                
        except Exception as e:
            self.statusBar().showMessage(f"エラー: {e}")
    
    def _update_theme_button_styles(self, current_theme: str):
        """Update theme button visual states."""
        for theme_name, button in self.theme_buttons.items():
            if theme_name == current_theme:
                button.setProperty("class", "current_theme")
            else:
                button.setProperty("class", "")
            # Force style update
            button.style().unpolish(button)
            button.style().polish(button)
    
    def _apply_current_theme(self):
        """Apply current theme to the preview window."""
        self.controller.apply_theme_to_widget(self)


def show_preview(config_path: Optional[Union[str, Path]] = None) -> Optional['ThemePreviewWindow']:
    """
    Show theme preview window.
    
    Args:
        config_path: Path to theme configuration file
        
    Returns:
        Preview window instance if Qt is available, None otherwise
    """
    if not qt_available:
        print("Qt framework not available. Install PyQt5 or PySide6 to use preview.")
        return None
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    preview_window = ThemePreviewWindow(config_path)
    preview_window.show()
    
    return preview_window


def launch_preview():
    """Launch theme preview as standalone application (for pip entry point)."""
    if not qt_available:
        print("❌ Qt framework not available.")
        print("📦 Please install a Qt framework:")
        print("   pip install qt-theme-manager[pyqt6]    # for PyQt6")
        print("   pip install qt-theme-manager[pyqt5]    # for PyQt5")
        print("   pip install qt-theme-manager[pyside6]  # for PySide6")
        return 1
    
    import sys
    import argparse
    
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='Qt Theme Manager - プレビューツール')
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='カスタムテーマ設定ファイル（JSON）のパス'
    )
    parser.add_argument(
        '--theme', '-t',
        type=str,
        help='起動時に適用するテーマ名'
    )
    
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    
    print("🎨 ThemeManager - プレビューを起動しています...")
    if args.config:
        print(f"📄 カスタム設定ファイル: {args.config}")
    
    window = ThemePreviewWindow(config_path=args.config)
    window.show()
    
    # 指定されたテーマを適用
    if args.theme and hasattr(window, 'theme_controller'):
        try:
            window.theme_controller.apply_theme(args.theme)
            print(f"🎨 テーマ '{args.theme}' を適用しました")
        except Exception as e:
            print(f"⚠️  テーマ適用エラー: {e}")
    
    try:
        if hasattr(app, 'exec'):
            sys.exit(app.exec())
        else:
            sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("\n👋 プレビューを終了します")
        return 0


if __name__ == "__main__":
    # Run preview if executed directly
    launch_preview()
