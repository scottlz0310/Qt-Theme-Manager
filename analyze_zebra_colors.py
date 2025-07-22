#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ゼブラ色の色差分析ツール
現在のテーマ設定でのコントラスト比と色差を計算します
"""

import json
import colorsys
from pathlib import Path

def hex_to_rgb(hex_color):
    """16進数カラーコードをRGBに変換"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsl(r, g, b):
    """RGBをHSLに変換"""
    r, g, b = r/255.0, g/255.0, b/255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h*360, s*100, l*100

def calculate_luminance(r, g, b):
    """相対輝度を計算（WCAG基準）"""
    def to_linear(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else pow((c + 0.055) / 1.055, 2.4)
    
    r_lin = to_linear(r)
    g_lin = to_linear(g)
    b_lin = to_linear(b)
    
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

def calculate_contrast_ratio(color1, color2):
    """2つの色のコントラスト比を計算"""
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    lum1 = calculate_luminance(*rgb1)
    lum2 = calculate_luminance(*rgb2)
    
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    
    return (lighter + 0.05) / (darker + 0.05)

def calculate_color_difference(color1, color2):
    """色差を複数の方法で計算"""
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    # Euclidean距離（RGB空間）
    euclidean = ((rgb1[0] - rgb2[0])**2 + (rgb1[1] - rgb2[1])**2 + (rgb1[2] - rgb2[2])**2)**0.5
    
    # HSL空間での明度差
    h1, s1, l1 = rgb_to_hsl(*rgb1)
    h2, s2, l2 = rgb_to_hsl(*rgb2)
    lightness_diff = abs(l1 - l2)
    
    return {
        'euclidean': euclidean,
        'lightness_diff': lightness_diff,
        'rgb1': rgb1,
        'rgb2': rgb2,
        'hsl1': (h1, s1, l1),
        'hsl2': (h2, s2, l2)
    }

def analyze_zebra_colors():
    """ゼブラ色の分析を実行"""
    # テーマ設定を読み込み
    config_path = Path("theme_manager/config/theme_settings.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("🎨 ゼブラ色差分析レポート")
    print("=" * 60)
    
    results = []
    
    for theme_name, theme_config in config['available_themes'].items():
        panel_config = theme_config.get('panel', {})
        bg_color = panel_config.get('background', '#ffffff')
        zebra_config = panel_config.get('zebra', {})
        zebra_color = zebra_config.get('alternate', bg_color)
        
        if bg_color == zebra_color:
            print(f"\n📋 {theme_name.upper()} ({theme_config.get('display_name', theme_name)})")
            print(f"   ⚠️  ゼブラ色が設定されていません（背景色と同じ）")
            continue
        
        # 色差計算
        contrast_ratio = calculate_contrast_ratio(bg_color, zebra_color)
        color_diff = calculate_color_difference(bg_color, zebra_color)
        
        # 結果を保存
        result = {
            'theme': theme_name,
            'display_name': theme_config.get('display_name', theme_name),
            'bg_color': bg_color,
            'zebra_color': zebra_color,
            'contrast_ratio': contrast_ratio,
            'color_diff': color_diff
        }
        results.append(result)
        
        # 詳細表示
        print(f"\n📋 {theme_name.upper()} ({theme_config.get('display_name', theme_name)})")
        print(f"   背景色: {bg_color} RGB{color_diff['rgb1']} HSL({color_diff['hsl1'][0]:.0f}°, {color_diff['hsl1'][1]:.1f}%, {color_diff['hsl1'][2]:.1f}%)")
        print(f"   ゼブラ色: {zebra_color} RGB{color_diff['rgb2']} HSL({color_diff['hsl2'][0]:.0f}°, {color_diff['hsl2'][1]:.1f}%, {color_diff['hsl2'][2]:.1f}%)")
        print(f"   📊 コントラスト比: {contrast_ratio:.3f}:1")
        print(f"   📏 RGB色差 (Euclidean): {color_diff['euclidean']:.1f}")
        print(f"   💡 明度差: {color_diff['lightness_diff']:.1f}%")
        
        # アクセシビリティ評価
        if contrast_ratio < 1.2:
            print(f"   🟢 非常に控えめ（推奨: 視覚疲労軽減）")
        elif contrast_ratio < 2.0:
            print(f"   🟡 控えめ（バランス良好）")
        elif contrast_ratio < 3.0:
            print(f"   🟠 やや目立つ（従来的）")
        else:
            print(f"   🔴 高コントラスト（アクセシビリティ特化）")
    
    # 統計サマリー
    if results:
        print(f"\n📈 統計サマリー")
        print("=" * 30)
        contrast_ratios = [r['contrast_ratio'] for r in results]
        lightness_diffs = [r['color_diff']['lightness_diff'] for r in results]
        
        print(f"コントラスト比:")
        print(f"  最小: {min(contrast_ratios):.3f}:1")
        print(f"  最大: {max(contrast_ratios):.3f}:1")
        print(f"  平均: {sum(contrast_ratios)/len(contrast_ratios):.3f}:1")
        
        print(f"明度差:")
        print(f"  最小: {min(lightness_diffs):.1f}%")
        print(f"  最大: {max(lightness_diffs):.1f}%")
        print(f"  平均: {sum(lightness_diffs)/len(lightness_diffs):.1f}%")
        
        # 推奨事項
        avg_contrast = sum(contrast_ratios)/len(contrast_ratios)
        print(f"\n💡 推奨事項:")
        if avg_contrast < 1.3:
            print("  ✅ 現在の設定は非常に控えめで、長時間作業に最適です")
            print("  💭 より判別しやすくしたい場合は、明度差を2-4%増やすことを検討")
        elif avg_contrast < 2.0:
            print("  ✅ 現在の設定はバランスが良好です")
        else:
            print("  ⚠️  コントラストがやや高めです。アクセシビリティ目的でない限り、")
            print("     もう少し控えめにすることで視覚疲労を軽減できます")

if __name__ == "__main__":
    analyze_zebra_colors()
