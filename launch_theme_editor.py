#!/usr/bin/env python3
"""
Launch script for the advanced theme editor.
"""

import sys
from pathlib import Path

# Add the theme_manager to the path
current_dir = Path(__file__).parent
theme_manager_dir = current_dir / "theme_manager"
sys.path.insert(0, str(current_dir))

def main():
    """Main entry point for theme editor."""
    try:
        from theme_manager.qt.theme_editor import launch_theme_editor
        
        print("🎨 ThemeManager - 高度なテーマエディターを起動しています...")
        print("=" * 60)
        print("機能:")
        print("  ✓ リアルタイムカラー調整 (RGBスライダー)")
        print("  ✓ WCAGコントラスト比チェック")
        print("  ✓ 自動テキスト色最適化")
        print("  ✓ カラーパレット自動生成")
        print("  ✓ ライブプレビュー")
        print("  ✓ テーマのエクスポート/インポート")
        print("=" * 60)
        
        # Launch the editor
        editor = launch_theme_editor()
        
        if editor is not None:
            from theme_manager.qt.theme_editor import qt_available
            
            if qt_available:
                # Get the Qt application instance
                try:
                    from PyQt5.QtWidgets import QApplication
                except ImportError:
                    try:
                        from PyQt6.QtWidgets import QApplication  
                    except ImportError:
                        from PySide6.QtWidgets import QApplication
                
                app = QApplication.instance()
                if app is not None:
                    print("\n🚀 テーマエディターが起動しました！")
                    sys.exit(app.exec_() if hasattr(app, 'exec_') else app.exec())
            else:
                print("❌ Qtライブラリが見つかりません。")
                print("以下のコマンドでインストールしてください:")
                print("  pip install PyQt6")
                print("  または")
                print("  pip install PyQt5")
                print("  または") 
                print("  pip install PySide6")
                sys.exit(1)
                
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("\n必要な依存関係をインストールしてください:")
        print("  pip install PyQt6  # または PyQt5, PySide6")
        sys.exit(1)
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
