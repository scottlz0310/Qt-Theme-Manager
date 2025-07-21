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
        
        # Check Qt availability
        from theme_manager.qt.theme_editor import qt_available
        
        if not qt_available:
            print("❌ Qtライブラリが見つかりません。")
            print("以下のコマンドでインストールしてください:")
            print("  pip install PyQt6")
            print("  または")
            print("  pip install PyQt5")
            print("  または") 
            print("  pip install PySide6")
            sys.exit(1)
        
        # Import Qt classes
        try:
            from PyQt5.QtWidgets import QApplication
        except ImportError:
            try:
                from PyQt6.QtWidgets import QApplication
            except ImportError:
                from PySide6.QtWidgets import QApplication
        
        from theme_manager.qt.theme_editor import ThemeEditorWindow
        
        # Create application if needed
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create and show editor
        editor = ThemeEditorWindow()
        editor.show()
        print("✅ エディターが正常に作成されました")
        print("\n🚀 テーマエディターが起動しました！")
        
        # Start event loop
        try:
            if hasattr(app, 'exec'):
                sys.exit(app.exec())
            else:
                sys.exit(app.exec_())
        except KeyboardInterrupt:
            print("\n👋 エディターを終了します")
            sys.exit(0)
                
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("\n必要な依存関係をインストールしてください:")
        print("  pip install PyQt6  # または PyQt5, PySide6")
        sys.exit(1)
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
