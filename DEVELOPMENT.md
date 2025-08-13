# Development Guidelines

## 🦓 最新機能: ゼブラパターン自動生成開発

### 新しいコンポーネントの構成

注: v1.0.x ではGUI機能は別リポジトリ（qt-theme-studio）に移行しています。

1. **コア生成エンジン** (`zebra_pattern_editor.py`)
   - `ZebraPatternGenerator`: 科学的色計算クラス
   - `ZebraPatternEditor`: GUIエディターウィジェット
   - HSL/HSV色空間での精密な色調整

2. **テーマエディター統合** (`theme_editor_zebra_extension.py`)
   - 既存テーマエディターの拡張レイヤー
   - 動的な機能追加とタブ統合
   - 後方互換性を保持した設計

3. **マルチモードランチャー** (`launch_zebra_theme_editor.py`)
   - 統合モード、スタンドアロンモード、デモモード
   - エラーハンドリングとフォールバック機能
   - Qt フレームワーク自動検出

### 開発指針

- **アクセシビリティファースト**: WCAG 2.1準拠の色計算
- **科学的精度**: HSL/HSV色空間での数学的アルゴリズム  
- **クロスプラットフォーム**: PyQt5/PyQt6/PySide6完全対応
- **拡張可能設計**: プラグイン形式での機能追加

## 🚀 自動リリースワークフロー

PyPIへの自動リリースワークフローは1.0.xでも継続しています。

### 簡単リリース方法

1. **自動リリーススクリプト使用（推奨）**
   ```bash
   # バージョン番号と説明を指定
   ./release.sh 1.0.1 "Fixes and quality improvements"
   ```

2. **手動リリース**
   ```bash
   # バージョンを更新（pyproject.toml, setup.py, __init__.py）
   # コミットしてタグを作成
   git add -A
   git commit -m "Release v1.0.1"
   git tag v1.0.1
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
1. **メジャー/マイナー/パッチの選択**: 1.0.x では後方互換維持の範囲でパッチ/マイナーを選択
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
