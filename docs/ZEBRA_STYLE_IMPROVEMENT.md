# ゼブラスタイル アクセシビリティ改善

## 概要

Qt Theme Managerでゼブラスタイル（交互色）のアクセシビリティを改善しました。従来の高コントラストから、白と灰色、黒とダークグレイのような近いコントラスト比に変更することで、視覚的疲労を軽減し、長時間の作業でも快適に使用できるようにしました。

## 実装内容

### 1. テーマ設定の拡張
- `theme_manager/config/theme_settings.json`にすべてのテーマ用のzebraスタイル設定を追加
- 各テーマに`zebra.alternate`色を定義
- 背景色に近い、控えめなコントラスト比を採用

### 2. スタイルシート生成の改善
- `theme_manager/qt/stylesheet.py`でzebra_bg変数を追加
- `_generate_panel_styles`メソッドでzebra色を適切に処理
- QListWidget、QTreeWidget、QTableWidgetの`alternate-background-color`プロパティに適用

### 3. テーマ別のゼブラ色

| テーマ | 背景色 | ゼブラ交互色 | コントラスト比 |
|--------|--------|--------------|---------------|
| dark | #1e1e1e | #252a34 | 控えめ |
| light | #f8f8f8 | #fbfbfb | 控えめ |
| high_contrast | #111111 | #222222 | アクセシビリティ対応 |
| blue | #1a365d | #1e3a64 | 控えめ |
| green | #1a2e1a | #1e321e | 控えめ |
| purple | #2d1b45 | #331e4a | 控えめ |
| その他 | ... | ... | すべて控えめ |

## 使用方法

### PhotoGeoViewでの統合例

```python
# QListWidget、QTreeWidget、QTableWidgetでゼブラスタイルを有効化
list_widget.setAlternatingRowColors(True)
tree_widget.setAlternatingRowColors(True)
table_widget.setAlternatingRowColors(True)

# テーママネージャでテーマ適用
from theme_manager.qt.controller import ThemeController
controller = ThemeController()
controller.apply_theme("dark")  # または任意のテーマ
```

### テスト用デモ

テスト用のデモスクリプトも作成しました：

```bash
python test_zebra_style.py
```

このデモでは：
- 複数のテーマでゼブラスタイルを確認可能
- QListWidget、QTreeWidget、QTableWidgetのすべてでテスト
- リアルタイムでテーマ変更して比較可能

## アクセシビリティの改善点

1. **視覚的疲労の軽減**: 高コントラストから控えめなコントラストへ
2. **読みやすさの向上**: テキストと背景のコントラストを最適化
3. **長時間使用の快適性**: 目に優しい色合いの採用
4. **テーマ間の一貫性**: すべてのテーマで統一されたアプローチ

## 技術的詳細

### 色の選択基準

- **背景色ベース**: 各テーマの標準背景色を基準として選択
- **輝度差**: 約5-10%の控えめな輝度差を維持
- **色相の一致**: テーマの色相に合わせた微調整

### CSSプロパティ

```css
QListWidget, QTreeWidget, QTableWidget {
    background-color: {bg};
    border: 1px solid {border};
    border-radius: 4px;
    alternate-background-color: {zebra_bg};
}
```

### 変数定義

```python
# _generate_panel_styles内での処理
zebra_config = panel_config.get("zebra", {})
zebra_bg = zebra_config.get("alternate", bg)  # デフォルトは通常背景と同色
```

## 今後の展開

- ユーザー設定でコントラスト比の調整機能
- カスタムテーマでのzebra色のカスタマイズ
- アクセシビリティガイドラインとの適合性チェック
- 色覚異常への対応
