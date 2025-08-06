#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ゼブラパターン機能付きテーマエディター - ランチャー
"""

import sys
from pathlib import Path

# パッケージパスを追加
sys.path.insert(0, str(Path(__file__).parent))


def launch_zebra_theme_editor():
    """ゼブラパターン機能付きテーマエディターを起動"""

    print("🎨 ゼブラパターン機能付きテーマエディターを起動しています...")

    try:
        # Qt availabilityをチェック
        try:
            from PyQt5.QtWidgets import QApplication

            qt_framework = "PyQt5"
        except ImportError:
            try:
                from PyQt6.QtWidgets import QApplication

                qt_framework = "PyQt6"
            except ImportError:
                try:
                    from PySide6.QtWidgets import QApplication

                    qt_framework = "PySide6"
                except ImportError:
                    print("❌ Qtフレームワークがインストールされていません")
                    print("   以下のいずれかをインストールしてください:")
                    print("   pip install PyQt5")
                    print("   pip install PyQt6")
                    print("   pip install PySide6")
                    return

        print(f"✅ {qt_framework} を使用します")

        # アプリケーションを作成
        app = QApplication(sys.argv)
        app.setApplicationName("Qt Theme Manager - Zebra Pattern Editor")
        app.setApplicationVersion("0.2.3")

        # テーマエディター拡張を試行
        try:
            from theme_editor_zebra_extension import (
                extend_theme_editor_with_zebra,
            )

            extended_editor_class = extend_theme_editor_with_zebra()

            if extended_editor_class:
                print("✅ 統合テーマエディターを起動します")
                editor = extended_editor_class()
                editor.setWindowTitle(
                    "Qt Theme Manager - ゼブラパターン機能付きエディター"
                )
                editor.show()
            else:
                raise ImportError("テーマエディター統合に失敗")

        except ImportError as e:
            print(f"⚠️  統合エディターが利用できません: {e}")
            print(
                "   フォールバック: ゼブラパターンエディター単体を起動します"
            )

            try:
                from zebra_pattern_editor import ZebraPatternEditor

                editor = ZebraPatternEditor()
                editor.setWindowTitle("ゼブラパターンエディター - 単体版")
                editor.resize(700, 500)
                editor.show()

                # テスト用の背景色を設定
                editor.set_base_color("#2d3748")

            except ImportError:
                print("❌ ゼブラパターンエディターも利用できません")
                return

        print("🚀 エディターが起動しました")
        print("\n📖 使用方法:")
        print("   1. 基本色タブで背景色を設定")
        print("   2. ゼブラタブでコントラスト比を調整")
        print("   3. プレビューで結果を確認")
        print("   4. 保存してテーマを適用")

        # イベントループを開始
        sys.exit(app.exec_())

    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback

        traceback.print_exc()


def launch_standalone_zebra_editor():
    """ゼブラパターンエディター単体を起動"""

    print("🦓 ゼブラパターンエディター（単体）を起動しています...")

    try:
        from PyQt5.QtWidgets import QApplication
    except ImportError:
        try:
            from PyQt6.QtWidgets import QApplication
        except ImportError:
            try:
                from PySide6.QtWidgets import QApplication
            except ImportError:
                print("❌ Qtフレームワークがインストールされていません")
                return

    try:
        from zebra_pattern_editor import ZebraPatternEditor

        app = QApplication(sys.argv)

        editor = ZebraPatternEditor()
        editor.setWindowTitle("ゼブラパターンエディター")
        editor.resize(600, 500)
        editor.show()

        # デモ用の色を設定
        demo_colors = ["#ffffff", "#f8f9fa", "#2d3748", "#1a202c", "#4a5568"]
        import random

        demo_color = random.choice(demo_colors)
        editor.set_base_color(demo_color)

        print(f"✅ デモ背景色: {demo_color}")
        print("🎯 コントラスト比スライダーで調整してください")

        sys.exit(app.exec_())

    except ImportError as e:
        print(f"❌ ゼブラパターンエディターが利用できません: {e}")


def demo_zebra_generation():
    """ゼブラパターン生成のデモ"""

    print("🧪 ゼブラパターン生成デモ")
    print("=" * 50)

    try:
        from zebra_pattern_editor import ZebraPatternGenerator

        # テスト用の背景色
        test_colors = [
            ("#ffffff", "ライトテーマ"),
            ("#2d3748", "ダークテーマ"),
            ("#f7fafc", "グレーライト"),
            ("#1a202c", "グレーダーク"),
            ("#ebf8ff", "ブルーライト"),
            ("#2c5282", "ブルーダーク"),
        ]

        for bg_color, theme_name in test_colors:
            print(f"\n📋 {theme_name} ({bg_color})")

            # アクセシビリティレベル別に生成
            for level in ["subtle", "moderate", "high"]:
                result = ZebraPatternGenerator.generate_accessibility_compliant_zebra(
                    bg_color, level
                )

                print(
                    f"  {level:>8}: {result['zebra_color']} "
                    f"(コントラスト: {result['contrast_ratio']:.2f}:1)"
                )

    except ImportError:
        print("❌ ZebraPatternGeneratorが利用できません")

        # シンプルな代替実装
        print("💡 シンプルな明度調整デモ:")

        def simple_adjust(hex_color, percent):
            # 非常にシンプルな明度調整
            hex_color = hex_color.lstrip("#")
            r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

            if sum([r, g, b]) / 3 > 127:  # 明るい色
                factor = 1 - percent / 100
            else:  # 暗い色
                factor = 1 + percent / 100

            r = max(0, min(255, int(r * factor)))
            g = max(0, min(255, int(g * factor)))
            b = max(0, min(255, int(b * factor)))

            return f"#{r:02x}{g:02x}{b:02x}"

        test_colors = ["#ffffff", "#2d3748", "#f0f0f0", "#1a1a1a"]

        for color in test_colors:
            zebra = simple_adjust(color, 5)  # 5%調整
            print(f"  {color} → {zebra}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="ゼブラパターン機能付きテーマエディター"
    )
    parser.add_argument(
        "--mode",
        choices=["full", "zebra", "demo"],
        default="full",
        help="起動モード: full=統合エディター, zebra=ゼブラのみ, demo=生成デモ",
    )

    args = parser.parse_args()

    if args.mode == "full":
        launch_zebra_theme_editor()
    elif args.mode == "zebra":
        launch_standalone_zebra_editor()
    elif args.mode == "demo":
        demo_zebra_generation()
