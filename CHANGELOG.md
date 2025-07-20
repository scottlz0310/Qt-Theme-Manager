# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
