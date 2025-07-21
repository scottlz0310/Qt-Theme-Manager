#!/usr/bin/env python3
"""
ThemeManager GUI Preview Launcher
デスクトップ環境でGUIプレビューを起動するためのスクリプト
"""

import sys
import os
from pathlib import Path

def main():
    """GUIプレビューを起動"""
    print("ThemeManager GUI Preview Launcher")
    print("=" * 40)
    
    # 仮想環境の確認
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ 仮想環境が見つかりません")
        print("まず仮想環境をセットアップしてください:")
        print("  python -m venv venv")
        print("  source venv/bin/activate  # Linux/Mac")
        print("  pip install -r requirements.txt")
        return 1
    
    # モジュールの確認
    try:
        from theme_manager.qt.controller import qt_available
        from theme_manager.qt.preview import show_preview
        
        if not qt_available:
            print("❌ Qt framework が利用できません")
            print("PyQt5, PyQt6, または PySide6 をインストールしてください:")
            print("  pip install PyQt5")
            print("  pip install PyQt6")
            print("  pip install PySide6")
            return 1
            
        print("✅ ThemeManager GUI components ready")
        
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("依存関係をインストールしてください:")
        print("  pip install -r requirements.txt")
        return 1
    
    # GUI環境の確認
    display = os.environ.get('DISPLAY')
    if not display and sys.platform.startswith('linux'):
        print("⚠️  DISPLAY環境変数が設定されていません")
        print("デスクトップ環境で実行するか、Xサーバーを設定してください")
        print("ヘッドレス環境では実際のGUI表示はできませんが、テストは可能です")
        
        # テストモードで実行
        print("\n🧪 テストモードでプレビュー機能を確認します...")
        return test_mode()
    
    # 実際のGUIプレビューを起動
    print("🚀 GUIプレビューを起動しています...")
    try:
        # 動的にQtフレームワークを検出・インポート
        from theme_manager.qt.controller import qt_framework, qt_available
        
        if not qt_available:
            print("❌ Qtフレームワークが利用できません")
            return 1
            
        print(f"✅ 検出されたQtフレームワーク: {qt_framework}")
        
        # 検出されたフレームワークに応じてQApplicationをインポート
        if qt_framework == "PyQt5":
            from PyQt5.QtWidgets import QApplication
        elif qt_framework == "PyQt6":
            from PyQt6.QtWidgets import QApplication
        elif qt_framework == "PySide6":
            from PySide6.QtWidgets import QApplication
        else:
            print(f"❌ サポートされていないQtフレームワーク: {qt_framework}")
            return 1
        
        app = QApplication.instance() or QApplication(sys.argv)
        preview_window = show_preview()
        
        if preview_window:
            print("✅ プレビューウィンドウが作成されました")
            print("テーマ切り替えボタンを使ってテーマをプレビューできます")
            print("ウィンドウを閉じるか、Ctrl+C で終了してください")
            
            # イベントループを開始
            return app.exec() if hasattr(app, 'exec') else app.exec_()
        else:
            print("❌ プレビューウィンドウの作成に失敗しました")
            return 1
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1

def test_mode():
    """テストモードでの動作確認"""
    try:
        from theme_manager.qt.controller import ThemeController, qt_framework, qt_available
        from theme_manager.qt.preview import show_preview
        
        if not qt_available:
            print("❌ Qtフレームワークが利用できません")
            return 1
            
        print(f"✅ 検出されたQtフレームワーク: {qt_framework}")
        
        # 検出されたフレームワークに応じてQApplicationをインポート
        if qt_framework == "PyQt5":
            from PyQt5.QtWidgets import QApplication
        elif qt_framework == "PyQt6":
            from PyQt6.QtWidgets import QApplication
        elif qt_framework == "PySide6":
            from PySide6.QtWidgets import QApplication
        else:
            print(f"❌ サポートされていないQtフレームワーク: {qt_framework}")
            return 1
        
        # コントローラーのテスト
        controller = ThemeController()
        themes = list(controller.get_available_themes())
        print(f"✅ {len(themes)}個のテーマを読み込みました")
        print(f"   利用可能テーマ: {', '.join(themes[:5])}" + 
              (", ..." if len(themes) > 5 else ""))
        
        # アプリケーション作成
        app = QApplication.instance() or QApplication([])
        
        # プレビューウィンドウ作成
        preview_window = show_preview()
        if preview_window:
            print("✅ プレビューウィンドウ作成成功")
            print("✅ GUI機能は正常に動作しています")
            print("📝 デスクトップ環境で実行すると実際のGUIが表示されます")
        else:
            print("❌ プレビューウィンドウ作成失敗")
            return 1
            
        return 0
        
    except Exception as e:
        print(f"❌ テストモードエラー: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
