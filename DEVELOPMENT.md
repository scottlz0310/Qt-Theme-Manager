# Development Guidelines

## 🚀 自動リリースワークフロー

v0.2.1から、PyPIへの自動リリースが可能になりました！

### 簡単リリース方法

1. **自動リリーススクリプト使用（推奨）**
   ```bash
   # バージョン番号と説明を指定
   ./release.sh 0.2.2 "Fix critical GUI bugs and enhance performance"
   ```

2. **手動リリース**
   ```bash
   # バージョンを更新（pyproject.toml, setup.py, __init__.py）
   # コミットしてタグを作成
   git add -A
   git commit -m "Release v0.2.2"
   git tag v0.2.2
   git push origin main --tags
   ```

どちらの方法でも、GitHub Actionsが自動的に：
- ✅ テスト実行（Python 3.8-3.12 × PyQt5/PyQt6/PySide6）
- 📦 パッケージビルド
- 🚀 PyPIリリース

を実行します。

### CI/CDバッジ

READMEにCI/CDステータスバッジを追加済み：
[![CI/CD Tests](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml/badge.svg)](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml)

## ディレクトリ構成

### `examples/` - 公式サンプル（Gitに含まれる）
実際のユーザーが参考にするための高品質なサンプルコード
- `basic/` - 基本的な使用例
- `advanced/` - 高度な使用例  
- `integration/` - 他のライブラリとの統合例

### `sandbox/` - 開発用実験場（Gitから除外）
開発者が自由に実験できるスペース
- プロトタイプ開発
- アイデア検証
- 一時的なテストコード

### `temp/` - 一時ファイル（Gitから除外）
自動生成ファイルや一時的なデータ
- ビルド成果物
- キャッシュファイル
- テスト時の一時データ

## ファイル命名規則

### Examples（推奨）
- `example_*.py` - 基本的なサンプル
- `demo_*.py` - デモンストレーション
- `integration_*.py` - 統合例

### Sandbox/Temp（自動的に除外されるパターン）
- `*_temp.py`
- `*_test.py`
- `*_example.py`
- `*_sample.py`
- `*_backup.*`
- `*_old.*`

## PyPI リリース戦略

### 現在の状況
- **PyPIパッケージ**: `qt-theme-manager` (v0.1.0)
- **GitHubリポジトリ**: 活発に開発中（v0.1.0以降の多数の機能追加）
- **状況**: GitHubが先行、PyPIが追従待ち

### リリースタイミング
1. **マイナーリリース (v0.2.0)**: 機能追加が多数あるため推奨
2. **タイミング**: 
   - テーマエディタの安定性確認後
   - ドキュメント整備完了後
   - テスト実行完了後

### リリース前チェックリスト
- [ ] バージョン番号更新（`setup.py`, `pyproject.toml`, `__init__.py`）
- [ ] CHANGELOG.md作成・更新
- [ ] テストスイート実行
- [ ] ドキュメント更新確認
- [ ] セキュリティチェック
- [ ] パッケージビルドテスト

### 自動化の検討
- GitHub Actionsでの自動PyPI公開
- タグプッシュ時の自動リリース
- テスト通過時の自動デプロイ

## 注意事項

1. **sandbox/** と **temp/** の内容はGitに保存されません
2. 重要なコードは適切な場所に移動してください
3. examples/のコードは品質を保ってください（ユーザーが参照するため）
4. **PyPI更新前には必ずテストを実行してください**
