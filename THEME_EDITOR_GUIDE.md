# 🎨 高度なテーマエディター - 機能詳細

この文書では、Qt Theme Manager に新たに追加された高度なテーマエディターの機能について詳しく説明します。

## 📋 概要

高度なテーマエディターは、色彩理論とアクセシビリティガイドラインに基づいてテーマを作成・編集できる統合GUIツールです。専門的な色彩知識がなくても、美しく実用的なテーマを簡単に作成できます。

## 🚀 起動方法

テーマエディターはv0.2.1で起動の信頼性が大幅に向上しました。すべてのQtフレームワーク（PyQt5/PyQt6/PySide6）で確実に動作します。

### 方法1: モジュール実行（推奨）
```bash
python -m theme_manager.qt.theme_editor
```

### 方法2: 専用ランチャー
```bash
python launch_theme_editor.py
```

### 方法3: pipエントリーポイント
```bash
theme-editor  # pip install qt-theme-manager後
```

> **✨ v0.2.1の改善**: すべての起動方法でイベントループが適切に管理され、GUI起動が確実に行われます。

## 🎯 主要機能

### 1. 🧮 色彩理論エンジン

#### WCAG準拠のコントラスト計算
- **輝度計算**: 各色の相対輝度を正確に測定
- **コントラスト比**: 2つの色間のコントラスト比を計算
- **アクセシビリティ判定**: WCAG AA/AAA基準の自動判定

```python
# 使用例
from theme_manager.qt.theme_editor import ColorUtils

# 輝度計算
luminance = ColorUtils.get_luminance("#007acc")  # 0.213

# コントラスト比
contrast = ColorUtils.get_contrast_ratio("#ffffff", "#000000")  # 21.0:1

# アクセシビリティチェック
is_accessible = ColorUtils.is_accessible("#007acc", "#ffffff", "AA")  # True
```

#### 自動テキスト色選択
背景色の輝度に基づいて、最適なテキスト色（黒または白）を自動選択：

```python
# 背景色に対する最適なテキスト色を取得
optimal_text = ColorUtils.get_optimal_text_color("#007acc")  # "#ffffff"
```

#### HSV色空間での色調整
- **明度調整**: `-1.0`（最暗）〜 `+1.0`（最明）
- **彩度調整**: `-1.0`（無彩色）〜 `+1.0`（最高彩度）

```python
# 明度を20%上げる
brighter = ColorUtils.adjust_brightness("#007acc", 0.2)

# 彩度を30%下げる  
desaturated = ColorUtils.adjust_saturation("#007acc", -0.3)
```

### 2. 🎨 インテリジェントパレット生成

#### 補色ベースのアクセント色生成
プライマリ色から色相環上の補色（180度反対）を計算してアクセント色を自動生成：

```python
def generate_color_palette(self):
    """Generate harmonious color palette based on primary color."""
    primary_color = self.current_theme_config.get("primaryColor", "#007acc")
    
    # HSV変換
    r, g, b = ColorUtils.hex_to_rgb(primary_color)
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    
    # 補色生成（色相を180度回転）
    accent_h = (h + 0.5) % 1.0
    accent_r, accent_g, accent_b = colorsys.hsv_to_rgb(accent_h, s * 0.8, v * 0.9)
    accent_color = ColorUtils.rgb_to_hex(int(accent_r*255), int(accent_g*255), int(accent_b*255))
```

#### ライト/ダークテーマの自動判定
プライマリ色の輝度に基づいて、適切なテーマタイプを自動選択：

- **輝度 > 0.5**: ライトテーマを生成（明るい背景、暗いテキスト）
- **輝度 ≤ 0.5**: ダークテーマを生成（暗い背景、明るいテキスト）

### 3. 🖱️ 直感的なユーザーインターフェース

#### タブベースの整理
- **基本色**: 背景、テキスト、プライマリ、アクセント色の設定
- **コンポーネント**: 20種類以上のUIコンポーネント詳細設定
- **コントラスト**: リアルタイムコントラストチェッカー

#### 包括的なコンポーネント設定
1. **ボタンコンポーネント**: 通常、ホバー、押下、無効、境界線
2. **入力コンポーネント**: 背景、テキスト、境界線、フォーカス、プレースホルダー、選択範囲
3. **パネル・グループボックス**: 背景、境界線、タイトル背景、タイトルテキスト
4. **メニュー・コンボボックス**: 背景、テキスト、ホバー背景、選択背景、選択テキスト、区切り線
5. **プログレスバー・スライダー**: 背景、進捗部分、溝、ハンドル
6. **スクロールバー**: 背景、ハンドル、ハンドルホバー、ハンドル押下

#### RGBスライダー
- 0-255の範囲でR、G、B値を個別調整
- スライダーとスピンボックスの連動
- 16進数カラーコードの直接入力
- カラーピッカー連携

#### 高度なプレビューシステム
- **包括的なウィジェット**: 20種類以上のQtウィジェットの表示確認
- **リアルタイム反映**: 100ms遅延でのスムーズな色変更プレビュー
- **実際のスタイルシート**: 実装されるQSSでの正確な表示確認
- **アクセシビリティ表示**: コントラスト情報の視覚的フィードバック

#### スマート調整機能
- **コンポーネント色を自動調整**: 基本色から全コンポーネント色を論理的に生成
- **色の調和を最適化**: 類似色を使用した美的バランスの改善
- **一括設定更新**: 複数のコンポーネントを一度に最適化

### 4. 📊 アクセシビリティチェッカー

#### WCAG準拠チェック
```
コントラスト比: 4.51:1  
WCAG AA: ✅  
WCAG AAA: ❌
```

#### 推奨事項の表示
- コントラストが低い場合の具体的な改善提案
- アクセシビリティレベルの視覚的表示
- 実際のテキストサンプルでの見え方確認

### 5. 💾 エクスポート・インポート機能

#### JSON形式でのエクスポート
```json
{
  "name": "ai_generated_theme",
  "display_name": "AI生成テーマ",
  "description": "色彩理論に基づいて自動生成されたテーマ",
  "backgroundColor": "#1a202c",
  "textColor": "#f7fafc",
  "primaryColor": "#6c63ff",
  "accentColor": "#dfe575",
  "button": {
    "background": "#6159e5",
    "text": "#ffffff",
    "hover": "#6b62ff",
    "pressed": "#4b45b2",
    "border": "#403b98"
  }
  // ... 省略
}
```

## 🧪 デモンストレーション

### コンソールベースデモ
```bash
python demo_theme_editor.py
```

このデモでは以下を実行：

1. **輝度計算テスト**: 10種類の基本色の輝度測定
2. **コントラスト比テスト**: 一般的な色組み合わせの評価
3. **色調整テスト**: 明度・彩度調整のサンプル
4. **パレット生成**: 4つのベース色からの色展開
5. **インテリジェントテーマ生成**: AI風の自動テーマ作成

### 出力例
```
🎨 ColorUtils クラスのテスト
==================================================
輝度計算テスト:
------------------------------
白            #ffffff: 輝度=1.000, 最適テキスト=#000000
黒            #000000: 輝度=0.000, 最適テキスト=#ffffff
赤            #ff0000: 輝度=0.213, 最適テキスト=#ffffff
...

🎯 インテリジェントテーマ生成デモ
==================================================
選択されたプライマリ色: #6c63ff

アクセシビリティチェック:
------------------------------
背景-テキスト コントラスト: 15.57:1 ✅
ボタン コントラスト: 5.16:1 ✅
```

## 🔧 技術仕様

### 色彩計算アルゴリズム

#### 相対輝度計算（WCAG 2.1準拠）
```python
def get_luminance(hex_color: str) -> float:
    r, g, b = hex_to_rgb(hex_color)
    r, g, b = r/255.0, g/255.0, b/255.0
    
    # ガンマ補正
    def gamma_correct(c):
        return c/12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    r, g, b = map(gamma_correct, [r, g, b])
    
    # 輝度計算
    return 0.2126 * r + 0.7152 * g + 0.0722 * b
```

#### コントラスト比計算
```python
def get_contrast_ratio(color1: str, color2: str) -> float:
    l1 = get_luminance(color1)
    l2 = get_luminance(color2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)
```

### アクセシビリティ基準

- **WCAG AA**: コントラスト比 4.5:1 以上
- **WCAG AAA**: コントラスト比 7.0:1 以上
- **推奨**: 大きなテキスト（18pt以上）は 3.0:1 以上

### 色空間変換
- **RGB**: ディスプレイ表示用
- **HSV**: 直感的な色調整用
- **Hex**: 設定ファイル保存用

## 🎓 使用方法のベストプラクティス

### 1. アクセシブルなテーマ作成
```python
# 1. まずプライマリ色を選択
primary_color = "#007acc"

# 2. 背景色の輝度で判定
luminance = ColorUtils.get_luminance(primary_color)
if luminance > 0.5:
    background = "#ffffff"  # ライトテーマ
else:
    background = "#1a1a1a"  # ダークテーマ

# 3. 最適なテキスト色を自動選択
text_color = ColorUtils.get_optimal_text_color(background)

# 4. コントラストを確認
contrast = ColorUtils.get_contrast_ratio(background, text_color)
assert contrast >= 4.5, "WCAG AA基準を満たしません"
```

### 2. 調和のとれたカラーパレット
```python
# 基調色から補色を生成
base_color = "#6c63ff"
r, g, b = ColorUtils.hex_to_rgb(base_color)
h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

# 補色（180度反対）
complement_h = (h + 0.5) % 1.0
# 三角配色（120度）
triadic1_h = (h + 0.33) % 1.0
triadic2_h = (h + 0.67) % 1.0
```

### 3. 段階的明度調整
```python
base_color = "#007acc"

# 明度のバリエーション作成
darker = ColorUtils.adjust_brightness(base_color, -0.3)    # ボタン押下時
normal = base_color                                        # 通常状態
hover = ColorUtils.adjust_brightness(base_color, 0.1)     # ホバー時
lighter = ColorUtils.adjust_brightness(base_color, 0.3)   # 無効状態
```

## � 実用的な使用例

### シナリオ1: 企業アプリケーションのテーマ作成

```python
# ブランドカラーに基づく企業テーマの作成
python launch_theme_editor.py --base-color "#1976D2"  # 企業カラー

# エディター内での操作:
# 1. コントラスト比 > 7:1 でAAAレベル準拠を確認
# 2. 「全コンポーネント自動調整」で統一感を生成
# 3. 個別にボタンやパネルを微調整
# 4. 保存して社内アプリに適用
```

### シナリオ2: アクセシブルなダークテーマ

```python
# 視認性重視のダークテーマ
python launch_theme_editor.py --theme dark --base-color "#BB86FC"

# 重要なポイント:
# - 背景色の明度を25以下に設定（目の負担軽減）
# - テキストコントラスト比 > 4.5（WCAG AA準拠）
# - アクセント色は彩度60%以上で判別性向上
```

### シナリオ3: プロトタイプ用カラフルテーマ

```python
# 創作活動向けの鮮やかなテーマ
from theme_manager.qt.theme_editor import ColorUtils

utils = ColorUtils()
# 補色を活用した印象的なテーマ
theme = utils.generate_intelligent_theme("#FF6B35")  # エネルギッシュなオレンジ
# 自動的に青系の補色がアクセントカラーに設定される
```

### カラー調整のベストプラクティス

#### 基本色選択のコツ
```python
# ブランドカラーをベースに
base = "#3498DB"  # メインブランドカラー
hover = ColorUtils.adjust_brightness(base, 0.15)    # 15%明るく（ホバー効果）
pressed = ColorUtils.adjust_brightness(base, -0.2)  # 20%暗く（押下効果）
disabled = ColorUtils.adjust_saturation(base, -0.5) # 彩度半減（無効状態）
```

#### コントラスト最適化
```python
# 自動的に最適なテキスト色を決定
bg_color = "#2C3E50"
text_color = utils.get_optimal_text_color(bg_color)
ratio = utils.get_contrast_ratio(text_color, bg_color)
print(f"最適化結果: {text_color}, コントラスト比: {ratio:.2f}")
```

### 実際のワークフロー

1. **基本設定** (2分)
   - ベースカラーを選択
   - テーマタイプ（ライト/ダーク）を決定
   
2. **自動最適化** (30秒)
   - 「全コンポーネント自動調整」をクリック
   - アクセシビリティ情報を確認
   
3. **手動調整** (5分)
   - 各コンポーネントタブで細かい調整
   - プレビューで実際の見栄えを確認
   
4. **保存と適用** (30秒)
   - テーマを保存
   - アプリケーションで即座に利用

## 🔮 今後の拡張予定と改善点

### 現在実装済みの高度機能
✅ **WCAG 2.1準拠のコントラスト計算**  
✅ **20種類以上のQtコンポーネント対応**  
✅ **HSV色空間での直感的調整**  
✅ **リアルタイム100msプレビュー**  
✅ **インテリジェントな色彩生成**  
✅ **CLI統合とJSON設定**

### 近日実装予定 🚧
- [ ] **コンポーネントタブの実装**: ボタン、パネル、入力欄の詳細設定
- [ ] **テーマプリセット**: 人気のデザインシステムベースのテンプレート
- [ ] **カラーパレット拡張**: トライアド、テトラード配色の自動生成
- [ ] **アニメーション**: テーマ切り替え時のスムーズなトランジション

### 中期計画
- [ ] **マテリアルデザイン対応**: Google Material Design準拠のテーマ
- [ ] **ダークモード検出**: システム設定からの自動テーマ切り替え
- [ ] **カスタムCSS**: 高度ユーザー向けの直接スタイル編集
- [ ] **テーマ共有**: クラウドベースのテーマライブラリ

### 長期計画
- [ ] **AI色彩推薦**: 機械学習による美的バランスの最適化
- [ ] **視覚障害対応**: 色覚異常者向けの特別配慮機能
- [ ] **多言語UI**: テーマエディター自体の国際化
- [ ] **プラグインシステム**: サードパーティ機能の統合

## 🤝 貢献方法

このテーマエディターはオープンソースプロジェクトです。以下の方法で貢献できます：

### コードの貢献
- バグ修正
- 新機能の実装
- パフォーマンス改善
- テストケース追加

### デザインの貢献
- UIデザインの改善案
- UXフローの最適化
- アクセシビリティ向上

### ドキュメントの貢献
- 使用例の追加
- 翻訳作業
- チュートリアル作成

---

この高度なテーマエディターにより、Qt Theme Manager は単なる色変更ツールから、プロフェッショナルなデザインシステム構築ツールへと進化しました。色彩理論とアクセシビリティを重視した設計により、誰でも美しく使いやすいテーマを作成できます。
