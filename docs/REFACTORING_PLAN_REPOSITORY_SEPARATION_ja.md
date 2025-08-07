# Qt-Theme-Manager v1.0.0 リファクタリング計画書（リポジトリ分離版）

**目標バージョン**: v1.0.0 (メジャーバージョンリリース)  
**作成日**: 2025年8月7日  
**ステータス**: 実装準備完了  
**予想期間**: 3週間（フェーズ1: 1週間、フェーズ2: 2週間、フェーズ3: 1日）  

## 🎯 プロジェクト概要

Qt-Theme-Managerを**ライブラリ**と**GUIツール**に分離し、それぞれを独立したリポジトリとして管理します。

### 主要目標
- **ライブラリ分離**: 純粋なライブラリとして`qt-theme-manager`を整理
- **GUIツール独立**: 統合GUIツールとして`qt-theme-studio`を新規作成
- **関心の分離**: ライブラリ開発とGUI開発の独立
- **配布最適化**: ライブラリはPyPI、GUIツールはGitHub Releases

## 📋 リポジトリ分離戦略

### 1. qt-theme-manager（ライブラリ専用）
**目的**: 純粋なテーマ管理ライブラリ
**配布**: PyPI
**依存関係**: PySide6→PyQt6→PyQt5自動判別

```
qt-theme-manager/
├── qt-theme_manager/           # コアライブラリ
│   ├── __init__.py
│   ├── main.py
│   ├── cli/                # CLI機能
│   ├── qt/                 # Qt統合モジュール
│   └── config/             # 設定ファイル
├── pyproject.toml          # ライブラリ設定
├── setup.py               # パッケージング設定
├── MANIFEST.in            # 配布ファイル設定
├── README.md              # ライブラリドキュメント
├── API_REFERENCE.md       # API仕様書
├── INSTALL.md             # インストールガイド
└── CHANGELOG.md           # 変更履歴
```

### 2. qt-theme-studio（GUIツール専用）
**目的**: 統合テーマエディターGUIアプリケーション
**配布**: GitHub Releases
**依存関係**: qt-theme-manager + GUI関連（Qt自動判別）

```
qt-theme-studio/
├── qt_theme_studio/        # GUIアプリケーション
│   ├── main.py            # メインエントリーポイント
│   ├── config/            # アプリケーション設定
│   ├── adapters/          # ライブラリとの橋渡し
│   ├── views/             # UIレイヤー
│   ├── controllers/       # ビジネスロジック
│   ├── services/          # アプリケーションサービス
│   ├── utilities/         # GUI専用ユーティリティ
│   └── resources/         # アセット・テンプレート
├── examples/              # 使用例
├── scripts/               # ユーティリティスクリプト
├── docs/                  # GUIツールドキュメント
├── pyproject.toml         # GUIツール設定
├── launch_theme_studio.py # 統合ランチャー
└── README.md              # GUIツールドキュメント
```

## 🏗️ 移行計画

### フェーズ1: ファイル移行準備（1週間）
**目標**: 新規リポジトリ用のファイルを準備してから削除

**主要タスク**:
1. **移行ファイルのバックアップ作成**
   - `launch_*.py` スクリプトを一時的に `temp_migration/` にコピー
   - `zebra_*.py` スクリプトを一時的に `temp_migration/` にコピー
   - `theme_editor_zebra_extension.py` を一時的に `temp_migration/` にコピー
   - `analyze_zebra_colors.py` を一時的に `temp_migration/` にコピー
   - `improve_zebra_colors.py` を一時的に `temp_migration/` にコピー
   - `examples/` ディレクトリを一時的に `temp_migration/` にコピー
   - `scripts/` ディレクトリを一時的に `temp_migration/` にコピー
   - `utils/` ディレクトリを一時的に `temp_migration/` にコピー

2. **ライブラリ最適化**
   - 行長制限79文字に統一
   - 未使用インポート削除
   - コード品質向上
   - テストカバレッジ向上

3. **ドキュメント更新**
   - ライブラリ専用README作成
   - API仕様書更新
   - インストールガイド更新

### フェーズ2: GUIツール新規作成（2週間）
**目標**: qt-theme-studioを新規リポジトリとして作成

**主要タスク**:
1. **新規リポジトリ作成**
   - GitHubでqt-theme-studioリポジトリ作成
   - 基本プロジェクト構造設定

2. **移行ファイル復元**
   - `temp_migration/` からファイルを適切な場所に移行
   - 統合GUIアプリケーションとして再構成

3. **依存関係設定**
   - qt-theme-managerを依存関係として追加
   - GUI関連依存関係の追加（Qt自動判別機能を活用）

4. **統合アプリケーション開発**
   - MVCアーキテクチャ実装
   - 統合テーマエディター
   - ゼブラパターンエディター
   - ライブプレビューシステム

### フェーズ3: クリーンアップ（1日）
**目標**: 元リポジトリから不要ファイルを削除

**主要タスク**:
1. **移行完了確認**
   - qt-theme-studioリポジトリでの動作確認
   - ファイル移行の完全性確認

2. **不要ファイル削除**
   - 元リポジトリから `temp_migration/` ディレクトリ削除
   - 元リポジトリから移行済みファイル削除
   - ライブラリ専用構造の最終確認

## 🔄 ファイル移行マップ

### qt-theme-manager（ライブラリ）に残すファイル
```
✅ theme_manager/           # コアライブラリ（全ファイル）
✅ pyproject.toml          # プロジェクト設定
✅ setup.py               # パッケージング設定
✅ MANIFEST.in            # 配布ファイル設定
✅ README.md              # ライブラリドキュメント
✅ API_REFERENCE.md       # API仕様書
✅ INSTALL.md             # インストールガイド
✅ CHANGELOG.md           # 変更履歴
✅ LICENSE                # ライセンス
```

### qt-theme-studio（GUIツール）に移行するファイル
```
🔄 launch_theme_editor.py → qt_theme_studio/views/theme_editor.py
🔄 launch_zebra_theme_editor.py → qt_theme_studio/views/zebra_editor.py
🔄 launch_gui_preview.py → qt_theme_studio/views/preview.py
🔄 theme_editor_zebra_extension.py → qt_theme_studio/views/zebra_extension.py
🔄 zebra_pattern_editor.py → qt_theme_studio/controllers/zebra_controller.py
🔄 analyze_zebra_colors.py → qt_theme_studio/utilities/color_analyzer.py
🔄 improve_zebra_colors.py → qt_theme_studio/utilities/color_improver.py
🔄 examples/ → qt_theme_studio/examples/
🔄 scripts/ → qt_theme_studio/scripts/
🔄 utils/ → qt_theme_studio/utilities/
```

### 新規作成ファイル（qt-theme-studio）
```
🆕 qt_theme_studio/main.py              # メインアプリケーション
🆕 qt_theme_studio/config/              # 設定管理
🆕 qt_theme_studio/adapters/            # ライブラリアダプター
🆕 qt_theme_studio/controllers/         # ビジネスロジック
🆕 qt_theme_studio/services/            # アプリケーションサービス
🆕 qt_theme_studio/resources/           # リソースファイル
🆕 launch_theme_studio.py               # 統合ランチャー
🆕 pyproject.toml                       # GUIツール設定
🆕 README.md                            # GUIツールドキュメント
```

## 🎨 GUIツール機能設計

### 統合テーマエディター
- 従来のテーマプロパティ編集
- リアルタイム色調整
- コンポーネント固有スタイリング
- アクセシビリティ検証

### ゼブラパターンエディター
- WCAG準拠コントラスト調整
- 科学的色計算
- リアルタイムプレビュー
- アクセシビリティレベルプリセット

### ライブプレビューシステム
- マルチウィジェットプレビュー
- リアルタイム更新
- プレビュー画像エクスポート
- レスポンシブレイアウトテスト

### スマートテーマ管理
- テーマギャラリーブラウザー
- フォーマット中立インポート/エクスポート
- ラウンドトリップ変換対応
- バージョン管理統合
- テーマテンプレートとプリセット

## 📊 実装フェーズ詳細

### フェーズ1: ライブラリ整理（1週間）

#### 週1-2日: 移行ファイル準備
- 移行対象ファイルの特定とバックアップ作成
- `temp_migration/` ディレクトリへの安全なコピー
- ライブラリ専用ディレクトリ構造の確認
- 依存関係の最適化

#### 週3-4日: コード品質向上
- black/isort/autoflakeによる自動整形
- 行長制限79文字への統一
- 未使用インポートの削除
- テストカバレッジの向上

#### 週5-7日: ドキュメント更新
- ライブラリ専用README作成
- API仕様書の更新
- インストールガイドの更新
- リリース準備

### フェーズ2: GUIツール開発（2週間）

#### 週1-3日: 基盤セットアップ
- 新規リポジトリ作成
- プロジェクト構造設定
- 基本MVCアーキテクチャ実装
- 依存関係設定（Qt自動判別機能を活用）

#### 週4-7日: コア機能実装
- 統合テーマエディター
- ゼブラパターンエディター
- ライブプレビューシステム
- `temp_migration/` からのファイル復元と統合

#### 週8-10日: 高度機能実装
- フォーマット変換システム
- アクセシビリティツール
- バッチ処理機能
- 統合ロギング

#### 週11-14日: テストと調整
- 統合テストスイート
- パフォーマンス最適化
- ドキュメント作成
- リリース準備

### フェーズ3: クリーンアップ（1日）

#### 最終日: 移行完了とクリーンアップ
- qt-theme-studioリポジトリでの動作確認
- ファイル移行の完全性確認
- 元リポジトリから `temp_migration/` ディレクトリ削除
- 元リポジトリから移行済みファイル削除
- ライブラリ専用構造の最終確認

## 🔧 技術仕様

### qt-theme-manager（ライブラリ）
```toml
[project]
name = "qt-theme-manager"
version = "1.0.0"
description = "A comprehensive theme management library for PyQt5/PyQt6/PySide6 applications"
dependencies = [
    # 自動判別: PySide6 → PyQt6 → PyQt5 の順で利用可能なものを自動選択
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "pytest-qt>=4.0",
    "black",
    "isort",
    "flake8",
]
```

### qt-theme-studio（GUIツール）
```toml
[project]
name = "qt-theme-studio"
version = "1.0.0"
description = "Integrated theme editor GUI application for Qt applications"
dependencies = [
    "qt-theme-manager>=1.0.0",
    "pillow>=8.0.0",
    "colorama>=0.4.0"
    # Qt依存関係はqt-theme-managerの自動判別機能を使用
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "pytest-qt>=4.0",
    "black",
    "isort",
    "flake8",
]
```

## 🧪 テスト戦略

### qt-theme-manager（ライブラリ）
- **単体テスト**: 95%カバレッジ目標
- **統合テスト**: API互換性テスト
- **パフォーマンステスト**: メモリ使用量最適化
- **クロスプラットフォームテスト**: 全OS対応確認

### qt-theme-studio（GUIツール）
- **単体テスト**: 90%カバレッジ目標
- **統合テスト**: ライブラリ連携テスト
- **UIテスト**: ユーザーインターフェーステスト
- **エンドツーエンドテスト**: 完全ワークフローテスト

## 📈 成功指標

### 定量的目標
- **ライブラリ**: コードサイズ30%削減、依存関係最小化
- **GUIツール**: 機能統合による開発効率50%向上
- **テストカバレッジ**: ライブラリ95%、GUIツール90%
- **パフォーマンス**: 現在の速度を維持または改善

### 定性的目標
- **関心の分離**: ライブラリとGUIツールの明確な責任分離
- **保守性**: 独立した開発・リリースサイクル
- **ユーザーエクスペリエンス**: 統合GUIツールによる改善
- **開発者エクスペリエンス**: 貢献しやすい構造

## 🚀 リリース計画

### qt-theme-manager v1.0.0
- **リリース日**: フェーズ1完了後
- **配布**: PyPI
- **変更**: 破壊的変更なし（後方互換性維持）

### qt-theme-studio v1.0.0
- **リリース日**: フェーズ2完了後
- **配布**: GitHub Releases
- **変更**: 新規アプリケーション

## 🔧 開発ガイドライン

### コード標準
- PythonコードスタイルにPEP 8を使用
- 行長制限: ライブラリ79文字、GUIツール88文字
- 全体を通してタイプヒントを使用
- docstringカバレッジを維持

### Gitワークフロー
- 各フェーズ用の機能ブランチ
- プルリクエストレビューが必須
- マージ前の自動テスト
- セマンティックコミットメッセージ

### テスト要件
- すべての新コードに単体テスト
- ワークフロー用統合テスト
- パフォーマンス回帰テスト
- クロスプラットフォーム検証

## 🧠 AI振る舞いルール（AI Behavior Rules）

- 応答はすべて日本語で行う、ドキュメントは英語で記述するが、日本語版も必ず作成する。
- print文は禁止。必ず logger を使用すること。
- メインのエントリーポイント以外のスクリプトは root に配置しない。適切なフォルダに整理すること。
- `theme_manager/` パッケージは一切変更しない。既存ライブラリの保護を最優先とする。
- GUIアプリケーションは `qt_theme_studio/` 以下に構築し、MVCアーキテクチャを遵守すること。
- 統合ランチャーは `launch_theme_studio.py` のみとし、旧ランチャーは削除対象とする。

---

**次のステップ**: フェーズ1（ライブラリ整理）から実装開始

**開発体制**: 単体開発（Amazon Kiro支援）

**バージョン**: 1.0.0 - リファクタリング計画（リポジトリ分離版） 