# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.3] - 2025-07-22

### 🚀 Added
- **エントリーポイント追加**
  - `theme-editor` コマンド: GUIテーマエディターの直接起動
  - `theme-preview` コマンド: テーマプレビューウィンドウの直接起動  
  - `theme-manager` コマンド: CLIツールの統一インターフェース

### 🎨 Added
- **CLI プレビュー機能強化**
  - `launch_gui_preview.py` にコマンドライン引数対応
  - `--config` オプション: カスタム設定ファイル指定
  - `--theme` オプション: 起動時テーマ指定
  - アクセシビリティ改善テーマのプレビュー対応

### 🐍 Changed
- **Python サポート更新**
  - Python 3.9+ のみサポート（Python 3.8 サポート終了）
  - モダンなPython環境に最適化
  - CI/CDテストマトリックスから Python 3.8 削除

### 🔄 Added  
- **テーマフォーマット変換機能**
  - カスタムテーマ→Qt-Theme-Manager形式変換ツール
  - 16テーマの完全変換対応（アクセシビリティ改善版含む）
  - 変換済みアクセシビリティ強化テーマセット

### ♿ Improved
- **アクセシビリティ大幅改善**
  - ゼブラスタイル：6%ライトネス差で目に優しい設計
  - 全16テーマで統一されたコントラスト比
  - WCAG基準を考慮した色彩設計

### 📚 Enhanced
- ヘルプメッセージと使用例の改善
- エラーハンドリングの強化
- デバッグ情報の詳細化

## [0.2.2] - 2025-07-21

### 🤖 Added
- **自動リリースシステム**
  - GitHub Actions によるPyPI自動公開
  - マルチプラットフォーム（Ubuntu/Windows/macOS）CI/CDテスト
  - Python 3.8-3.12 × PyQt5/PyQt6/PySide6 の組み合わせテスト
  - `release.sh` ワンコマンドリリーススクリプト
  - CI/CDステータスバッジをREADMEに追加

### 📚 Improved
- ドキュメントに自動リリース機能の説明を追加
- 開発ワークフローの改善と文書化
- PyPI公開プロセスの自動化

## [0.2.1] - 2025-07-21

### 🔧 Fixed
- **GUI起動問題の完全解決**
  - テーマエディターのGUI起動失敗問題を修正
  - `launch_theme_editor.py`でのイベントループ管理を適正化
  - PyQt5での循環参照エラー（`QtAlignCenter`）を修正

- **Qt互換性の向上**
  - PyQt5/PyQt6/PySide6の互換性定数を統一
  - QSSスタイルシートからサポートされていないCSS機能を削除
  - すべてのQtフレームワークでの動作を確認

- **起動方法の統一**
  - `python -m theme_manager.qt.theme_editor` 
  - `python launch_theme_editor.py`
  - 両方の方法で確実にGUIが起動するように修正

### 📦 Changed  
- デフォルトのQtフレームワークをPyQt6に変更
- エラーハンドリングとログの改善
- KeyboardInterrupt（Ctrl+C）サポートを追加

## [0.2.0] - 2025-07-20 ✅ **Released to PyPI**

🎉 **Successfully published to PyPI: https://pypi.org/project/qt-theme-manager/0.2.0/**

### Added
- 🎨 **高度なテーマエディタ機能**
  - 色彩理論に基づく色選択（補色、三角色、類似色）
  - リアルタイムプレビュー機能
  - コンポーネント別詳細設定
  - アクセシビリティ機能（コントラスト比チェック）
  
- 🖥️ **GUIツールのpipエントリーポイント**
  - `theme-editor` コマンドでテーマエディター起動
  - `theme-preview` コマンドでプレビュー起動
  - `theme-manager` CLIコマンド

- 📁 **開発者向け環境整備**
  - `examples/` ディレクトリ（公式サンプル）
  - `sandbox/` ディレクトリ（開発実験用、Gitから除外）
  - `temp/` ディレクトリ（一時ファイル用、Gitから除外）
  - 開発ガイドライン `DEVELOPMENT.md`

- 🎯 **テーマカスタマイズ機能強化**
  - 16種類の基本テーマサポート
  - カスタムテーマ作成支援
  - テーマのインポート/エクスポート機能

### Improved
- 🚀 **パフォーマンス向上**
  - テーマ適用速度の最適化
  - メモリ使用量の削減

- 🎨 **UI/UX改善**
  - より直感的なテーマエディターインターフェース
  - レスポンシブデザインの向上
  - ユーザビリティの向上

- 📚 **ドキュメント強化**
  - 日本語ドキュメント充実
  - API リファレンス更新
  - 使用例の追加

### Fixed
- 🐛 **バグ修正**
  - テーマ切り替え時の表示不具合修正
  - メモリリーク問題の解決
  - 特定環境での初期化エラー修正

### Changed
- 📦 **パッケージ構成改善**
  - より適切なモジュール構成
  - インストール時のファイル配置最適化

### Technical
- 🔧 **開発環境改善**
  - `.gitignore` パターン強化
  - リリースワークフロー文書化
  - 自動化準備

## [0.1.0] - 2025-XX-XX

### Added
- 初回PyPI公開
- 基本的なテーマ管理機能
- PyQt5/PyQt6/PySide6サポート
- CLIインターフェース

### Features
- テーマの動的切り替え
- 設定の永続化
- 基本的なGUIコンポーネント

---

## 今後の予定

### [0.3.0] - 2025年8月予定
- GitHub Actions自動化（タグプッシュ→自動PyPI公開）
- テストスイート強化
- パフォーマンス監視機能
- ユーザーフィードバック対応

### [1.0.0] - 2025年秋予定
- 安定版リリース
- 完全なAPI安定性保証
- 企業利用向け機能追加
- プラグインシステム検討
