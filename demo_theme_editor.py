#!/usr/bin/env python3
"""
Demo script to test the ColorUtils class and show color theory capabilities.
"""

import sys
import json
from pathlib import Path

# Add the theme_manager to the path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_color_utils():
    """Test and demonstrate ColorUtils functionality."""
    from theme_manager.qt.theme_editor import ColorUtils
    
    print("🎨 ColorUtils クラスのテスト")
    print("=" * 50)
    
    # Test colors
    test_colors = [
        ("#ffffff", "白"),
        ("#000000", "黒"), 
        ("#ff0000", "赤"),
        ("#00ff00", "緑"),
        ("#0000ff", "青"),
        ("#ffff00", "黄色"),
        ("#ff00ff", "マゼンタ"),
        ("#00ffff", "シアン"),
        ("#808080", "グレー"),
        ("#1a1a1a", "ダークグレー")
    ]
    
    print("輝度計算テスト:")
    print("-" * 30)
    for hex_color, name in test_colors:
        luminance = ColorUtils.get_luminance(hex_color)
        optimal_text = ColorUtils.get_optimal_text_color(hex_color)
        print(f"{name:12} {hex_color}: 輝度={luminance:.3f}, 最適テキスト={optimal_text}")
    
    print("\nコントラスト比テスト:")
    print("-" * 30)
    
    # Test contrast combinations
    contrast_tests = [
        ("#ffffff", "#000000", "白背景-黒文字"),
        ("#000000", "#ffffff", "黒背景-白文字"),
        ("#1a1a1a", "#eeeeee", "ダーク背景-ライト文字"),
        ("#007acc", "#ffffff", "青背景-白文字"),
        ("#ff6b35", "#ffffff", "オレンジ背景-白文字"),
        ("#ffff00", "#000000", "黄色背景-黒文字"),
        ("#808080", "#ffffff", "グレー背景-白文字"),
    ]
    
    for bg_color, text_color, description in contrast_tests:
        contrast = ColorUtils.get_contrast_ratio(bg_color, text_color)
        aa_pass = ColorUtils.is_accessible(bg_color, text_color, "AA")
        aaa_pass = ColorUtils.is_accessible(bg_color, text_color, "AAA")
        
        status_aa = "✅" if aa_pass else "❌"
        status_aaa = "✅" if aaa_pass else "❌"
        
        print(f"{description:20}: {contrast:5.2f}:1  AA{status_aa} AAA{status_aaa}")
    
    print("\n色調整テスト:")
    print("-" * 30)
    base_color = "#007acc"
    print(f"ベース色: {base_color}")
    
    adjustments = [
        (0.2, "明度+20%"),
        (-0.2, "明度-20%"),
        (0.0, "変更なし")
    ]
    
    for factor, description in adjustments:
        adjusted = ColorUtils.adjust_brightness(base_color, factor)
        print(f"{description:12}: {adjusted}")
    
    print("\nカラーパレット生成デモ:")
    print("-" * 30)
    
    # Generate a theme palette
    base_colors = ["#ff6b35", "#007acc", "#28a745", "#6f42c1"]
    
    for base_color in base_colors:
        print(f"\nベース色: {base_color}")
        
        # Generate variations
        darker = ColorUtils.adjust_brightness(base_color, -0.3)
        lighter = ColorUtils.adjust_brightness(base_color, 0.3)
        desaturated = ColorUtils.adjust_saturation(base_color, -0.3)
        
        print(f"  暗い色:   {darker}")
        print(f"  明るい色: {lighter}")
        print(f"  彩度低:   {desaturated}")
        
        # Check accessibility with white/black text
        white_contrast = ColorUtils.get_contrast_ratio(base_color, "#ffffff")
        black_contrast = ColorUtils.get_contrast_ratio(base_color, "#000000")
        optimal_text = ColorUtils.get_optimal_text_color(base_color)
        
        print(f"  白文字との比: {white_contrast:.2f}:1")
        print(f"  黒文字との比: {black_contrast:.2f}:1")
        print(f"  推奨文字色:   {optimal_text}")

def create_sample_theme():
    """Create a sample theme using color theory."""
    from theme_manager.qt.theme_editor import ColorUtils
    
    print("\n🎯 インテリジェントテーマ生成デモ")
    print("=" * 50)
    
    # User picks a primary color
    primary_color = "#6c63ff"  # Nice purple
    print(f"選択されたプライマリ色: {primary_color}")
    
    # Generate background colors based on luminance rules
    primary_luminance = ColorUtils.get_luminance(primary_color)
    
    if primary_luminance > 0.5:
        # Light primary -> generate light theme
        background_color = "#ffffff"
        secondary_bg = ColorUtils.adjust_brightness(primary_color, 0.4)
        text_color = "#2d3748"
    else:
        # Dark primary -> generate dark theme
        background_color = "#1a202c"
        secondary_bg = ColorUtils.adjust_brightness(primary_color, -0.4)
        text_color = "#f7fafc"
    
    # Generate accent color (complementary)
    import colorsys
    r, g, b = ColorUtils.hex_to_rgb(primary_color)
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    
    # Complementary color (180 degrees)
    accent_h = (h + 0.5) % 1.0
    accent_r, accent_g, accent_b = colorsys.hsv_to_rgb(accent_h, s * 0.8, v * 0.9)
    accent_color = ColorUtils.rgb_to_hex(int(accent_r*255), int(accent_g*255), int(accent_b*255))
    
    # Generate button colors with proper contrast
    button_bg = ColorUtils.adjust_brightness(primary_color, -0.1)
    button_hover = ColorUtils.adjust_brightness(primary_color, 0.1)
    button_text = ColorUtils.get_optimal_text_color(button_bg)
    
    # Create theme configuration
    theme_config = {
        "name": "ai_generated_theme",
        "display_name": "AI生成テーマ",
        "description": "色彩理論に基づいて自動生成されたテーマ",
        "backgroundColor": background_color,
        "textColor": text_color,
        "primaryColor": primary_color,
        "accentColor": accent_color,
        "button": {
            "background": button_bg,
            "text": button_text,
            "hover": button_hover,
            "pressed": ColorUtils.adjust_brightness(button_bg, -0.2),
            "border": ColorUtils.adjust_brightness(button_bg, -0.3)
        },
        "panel": {
            "background": secondary_bg,
            "border": ColorUtils.adjust_brightness(secondary_bg, -0.2),
            "header": {
                "background": ColorUtils.adjust_brightness(secondary_bg, -0.1),
                "text": ColorUtils.get_optimal_text_color(secondary_bg),
                "border": ColorUtils.adjust_brightness(secondary_bg, -0.3)
            }
        },
        "input": {
            "background": ColorUtils.adjust_brightness(background_color, -0.05 if background_color == "#ffffff" else 0.1),
            "text": text_color,
            "border": ColorUtils.adjust_brightness(primary_color, 0.2),
            "focus": primary_color,
            "placeholder": ColorUtils.adjust_brightness(text_color, 0.3 if text_color.startswith("#f") else -0.3)
        }
    }
    
    print("\n生成されたテーマ設定:")
    print("-" * 30)
    for key, value in theme_config.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict):
                    print(f"  {sub_key}:")
                    for sub_sub_key, sub_sub_value in sub_value.items():
                        print(f"    {sub_sub_key}: {sub_sub_value}")
                else:
                    print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
    
    # Accessibility check
    print("\nアクセシビリティチェック:")
    print("-" * 30)
    
    bg_text_contrast = ColorUtils.get_contrast_ratio(background_color, text_color)
    button_contrast = ColorUtils.get_contrast_ratio(button_bg, button_text)
    
    print(f"背景-テキスト コントラスト: {bg_text_contrast:.2f}:1 {'✅' if bg_text_contrast >= 4.5 else '❌'}")
    print(f"ボタン コントラスト: {button_contrast:.2f}:1 {'✅' if button_contrast >= 4.5 else '❌'}")
    
    # Save theme to file
    output_file = "ai_generated_theme.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(theme_config, f, indent=2, ensure_ascii=False)
    
    print(f"\nテーマを '{output_file}' に保存しました。")
    
    return theme_config

def main():
    """Main demo function."""
    print("🧪 Theme Editor - 色彩理論デモンストレーション")
    print("=" * 60)
    
    try:
        # Test color utilities
        test_color_utils()
        
        # Create sample theme
        create_sample_theme()
        
        print("\n🎉 デモ完了!")
        print("=" * 60)
        print("高度なテーマエディターの主要機能:")
        print("  ✓ WCAG準拠のコントラスト計算")
        print("  ✓ 輝度に基づく自動テキスト色選択")
        print("  ✓ 色彩理論に基づくパレット生成")
        print("  ✓ HSV色空間での色調整")
        print("  ✓ アクセシビリティガイドライン準拠")
        print("\nGUIエディターを起動するには:")
        print("  python launch_theme_editor.py")
        
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("theme_manager モジュールを確認してください。")
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
