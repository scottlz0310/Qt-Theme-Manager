#!/usr/bin/env python3
"""
Main entry point for the theme manager CLI.
"""

import sys
from .cli.themectl import main as cli_main

def main():
    """Main entry point with editor support."""
    # Check if theme editor is requested
    if len(sys.argv) > 1 and sys.argv[1] == "editor":
        # Launch theme editor
        try:
            from .qt.theme_editor import launch_theme_editor
            print("🎨 高度なテーマエディターを起動しています...")
            editor = launch_theme_editor()
            
            if editor is not None:
                from .qt.theme_editor import qt_available
                if qt_available:
                    try:
                        from PyQt5.QtWidgets import QApplication
                    except ImportError:
                        try:
                            from PyQt6.QtWidgets import QApplication  
                        except ImportError:
                            from PySide6.QtWidgets import QApplication
                    
                    app = QApplication.instance()
                    if app is not None:
                        print("🚀 テーマエディターが起動しました！")
                        sys.exit(app.exec_() if hasattr(app, 'exec_') else app.exec())
                else:
                    print("❌ Qtライブラリが見つかりません。")
                    print("以下のコマンドでインストールしてください:")
                    print("  pip install PyQt6")
                    sys.exit(1)
        except ImportError as e:
            print(f"❌ テーマエディターの起動に失敗: {e}")
            print("必要な依存関係をインストールしてください:")
            print("  pip install PyQt6  # または PyQt5, PySide6")
            sys.exit(1)
    else:
        # Use existing CLI
        cli_main()

if __name__ == "__main__":
    main()
