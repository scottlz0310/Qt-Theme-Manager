#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ゼブラ色の改善提案ツール
現在の控えめすぎる設定をより実用的に調整します
"""

import json
import colorsys
from pathlib import Path

def hex_to_rgb(hex_color):
    """16進数カラーコードをRGBに変換"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    """RGBを16進数カラーコードに変換"""
    return f"#{r:02x}{g:02x}{b:02x}"

def adjust_brightness(hex_color, lightness_change_percent):
    """明度を指定した%だけ調整"""
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    
    # 明度を調整（0-1の範囲で）
    new_l = max(0, min(1, l + lightness_change_percent/100))
    
    # HSLからRGBに戻す
    new_r, new_g, new_b = colorsys.hls_to_rgb(h, new_l, s)
    
    # 0-255の範囲に戻す
    new_r = int(round(new_r * 255))
    new_g = int(round(new_g * 255))
    new_b = int(round(new_b * 255))
    
    return rgb_to_hex(new_r, new_g, new_b)

def generate_improved_zebra_colors():
    """改善されたゼブラ色の提案を生成"""
    # テーマ設定を読み込み
    config_path = Path("theme_manager/config/theme_settings.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("🎨 ゼブラ色改善提案")
    print("=" * 50)
    print("目標: 明度差 3-5%（現在平均1.9%）")
    print("方針: アクセシビリティを保ちつつ、適度な判別性を確保")
    print()
    
    improvements = {}
    
    for theme_name, theme_config in config['available_themes'].items():
        panel_config = theme_config.get('panel', {})
        bg_color = panel_config.get('background', '#ffffff')
        current_zebra = panel_config.get('zebra', {}).get('alternate', bg_color)
        
        # 背景色のHSL値を取得
        r, g, b = hex_to_rgb(bg_color)
        h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
        
        # 明度に基づいて調整方向を決定
        if l > 0.5:  # 明るいテーマ
            # 暗くする（明度を下げる）
            target_change = -4.0  # 4%暗く
        else:  # 暗いテーマ
            # 明るくする（明度を上げる）
            target_change = 4.0   # 4%明るく
        
        # 新しいゼブラ色を生成
        new_zebra = adjust_brightness(bg_color, target_change)
        
        # 結果を保存
        improvements[theme_name] = {
            'current': current_zebra,
            'proposed': new_zebra,
            'background': bg_color,
            'change': target_change
        }
        
        print(f"📋 {theme_name.upper()} ({theme_config.get('display_name', theme_name)})")
        print(f"   背景色: {bg_color}")
        print(f"   現在: {current_zebra}")
        print(f"   提案: {new_zebra} (明度{target_change:+.1f}%)")
        print()
    
    return improvements

def generate_update_commands(improvements):
    """設定更新用のコマンドを生成"""
    print("\n🔧 設定更新用JSONスニペット")
    print("=" * 40)
    
    for theme_name, data in improvements.items():
        print(f'      "zebra": {{')
        print(f'        "alternate": "{data["proposed"]}"')
        print(f'      }}')
        print(f"   # {theme_name}: {data['background']} -> {data['proposed']}")
        print()

if __name__ == "__main__":
    improvements = generate_improved_zebra_colors()
    generate_update_commands(improvements)
