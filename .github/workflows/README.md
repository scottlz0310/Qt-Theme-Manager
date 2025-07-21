# PyPI自動リリース設定ガイド

このディレクトリには、Qt Theme ManagerをPyPIに自動リリースするためのGitHub Actionsワークフローが含まれています。

## 🚀 自動リリースの設定方法

### 1. PyPI APIトークンの取得

1. [PyPI](https://pypi.org)にログイン
2. Account Settings > API tokens
3. "Add API token"をクリック
4. Scope: "Entire account" または特定のプロジェクト
5. トークンをコピー（**一度だけ表示されます**）

### 2. GitHub Secretsの設定

1. GitHubリポジトリの Settings > Secrets and variables > Actions
2. "New repository secret"をクリック
3. Name: `PYPI_API_TOKEN`
4. Secret: コピーしたAPIトークンをペースト
5. "Add secret"をクリック

### 3. リリースの実行

```bash
# バージョンを上げてコミット
git add -A
git commit -m "Release v0.2.2: New features"

# タグを作成してプッシュ
git tag v0.2.2
git push origin main --tags
```

これだけで自動的に以下が実行されます：
1. 🧪 **テスト実行**: Python 3.8-3.12 × PyQt5/PyQt6/PySide6の組み合わせ
2. 📦 **パッケージビルド**: wheel と tar.gz の生成
3. ✅ **品質チェック**: twine check でパッケージの検証
4. 🚀 **PyPIリリース**: 自動的にPyPIに公開

## 📋 ワークフローファイル

### `publish-to-pypi.yml`
- **トリガー**: `v*` タグのプッシュ時
- **機能**: テスト→ビルド→PyPIリリース

### `ci-cd-tests.yml` 
- **トリガー**: mainブランチ、PRの作成・更新時
- **機能**: 継続的インテグレーションテスト

## 🔧 Trusted Publishing（推奨）

APIトークンの代わりに、より安全なTrusted Publishingも設定可能：

1. PyPIのプロジェクトページ → Publishing → "Add a new publisher"
2. GitHub Actionsを選択し、リポジトリ情報を入力
3. `publish-to-pypi.yml`から`password:`行を削除

## 🎯 リリース戦略

### セマンティックバージョニング
- **v0.x.y** (パッチ): バグフィックス
- **v0.x.0** (マイナー): 新機能
- **v1.0.0** (メジャー): 破壊的変更

### ブランチ戦略
- `main`: 安定版、プロダクション準備済み
- `develop`: 開発版、新機能の統合
- `feature/*`: 機能ブランチ

## 📊 CI/CDステータス

以下のバッジをREADMEに追加することを推奨：

```markdown
[![CI/CD Tests](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml/badge.svg)](https://github.com/scottlz0310/Qt-Theme-Manager/actions/workflows/ci-cd-tests.yml)
[![PyPI version](https://badge.fury.io/py/qt-theme-manager.svg)](https://badge.fury.io/py/qt-theme-manager)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qt-theme-manager)](https://pypi.org/project/qt-theme-manager/)
```

## 🚨 トラブルシューティング

### よくある問題

1. **テストの失敗**: 
   - ローカルでのテスト実行: `python test_theme_manager.py`
   - 全Qt框架での動作確認

2. **ビルドエラー**:
   - `python -m build` でローカルビルドテスト
   - `twine check dist/*` でパッケージ検証

3. **PyPIアップロードの失敗**:
   - APIトークンの確認
   - バージョン番号の重複チェック

### ログの確認

GitHub ActionsのログでCI/CDの詳細を確認：
1. リポジトリの Actions タブ
2. 失敗したワークフローをクリック
3. 各ジョブのログを確認

---

これらの設定により、開発者は単純に `git tag && git push --tags` するだけで、
自動的にテスト・ビルド・PyPIリリースが実行されます！ 🎉
