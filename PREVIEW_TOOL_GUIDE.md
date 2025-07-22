# プレビューツール使用ガイド (Updated for v0.2.3)

## 📖 概要

Qt Theme Managerのプレビューツールを使用して、テーマの外観を確認できます。pip install環境でも、カスタムJSONファイルを指定してプレビューが可能です。

**v0.2.3の新機能:**
- ✨ **コマンドライン引数対応**: `--config`と`--theme`オプション
- ♿ **アクセシビリティ強化**: 6%ライトネス差のゼブラスタイル
- 🔄 **フォーマット変換**: カスタムテーマ→Qt-Theme-Manager形式

## 🚀 pip install環境での使用方法

### 1. 基本的な起動

```bash
# 標準設定でプレビューを起動
theme-preview

# または
python -m theme_manager.qt.preview
```

### 2. カスタムJSONファイルと特定テーマを指定 (New in v0.2.3!)

```bash
# カスタム設定ファイルでプレビュー
theme-preview --config my_themes.json

# 特定のテーマで起動
theme-preview --theme amber

# 両方を組み合わせ
theme-preview --config sandbox/qt_theme_settings.json --theme "Orange (Improved)"
```

```bash
# 改善されたゼブラスタイルのJSONファイルを使用
theme-preview --config /path/to/improved_theme_settings.json

# または短縮形
theme-preview -c /path/to/improved_theme_settings.json
```

### 3. 起動時のテーマ指定

```bash
# 特定のテーマで起動
theme-preview --theme ocean

# カスタムJSONファイル + 特定テーマ
theme-preview --config custom_themes.json --theme cyberpunk
```

## 📋 コマンドライン引数

| 引数 | 短縮 | 説明 | 例 |
|------|------|------|-----|
| `--config` | `-c` | カスタムテーマ設定ファイル（JSON）のパス | `--config my_themes.json` |
| `--theme` | `-t` | 起動時に適用するテーマ名 | `--theme dark` |
| `--help` | `-h` | ヘルプメッセージを表示 | `--help` |

## 🎨 ゼブラスタイル改善版の使用例

### 改善されたJSONファイルでプレビュー

```bash
# PhotoGeoView用に最適化されたゼブラスタイルをプレビュー
theme-preview --config /path/to/improved_zebra_theme_settings.json

# 特定のテーマでゼブラスタイルを確認
theme-preview --config improved_themes.json --theme dark
theme-preview --config improved_themes.json --theme light
theme-preview --config improved_themes.json --theme ocean
```

### 複数テーマの比較

```bash
# 標準版でプレビュー
theme-preview --theme dark

# 別ターミナルで改善版をプレビュー
theme-preview --config improved_themes.json --theme dark
```

## 🔧 開発者向け使用例

### テーマ開発・テスト

```bash
# 開発中のテーマファイルをテスト
theme-preview --config dev/new_themes.json --theme experimental

# 特定の色調整をテスト
theme-preview --config zebra_test.json --theme test_theme
```

## 💡 PhotoGeoViewでの実際の適用

プレビューで確認したテーマを実際のPhotoGeoViewで使用：

```python
# PhotoGeoViewのコード（変更不要）
from theme_manager.qt.controller import ThemeController

# 改善されたJSONファイルを使用
controller = ThemeController(config_path="improved_themes.json")
controller.apply_theme("dark")

# ゼブラスタイルを有効化（既存コード）
list_widget.setAlternatingRowColors(True)
tree_widget.setAlternatingRowColors(True)
table_widget.setAlternatingRowColors(True)
```

## 🎯 利用シナリオ

### 1. **開発・テスト環境**
```bash
# 開発版テーマの確認
theme-preview --config dev_themes.json --theme new_design
```

### 2. **本番環境での検証**
```bash
# 本番リリース前の最終確認
theme-preview --config production_themes.json --theme default
```

### 3. **ユーザーカスタマイズ**
```bash
# ユーザー独自のテーマファイル
theme-preview --config ~/.my_themes/custom.json --theme personal
```

## 🔍 ゼブラスタイルの効果確認

プレビューウィンドウでは以下が確認できます：

- ✅ **QListWidget**: 8行のリストでゼブラスタイル表示
- ✅ **テーマ切り替え**: リアルタイムでの色変化
- ✅ **コントラスト比**: 改善された6%明度差の効果
- ✅ **アクセシビリティ**: 長時間使用での視覚的快適性

改善されたゼブラスタイル（6%明度差）により、PhotoGeoViewでの使用感が大幅に向上します！
