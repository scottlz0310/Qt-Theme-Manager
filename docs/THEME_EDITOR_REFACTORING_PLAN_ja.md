# テーマエディターリファクタリング計画書 v1.0.0

**目標バージョン**: v1.0.0 (メジャーバージョンリリース)
**作成日**: 2025年7月24日
**ステータス**: 計画フェーズ
**予想期間**: 2-3週間

## 🎯 プロジェクト概要

この文書では、Qt-Theme-Managerのテーマエディターコンポーネントの包括的なリファクタリング計画を概説します。現在の断片化されたテーマ管理ツールを、v1.0.0メジャーリリースにふさわしい統合されたプロフェッショナルグレードのGUIアプリケーションに変革することが目標です。

## 📋 現状分析

### 既存コンポーネント
- `launch_theme_editor.py` - メインテーマエディター（大きなモノリシックファイル）
- `launch_zebra_theme_editor.py` - ゼブラパターンエディター
- `launch_gui_preview.py` - テーマプレビューアプリケーション
- `theme_editor_zebra_extension.py` - ゼブラ統合拡張
- `zebra_pattern_editor.py` - コアゼブラ生成ロジック
- `qt_theme_manager/qt/preview.py` - プレビューモジュール
- `qt_theme_manager/qt/theme_editor.py` - コアテーマエディターモジュール

### 現在の課題
1. **コードの重複**: 重複する機能を持つ複数の起動スクリプト
2. **断片化されたUX**: 編集、プレビュー、ゼブラパターン用の別々のアプリケーション
3. **モノリシックアーキテクチャ**: 責任が混在した大きなファイル
4. **限定的な統合**: コンポーネント間の貧弱な通信
5. **保守負担**: テスト、拡張、デバッグが困難

## 🏗️ 目標アーキテクチャ

### 🔒 **重要な方針: 既存ライブラリの保護**

**`qt_theme_manager/`パッケージは変更しません**
- ✅ **安定性保証**: 実績のあるコアライブラリを保護
- ✅ **リスク削減**: テスト済みAPIへの影響を回避
- ✅ **互換性維持**: 既存ユーザーへの破壊的変更なし
- ✅ **開発効率**: GUIレイヤーのみに集中

### アーキテクチャ分離

```
# 既存ライブラリ（変更なし）
qt_theme_manager/                      # ✅ 現状維持 - 触らない
├── __init__.py                    # 安定版API
├── main.py                        # コアライブラリ
├── cli/                          # CLI機能
├── qt/                           # Qt統合モジュール
└── ...                           # 全ての既存機能

# 新しいGUIアプリケーション（新規作成）
qt_theme_studio/                    # 🆕 新しい統合アプリケーションパッケージ
├── __init__.py
├── main.py                         # メインアプリケーションエントリーポイント
├── config/
│   ├── __init__.py
│   ├── app_config.py              # アプリケーション設定
│   ├── editor_config.py           # エディター固有設定
│   └── ui_config.py               # UIレイアウトとスタイリング
├── adapters/                       # 🔗 既存ライブラリとの橋渡し
│   ├── __init__.py
│   ├── theme_adapter.py           # qt_theme_manager.qt との連携
│   ├── preview_adapter.py         # 既存プレビュー機能の活用
│   ├── api_adapter.py             # 既存APIラッパー
│   └── format_adapter.py          # 🆕 フォーマット変換システム
├── views/
│   ├── __init__.py
│   ├── main_window.py             # メインアプリケーションウィンドウ
│   ├── theme_editor_view.py       # テーマ編集インターフェース
│   ├── zebra_editor_view.py       # ゼブラパターンエディター
│   ├── preview_view.py            # ライブプレビューパネル
│   ├── theme_browser_view.py      # テーマギャラリーと管理
│   └── components/
│       ├── __init__.py
│       ├── color_picker.py        # 高度なカラーピッカーウィジェット
│       ├── contrast_slider.py     # WCAG準拠コントラスト制御
│       ├── theme_tree.py          # テーマ階層ブラウザー
│       ├── preview_widget.py      # リアルタイムプレビューコンポーネント
│       ├── export_dialog.py       # 🆕 スマートエクスポート/インポートダイアログ
│       └── settings_panel.py      # アプリケーション設定
├── controllers/
│   ├── __init__.py
│   ├── app_controller.py          # メインアプリケーションロジック
│   ├── theme_controller.py        # テーマ編集操作（theme_manager経由）
│   ├── zebra_controller.py        # ゼブラパターン管理
│   ├── preview_controller.py      # プレビュー同期
│   └── export_controller.py       # 🆕 フォーマット中立インポート/エクスポート操作
├── services/
│   ├── __init__.py
│   ├── gui_service.py             # GUI固有サービス
│   ├── validation_service.py      # GUI用検証（theme_manager活用）
│   ├── backup_service.py          # 自動保存とバックアップ
│   └── plugin_service.py          # 将来のプラグインシステム
├── utilities/
│   ├── __init__.py
│   ├── gui_utils.py               # GUI専用ユーティリティ
│   ├── accessibility_utils.py     # WCAG準拠チェック
│   ├── logger_utils.py            # ロギングシステム
│   └── qt_framework_manager.py    # Qtフレームワーク切り替えシステム
└── resources/
    ├── __init__.py
    ├── icons/                     # アプリケーションアイコン
    ├── themes/                    # 組み込みテーマテンプレート
    └── styles/                    # アプリケーションスタイリング
```

### 🔗 **既存ライブラリとの連携方針**

1. **アダプターパターンの活用**
   - `qt_theme_studio.adapters`で既存APIをラップ
   - GUIレイヤーと既存ライブラリの疎結合

2. **既存機能の再利用**
   - `theme_manager.qt.loader` - テーマ読み込み
   - `theme_manager.qt.stylesheet` - スタイルシート生成
   - `theme_manager.qt.controller` - テーマ操作
   - `theme_manager.main` - コア機能

3. **API安定性の保証**
   - 既存のパブリックAPIは一切変更しない
   - 新しい機能は`qt_theme_studio`内で完結

### 新しい統合ランチャー
```
# 旧個別ランチャー（削除対象）
launch_theme_editor.py              # → 削除
launch_zebra_theme_editor.py        # → 削除
launch_gui_preview.py               # → 削除

# 新しい統合ランチャー
launch_theme_studio.py              # すべての機能への単一エントリーポイント
```

## 🎨 機能統合計画

### コア機能
1. **統合テーマエディター**
   - 従来のテーマプロパティ編集
   - リアルタイム色調整
   - コンポーネント固有スタイリング
   - アクセシビリティ検証

2. **統合ゼブラパターンエディター**
   - WCAG準拠コントラスト調整
   - 科学的色計算
   - リアルタイムプレビュー
   - アクセシビリティレベルプリセット

3. **ライブプレビューシステム**
   - マルチウィジェットプレビュー
   - リアルタイム更新
   - 画像としてプレビューエクスポート
   - レスポンシブレイアウトテスト

4. **スマートテーマ管理**
   - テーマギャラリーブラウザー
   - **フォーマット中立インポート/エクスポート機能**
   - **ラウンドトリップ変換対応**（元フォーマット保持）
   - バージョン管理統合
   - テーマテンプレートとプリセット

5. **プロフェッショナルツール**
   - カラーパレットジェネレーター
   - アクセシビリティチェッカー
   - テーマ検証
   - バッチ処理

6. **開発者支援ツール**
   - 統合ロギングシステム
   - Qtフレームワーク切り替えツール
   - デバッグ情報エクスポート
   - パフォーマンス分析

## � フォーマット変換システム詳細仕様

### 6.1 概要
- **目的**: 複数のテーマフォーマット間での双方向変換
- **設計原則**: メタデータ保持、可逆変換、フォーマット中立
- **対応フォーマット**: QSS、JSON、VS Code、Sublime Text、その他

### 6.2 技術アーキテクチャ

```
format_system/
├── core/
│   ├── base_converter.py      # 変換基底クラス
│   ├── metadata_handler.py    # メタデータ管理
│   └── conversion_registry.py # フォーマット登録システム
├── converters/
│   ├── qss_converter.py       # QSS ⟷ 内部形式
│   ├── json_converter.py      # JSON ⟷ 内部形式
│   ├── vscode_converter.py    # VS Code ⟷ 内部形式
│   └── sublime_converter.py   # Sublime ⟷ 内部形式
├── validators/
│   ├── format_validator.py    # フォーマット検証
│   └── content_validator.py   # 内容整合性検証
└── dialogs/
    ├── smart_import_dialog.py # 自動判別インポート
    └── export_wizard.py      # エクスポートウィザード
```

### 6.3 変換プロセス

#### インポート処理
1. **フォーマット自動判別**: ファイル拡張子＋内容解析
2. **適切な変換器選択**: 登録済み変換器から最適選択
3. **メタデータ抽出**: 元フォーマット固有情報保持
4. **内部形式変換**: theme_manager互換データ構造へ
5. **検証実行**: データ整合性とフォーマット準拠確認

#### エクスポート処理
1. **ターゲット選択**: ユーザー指定または推奨フォーマット
2. **メタデータ結合**: 保存済みメタデータと現在状態統合
3. **フォーマット変換**: 内部形式から目標フォーマットへ
4. **最適化実行**: ターゲット固有の最適化適用
5. **検証・出力**: 結果検証後ファイル出力

### 6.4 メタデータ保持システム

```python
class ThemeMetadata:
    """テーマメタデータ管理"""
    original_format: str          # 元フォーマット識別子
    format_specific: Dict[str, Any]  # フォーマット固有データ
    conversion_history: List[Dict]   # 変換履歴
    custom_properties: Dict          # カスタムプロパティ
    validation_results: Dict         # 検証結果キャッシュ
```

### 6.5 双方向変換保証

- **可逆性原則**: A→B→A変換で情報損失最小化
- **メタデータ継承**: 変換チェーン全体でメタデータ保持
- **差分検出**: 変換前後の差分自動検出・報告
- **復元機能**: 元フォーマット情報からの復元サポート

### 6.6 スマートエクスポート機能

#### 自動最適化
- **フォーマット特化**: 各フォーマットの特徴に最適化
- **互換性考慮**: ターゲット環境の制約反映
- **パフォーマンス**: 出力サイズ・読み込み速度最適化

#### 品質保証
- **プレビュー機能**: エクスポート前結果確認
- **互換性検証**: ターゲット環境での動作確認
- **エラー修正**: 自動修正 + 手動修正オプション

## �📊 実装フェーズ

### フェーズ1: 基盤セットアップ（3-4日）
**ブランチ**: `refactor/phase1-foundation`

**目標**:
- 新しいパッケージ構造の作成
- 基本MVCアーキテクチャの実装
- 設定管理のセットアップ
- メインアプリケーションウィンドウスケルトンの作成

**成果物**:
- [ ] パッケージ構造の作成
- [ ] 基本`ThemeStudioApplication`クラス
- [ ] 設定システムの実装
- [ ] プレースホルダータブ付きメインウィンドウ
- [ ] イベントバスシステムのセットアップ

**検証基準**:
- アプリケーションがエラーなく起動する
- 基本ウィンドウレイアウトが正しく描画される
- 設定が正常に読み込まれる
- すべてのQtフレームワーク（PyQt5/PyQt6/PySide6）をサポート

### フェーズ2: アダプター層実装（2-3日）
**ブランチ**: `refactor/phase2-adapters`

**目標**:
- 既存`theme_manager`ライブラリとの安全な連携
- APIラッパーの作成
- データ変換レイヤーの実装
- 既存機能の活用

**成果物**:
- [ ] `ThemeAdapter`インターフェース実装
- [ ] 既存APIラッパー作成
- [ ] データ変換レイヤー
- [ ] 互換性テストスイート

### フェーズ3: フォーマット変換システム（4-5日）
**ブランチ**: `refactor/phase3-format-conversion`

**目標**:
- フォーマット中立インポート/エクスポートシステム
- メタデータ保持機能
- ラウンドトリップ変換対応
- スマートエクスポート機能

**成果物**:
- [ ] `format_system/`パッケージ実装
- [ ] QSS、JSON、VS Codeコンバーター
- [ ] メタデータハンドラー
- [ ] スマートインポート/エクスポートダイアログ
- [ ] 変換テストスイート

**検証基準**:
- 各フォーマット間の双方向変換が正常動作
- メタデータが適切に保持される
- ラウンドトリップ変換でデータ損失が最小限
- スマートインポートがフォーマットを正確に判別

### フェーズ4: コアエディタータブ（3-4日）
**ブランチ**: `refactor/phase4-editor-tabs`

**目標**:
- モジュラーUIコンポーネントの作成
- レスポンシブレイアウトの実装
- 高度なプレビューシステムの追加
- プロフェッショナルインターフェースの設計

**成果物**:
- [ ] タブ付きインターフェースの`MainWindow`
- [ ] プロパティパネル付き`ThemeEditorView`
- [ ] コントラスト制御付き`ZebraEditorView`
- [ ] 複数ウィジェットデモ付き`PreviewView`
- [ ] ギャラリーインターフェース付き`ThemeBrowserView`
- [ ] 再利用可能UIコンポーネントライブラリ

**検証基準**:
- 現在のエディター機能がすべて利用可能
- インターフェースが異なる画面サイズで適切にスケールする
- プレビューがリアルタイムで更新される
- ゼブラエディターが現在の機能パリティを維持する

### フェーズ5: コントローラー統合（2-3日）
**ブランチ**: `refactor/phase5-controllers`

**目標**:
- アプリケーションロジック層の実装
- ビューとモデルの接続
- 高度なテーマ操作の追加
- フォーマット変換システムの統合

**成果物**:
- [ ] メインアプリケーションフロー用`AppController`
- [ ] 編集操作用`ThemeController`
- [ ] ゼブラパターン管理用`ZebraController`
- [ ] ライブ更新用`PreviewController`
- [ ] フォーマット変換統合用`ExportController`
- [ ] **フォーマット中立インポート/エクスポート用`ExportController`**

**検証基準**:
- すべてのユーザーインタラクションが正しく動作する
- データがコンポーネント間で適切に流れる
- 複数フォーマットでのインポート/エクスポートが正常動作する
- ラウンドトリップ変換が元フォーマットを保持する
- エラーハンドリングがエッジケースをカバーする
- パフォーマンスが現在の実装と同等または上回る

### フェーズ6: サービス層と高度機能（3-4日）
**ブランチ**: `refactor/phase6-services`

**目標**:
- プロフェッショナルグレード機能の追加
- バックアップと復旧の実装
- 検証とテストツールの作成
- バッチ処理機能の追加

**成果物**:
- [ ] ファイル操作用`ThemeService`
- [ ] WCAG準拠用`ValidationService`
- [ ] 自動保存用`BackupService`
- [ ] 高度なカラーパレットツール
- [ ] バッチテーマ処理
- [ ] テーマテンプレートシステム
- [ ] 統合ロギングシステム
- [ ] Qtフレームワーク切り替えツール

**検証基準**:
- 自動保存によりデータ損失を防ぐ
- 検証がテーマエラーをキャッチする
- バッチ操作が正常に完了する
- パフォーマンスが応答性を維持する
- ロギングシステムが正しく動作する
- Qtフレームワーク切り替えが安全に実行される

### フェーズ7: テストと最終調整（2-3日）
**ブランチ**: `refactor/phase7-testing`

**目標**:
- 包括的テストスイート
- パフォーマンス最適化
- ドキュメント更新
- リリース準備

**成果物**:
- [ ] 統合テストスイート
- [ ] パフォーマンスベンチマーク
- [ ] ユーザードキュメント更新
- [ ] 旧エディターからの移行ガイド
- [ ] リリースノート準備

**検証基準**:
- すべての既存機能が保持される
- パフォーマンスが改善または維持される
- ドキュメントが完全で正確
- 移行パスが検証される

## 🔄 移行戦略

### 後方互換性
- すべての現在のAPIとファイル形式を保持
- 自動移行ツールの提供
- 破壊的変更の明確な文書化

### ロールバック計画
- 各フェーズを別ブランチで実施
- マージ前の包括的バックアップ
- 段階的ロールアウト用機能フラグ
- 各ステップでの自動テスト

### データ移行
- 自動テーマ設定移行
- 設定の保持
- ユーザー設定の転送
- 移行前のバックアップ作成

## 🧪 テスト戦略

### 単体テスト
- モデル層: 95%カバレッジ目標
- ユーティリティ関数: 100%カバレッジ
- 色計算: 包括的エッジケース
- ファイル操作: モックベーステスト
- **フォーマット変換**: 各変換器の詳細テスト

### 統合テスト
- コンポーネント間相互作用検証
- クロスQtフレームワーク互換性
- テーマロード/保存ワークフロー
- プレビュー同期精度
- **ラウンドトリップ変換**: フォーマット間双方向変換検証

### ユーザー受け入れテスト
- 現在のユーザーワークフロー保持
- 新機能ユーザビリティ検証
- パフォーマンス比較テスト
- アクセシビリティ準拠検証
- **フォーマット変換ワークフロー**: エンドツーエンドテスト

### パフォーマンステスト
- アプリケーション起動時間
- テーマ切り替え応答性
- メモリ使用量最適化
- 大きなテーマファイル処理
- **変換速度**: 大容量ファイル変換性能

## 📈 成功指標

### 定量的目標
- **コード品質**: 循環複雑度を50%削減
- **テストカバレッジ**: 90%以上の全体カバレッジ達成
- **パフォーマンス**: 現在の速度を維持または改善
- **ファイルサイズ**: コードベースサイズを30%削減
- **バグ密度**: < 0.1 bugs per KLOC

### 定性的目標
- **保守性**: 新機能追加が容易
- **ユーザーエクスペリエンス**: より直感的でプロフェッショナル
- **開発者エクスペリエンス**: 貢献がより簡単
- **ドキュメント**: 完全で最新
- **アーキテクチャ**: クリーンで拡張可能

## 🗂️ ファイル移行マップ

### リファクタリング対象ファイル
```
# 既存ライブラリ（変更なし - 完全保護）
theme_manager/                      # ✅ 一切変更しない
├── __init__.py                    # 安定版API保持
├── main.py                        # コアライブラリ保持
├── qt/                           # Qt統合モジュール保持
└── ...                           # 全機能現状維持

# リファクタリング対象（GUI層のみ）
現在 → 新しい場所
launch_theme_editor.py → qt_theme_studio/views/theme_editor_view.py + 非推奨ラッパー保持
launch_zebra_theme_editor.py → qt_theme_studio/views/zebra_editor_view.py + 非推奨ラッパー保持
launch_gui_preview.py → qt_theme_studio/views/preview_view.py + 非推奨ラッパー保持
theme_editor_zebra_extension.py → qt_theme_studio/controllers/zebra_controller.py
zebra_pattern_editor.py → qt_theme_studio/controllers/zebra_controller.py（統合）

# 活用される既存機能（変更なし）
theme_manager/qt/preview.py → qt_theme_studio/adapters/preview_adapter.py（経由）
theme_manager/qt/theme_editor.py → qt_theme_studio/adapters/theme_adapter.py（経由）
theme_manager/qt/loader.py → 直接活用（変更なし）
theme_manager/qt/stylesheet.py → 直接活用（変更なし）
```

### 削除するファイル
- 個別起動スクリプト（統合により不要）
  - `launch_theme_editor.py` → 削除
  - `launch_zebra_theme_editor.py` → 削除
  - `launch_gui_preview.py` → 削除
- 一部のヘルパースクリプト（統合により不要になったもの）
  - `theme_editor_zebra_extension.py` → 機能を`qt_theme_studio`に統合
  - `zebra_pattern_editor.py` → 機能を`qt_theme_studio`に統合

### 新規作成ファイル
- `launch_theme_studio.py` - 統合アプリケーションランチャー
- `qt_theme_studio/` - 完全新規のGUIアプリケーションパッケージ
- アダプター層 - 既存ライブラリとの橋渡し
- GUI専用のテストスイート
- 更新されたGUI用ドキュメント

### 🔒 **保護されるファイル（変更禁止）**
- `theme_manager/` - **全てのファイル・サブディレクトリ**
- 既存のCLIツール - `theme_manager/cli/`
- 既存のAPIドキュメント - 現状維持
- 既存の設定ファイル形式 - 互換性保持

## 🚀 リリース後計画

### v1.0.1 - 安定性リリース
- ユーザーフィードバックに基づくバグ修正
- パフォーマンス最適化
- ドキュメント改善

### v1.1.0 - 拡張機能
- プラグインシステム実装
- 高度なカラーハーモニーツール
- テーマ共有マーケットプレース統合

### v1.2.0 - コラボレーション機能
- チームコラボレーションツール
- バージョン管理統合
- クラウド同期

## 📝 実装チェックリスト

### 実装前
- [ ] 現在のコードベースの包括的バックアップ作成
- [ ] 開発ブランチ構造のセットアップ
- [ ] テストデータとシナリオの準備
- [ ] 現在の機能インベントリの文書化

### 実装中
- [ ] 日次進捗追跡
- [ ] 継続的統合検証
- [ ] 定期的ステークホルダーレビュー
- [ ] パフォーマンス監視

### 実装後
- [ ] ユーザー移行支援
- [ ] ドキュメント更新
- [ ] コミュニティフィードバック収集
- [ ] パフォーマンス分析

## 🔧 新規追加ソリューション詳細

### フォーマット中立インポート/エクスポートシステム

#### 目的
- **複数フォーマット対応**: QSS、JSON、VS Code、WebStorm等の幅広いテーマフォーマット
- **ラウンドトリップ変換**: インポート→編集→エクスポートで情報ロスなし
- **既存ライブラリ活用**: `theme_manager`の安定したAPIを最大限活用
- **ユーザビリティ向上**: フォーマットを意識せずにテーマ編集が可能

#### アーキテクチャ設計

**1. アダプターパターンによるフォーマット抽象化**
```
qt_theme_studio/adapters/
├── format_adapter.py           # 統一フォーマット変換システム
├── theme_format_converter.py   # フォーマット別変換器基底クラス
├── converters/
│   ├── qtm_converter.py        # Qt-Theme-Manager標準フォーマット
│   ├── qss_converter.py        # Qtスタイルシート変換
│   ├── json_converter.py       # 汎用JSON形式変換
│   ├── vscode_converter.py     # VS Codeテーマ変換
│   └── webstorm_converter.py   # WebStormテーマ変換
└── format_metadata.py          # メタデータ保持システム
```

**2. ラウンドトリップ対応データ構造**
- **FormatAwareThemeData**: 元フォーマット情報付きテーマデータ
- **ImportMetadata**: インポート時の詳細情報保持
- **OriginalStructure**: 元ファイルの構造・順序・コメント保持

**3. 統一内部フォーマット**
- 既存の`theme_manager`フォーマットを基準とする統一仕様
- すべての変換は内部フォーマットを経由
- フォーマット固有情報はメタデータで保持

#### 主要機能

**1. 自動フォーマット検出**
- ファイル拡張子による初期判定
- 内容解析による精密判定
- 複数フォーマット候補の提示

**2. メタデータ保持システム**
- 元ファイルの構造情報保持
- JSON順序・コメント・空白の保持
- フォーマット固有設定の保持
- 変換時の警告・注意事項記録

**3. スマートエクスポートUI**
- 元フォーマットでの推奨エクスポート
- 任意フォーマットへの変換オプション
- エクスポート前プレビュー機能
- 変換品質インジケーター

**4. プラグイン拡張システム**
- カスタムフォーマットの追加対応
- サードパーティフォーマット支援
- コミュニティ拡張の受け入れ

#### 技術仕様

**対応予定フォーマット**
- **Qt-Theme-Manager**: 標準内部フォーマット（100%互換）
- **QSS**: Qtスタイルシート（`theme_manager.qt.stylesheet`活用）
- **JSON**: 汎用JSON形式（カスタマイズ可能）
- **VS Code**: `.json`テーマファイル（colors, tokenColors対応）
- **WebStorm**: IntelliJ系IDE テーマ
- **CSS**: Web CSS風記法（実験的）

**変換品質レベル**
- **完全互換**: 情報ロスなしの双方向変換
- **高品質**: 主要情報保持、一部メタデータ欠損
- **基本互換**: 基本色・プロパティのみ変換
- **実験的**: 部分対応、手動調整必要

#### 実装戦略

**フェーズ1: 基本フォーマット対応**
- Qt-Theme-Manager（既存）
- QSS（`theme_manager`活用）
- 汎用JSON

**フェーズ2: 主要IDE対応**
- VS Code形式
- WebStorm形式

**フェーズ3: プラグインシステム**
- カスタムフォーマット追加機能
- コミュニティ拡張対応

#### 品質保証

**テスト戦略**
- 各フォーマットのラウンドトリップテスト
- 大量テーマファイルでの変換精度検証
- エッジケース・破損ファイル対応テスト
- パフォーマンステスト（大容量ファイル）

**エラーハンドリング**
- 部分的変換の継続実行
- 詳細エラーログと修復提案
- 安全なフォールバック処理
- ユーザーフレンドリーなエラーメッセージ

### 統合ロギングシステム

#### 目的
- リファクタリング後のデバッグ効率向上
- ユーザーサポート時の問題特定迅速化
- パフォーマンス分析とボトルネック特定
- 開発中のトラブルシューティング支援

#### 技術仕様
```python
# utilities/logger_utils.py
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ThemeStudioLogger:
    def __init__(self, name: str = "ThemeStudio"):
        self.logger = logging.getLogger(name)
        self.setup_logger()

    def setup_logger(self):
        """ロガーの初期設定"""
        self.logger.setLevel(logging.DEBUG)

        # ファイルハンドラー（詳細ログ）
        file_handler = self._create_file_handler()
        file_handler.setLevel(logging.DEBUG)

        # コンソールハンドラー（重要ログのみ）
        console_handler = self._create_console_handler()
        console_handler.setLevel(logging.INFO)

        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s'
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _create_file_handler(self):
        """ログファイルハンドラーの作成"""
        log_dir = Path.home() / ".qt_theme_studio" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"theme_studio_{datetime.now().strftime('%Y%m%d')}.log"
        return logging.FileHandler(log_file, encoding='utf-8')

    def _create_console_handler(self):
        """コンソールハンドラーの作成"""
        return logging.StreamHandler(sys.stdout)

    def log_qt_framework_info(self):
        """Qtフレームワーク情報のログ出力"""
        try:
            import PyQt6
            self.info(f"PyQt6 detected: {PyQt6.QtCore.PYQT_VERSION_STR}")
        except ImportError:
            pass

        try:
            import PyQt5
            self.info(f"PyQt5 detected: {PyQt5.QtCore.PYQT_VERSION_STR}")
        except ImportError:
            pass

        try:
            import PySide6
            self.info(f"PySide6 detected: {PySide6.__version__}")
        except ImportError:
            pass

    def log_performance_metrics(self, operation: str, duration: float, **kwargs):
        """パフォーマンスメトリクスのログ出力"""
        metrics = {
            'operation': operation,
            'duration_ms': round(duration * 1000, 2),
            **kwargs
        }
        self.info(f"Performance: {metrics}")

    def log_user_action(self, action: str, details: dict = None):
        """ユーザーアクションのログ出力"""
        log_data = {'user_action': action}
        if details:
            log_data.update(details)
        self.info(f"User Action: {log_data}")

    def log_error_with_context(self, error: Exception, context: dict = None):
        """エラーとコンテキスト情報のログ出力"""
        error_data = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {}
        }
        self.error(f"Error occurred: {error_data}", exc_info=True)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str):
        self.logger.critical(message)

# シングルトンインスタンス
logger = ThemeStudioLogger()
```

#### 使用例
```python
from qt_theme_studio.utilities.logger_utils import logger

# 基本ログ出力
logger.info("アプリケーション開始")
logger.debug("テーマファイル読み込み開始")

# パフォーマンス測定
import time
start_time = time.time()
# 処理実行
duration = time.time() - start_time
logger.log_performance_metrics("theme_loading", duration, theme_count=15)

# ユーザーアクション記録
logger.log_user_action("theme_changed", {"from": "dark", "to": "light"})

# エラーログ（コンテキスト付き）
try:
    # 何らかの処理
    pass
except Exception as e:
    logger.log_error_with_context(e, {"theme_name": "custom_theme", "operation": "save"})
```

### Qtフレームワーク切り替えシステム

#### 目的
- 開発/テスト時のフレームワーク切り替え効率化
- 互換性テストの自動化
- 安全なパッケージ管理
- 環境依存の問題解決支援

#### 技術仕様
```python
# utilities/qt_framework_manager.py
import subprocess
import sys
from enum import Enum
from typing import List, Optional, Dict, Tuple
from pathlib import Path
import json
import tempfile
import shutil

class QtFramework(Enum):
    PYQT5 = "PyQt5"
    PYQT6 = "PyQt6"
    PYSIDE6 = "PySide6"

class QtFrameworkManager:
    def __init__(self):
        self.logger = ThemeStudioLogger("QtFrameworkManager")
        self.backup_dir = Path.home() / ".qt_theme_studio" / "framework_backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def detect_current_framework(self) -> Optional[QtFramework]:
        """現在インストールされているQtフレームワークを検出"""
        frameworks = []

        try:
            import PyQt6
            frameworks.append(QtFramework.PYQT6)
            self.logger.debug(f"PyQt6 detected: {PyQt6.QtCore.PYQT_VERSION_STR}")
        except ImportError:
            pass

        try:
            import PyQt5
            frameworks.append(QtFramework.PYQT5)
            self.logger.debug(f"PyQt5 detected: {PyQt5.QtCore.PYQT_VERSION_STR}")
        except ImportError:
            pass

        try:
            import PySide6
            frameworks.append(QtFramework.PYSIDE6)
            self.logger.debug(f"PySide6 detected: {PySide6.__version__}")
        except ImportError:
            pass

        if len(frameworks) == 1:
            return frameworks[0]
        elif len(frameworks) > 1:
            self.logger.warning(f"Multiple Qt frameworks detected: {frameworks}")
            return frameworks[0]  # 最初に見つかったものを返す
        else:
            self.logger.warning("No Qt framework detected")
            return None

    def get_framework_packages(self, framework: QtFramework) -> List[str]:
        """フレームワークに必要なパッケージリストを取得"""
        package_map = {
            QtFramework.PYQT5: ["PyQt5==5.15.*", "PyQt5-tools"],
            QtFramework.PYQT6: ["PyQt6", "PyQt6-tools"],
            QtFramework.PYSIDE6: ["PySide6"]
        }
        return package_map.get(framework, [])

    def create_environment_backup(self) -> str:
        """現在の環境をバックアップ"""
        backup_name = f"backup_{QtFramework.__name__}_{int(time.time())}"
        backup_path = self.backup_dir / f"{backup_name}.txt"

        try:
            # pip freeze の結果を保存
            result = subprocess.run([sys.executable, "-m", "pip", "freeze"],
                                  capture_output=True, text=True, check=True)

            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(result.stdout)

            self.logger.info(f"Environment backup created: {backup_path}")
            return str(backup_path)

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create backup: {e}")
            raise

    def uninstall_qt_frameworks(self) -> bool:
        """すべてのQtフレームワークをアンインストール"""
        qt_packages = ["PyQt5", "PyQt5-tools", "PyQt6", "PyQt6-tools", "PySide6"]

        try:
            for package in qt_packages:
                self.logger.info(f"Uninstalling {package}...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "uninstall", package, "-y"],
                    capture_output=True, text=True
                )

                if result.returncode == 0:
                    self.logger.info(f"Successfully uninstalled {package}")
                else:
                    self.logger.debug(f"Package {package} was not installed or already removed")

            return True

        except Exception as e:
            self.logger.error(f"Error during uninstallation: {e}")
            return False

    def install_framework(self, framework: QtFramework) -> bool:
        """指定されたQtフレームワークをインストール"""
        packages = self.get_framework_packages(framework)

        try:
            for package in packages:
                self.logger.info(f"Installing {package}...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", package],
                    capture_output=True, text=True, check=True
                )
                self.logger.info(f"Successfully installed {package}")

            return True

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install {framework.value}: {e}")
            return False

    def switch_framework(self, target_framework: QtFramework,
                        create_backup: bool = True) -> bool:
        """Qtフレームワークを安全に切り替え"""
        self.logger.info(f"Starting framework switch to {target_framework.value}")

        # バックアップ作成
        backup_path = None
        if create_backup:
            try:
                backup_path = self.create_environment_backup()
            except Exception as e:
                self.logger.error(f"Backup creation failed: {e}")
                return False

        # 現在のフレームワークを記録
        current = self.detect_current_framework()
        if current:
            self.logger.info(f"Current framework: {current.value}")

        try:
            # 既存フレームワークのアンインストール
            if not self.uninstall_qt_frameworks():
                raise Exception("Failed to uninstall existing frameworks")

            # 新しいフレームワークのインストール
            if not self.install_framework(target_framework):
                raise Exception(f"Failed to install {target_framework.value}")

            # 切り替え成功の確認
            new_framework = self.detect_current_framework()
            if new_framework == target_framework:
                self.logger.info(f"Successfully switched to {target_framework.value}")
                return True
            else:
                raise Exception("Framework switch verification failed")

        except Exception as e:
            self.logger.error(f"Framework switch failed: {e}")

            # ロールバック処理
            if backup_path and Path(backup_path).exists():
                self.logger.info("Attempting rollback...")
                try:
                    self.restore_from_backup(backup_path)
                    self.logger.info("Rollback completed")
                except Exception as rollback_error:
                    self.logger.critical(f"Rollback failed: {rollback_error}")

            return False

    def restore_from_backup(self, backup_path: str) -> bool:
        """バックアップから環境を復元"""
        try:
            # 現在の環境をクリア
            self.uninstall_qt_frameworks()

            # バックアップから復元
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", backup_path],
                         check=True)

            self.logger.info(f"Environment restored from {backup_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to restore from backup: {e}")
            return False

    def test_framework_compatibility(self, framework: QtFramework) -> Dict[str, bool]:
        """フレームワーク互換性テスト"""
        results = {
            'import_success': False,
            'widget_creation': False,
            'stylesheet_support': False
        }

        try:
            if framework == QtFramework.PYQT5:
                from PyQt5.QtWidgets import QApplication, QWidget
                from PyQt5.QtCore import Qt
            elif framework == QtFramework.PYQT6:
                from PyQt6.QtWidgets import QApplication, QWidget
                from PyQt6.QtCore import Qt
            elif framework == QtFramework.PYSIDE6:
                from PySide6.QtWidgets import QApplication, QWidget
                from PySide6.QtCore import Qt

            results['import_success'] = True

            # ウィジェット作成テスト
            app = QApplication.instance() or QApplication([])
            widget = QWidget()
            results['widget_creation'] = True

            # スタイルシートテスト
            widget.setStyleSheet("background-color: red;")
            results['stylesheet_support'] = True

            widget.close()

        except Exception as e:
            self.logger.error(f"Compatibility test failed: {e}")

        return results

# CLI インターフェース
class QtFrameworkCLI:
    def __init__(self):
        self.manager = QtFrameworkManager()

    def run_interactive_mode(self):
        """対話式フレームワーク切り替え"""
        print("Qt Framework Manager")
        print("=" * 30)

        current = self.manager.detect_current_framework()
        if current:
            print(f"Current framework: {current.value}")
        else:
            print("No Qt framework detected")

        print("\nAvailable frameworks:")
        for i, framework in enumerate(QtFramework, 1):
            print(f"{i}. {framework.value}")

        try:
            choice = int(input("\nSelect framework to switch to (1-3): "))
            if 1 <= choice <= 3:
                target = list(QtFramework)[choice - 1]

                confirm = input(f"Switch to {target.value}? (y/N): ")
                if confirm.lower() == 'y':
                    success = self.manager.switch_framework(target)
                    if success:
                        print(f"Successfully switched to {target.value}")
                    else:
                        print("Framework switch failed. Check logs for details.")
                else:
                    print("Operation cancelled.")
            else:
                print("Invalid choice.")

        except (ValueError, KeyboardInterrupt):
            print("\nOperation cancelled.")

if __name__ == "__main__":
    cli = QtFrameworkCLI()
    cli.run_interactive_mode()
```

#### 使用例

**コマンドライン使用**:
```bash
# 対話式切り替え
python -m qt_theme_studio.utilities.qt_framework_manager

# スクリプトからの使用
python -c "
from qt_theme_studio.utilities.qt_framework_manager import QtFrameworkManager, QtFramework
manager = QtFrameworkManager()
manager.switch_framework(QtFramework.PYQT6)
"
```

**アプリケーション内統合**:
```python
from qt_theme_studio.utilities.qt_framework_manager import QtFrameworkManager, QtFramework

# 設定画面でのフレームワーク切り替えボタン
class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.framework_manager = QtFrameworkManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # フレームワーク選択コンボボックス
        self.framework_combo = QComboBox()
        for framework in QtFramework:
            self.framework_combo.addItem(framework.value, framework)

        # 切り替えボタン
        switch_button = QPushButton("Switch Framework")
        switch_button.clicked.connect(self.switch_framework)

        layout.addWidget(QLabel("Qt Framework:"))
        layout.addWidget(self.framework_combo)
        layout.addWidget(switch_button)
        self.setLayout(layout)

    def switch_framework(self):
        selected_framework = self.framework_combo.currentData()

        # 確認ダイアログ
        reply = QMessageBox.question(
            self, "Confirm Switch",
            f"Switch to {selected_framework.value}?\nThis will restart the application.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = self.framework_manager.switch_framework(selected_framework)
            if success:
                QMessageBox.information(self, "Success", "Framework switched successfully. Please restart the application.")
            else:
                QMessageBox.critical(self, "Error", "Framework switch failed. Check logs for details.")
```

## 🔧 開発ガイドライン

### コード標準
- PythonコードスタイルにPEP 8を使用
- 全体を通してタイプヒントを使用
- docstringカバレッジを維持
- 一貫した命名規則を適用

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

---

**次のステップ**: この計画をレビューし、フェーズ1から実装を開始。

**開発体制**: 単体開発（Amazon Kiro支援）

**バージョン**: 1.0.0 - リファクタリング計画
