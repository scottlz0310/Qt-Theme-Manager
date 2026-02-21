# CI/CDワークフロー

このディレクトリには、Qt Theme Managerの自動化されたCI/CDワークフローが含まれています。

## 🚀 ワークフロー概要

### 1. **ci.yml** - 継続的インテグレーション
- **トリガー**: main/developブランチへのpush、PR作成・更新
- **マトリックス**: Ubuntu/Windows/macOS × Python 3.14.2
- **チェック項目**:
  - ruff check (リント)
  - ruff format (フォーマット)
  - basedpyright (型チェック)
  - pytest (テスト + カバレッジ)
- **カバレッジ**: Codecovに自動アップロード

### 2. **security.yml** - セキュリティスキャン
- **トリガー**: main/developブランチへのpush、PR、毎週日曜日
- **スキャン項目**:
  - **Bandit**: セキュリティ脆弱性検出
  - **pip-audit**: 依存関係の脆弱性チェック
  - **CodeQL**: GitHub Advanced Security
  - **ライセンスチェック**: pip-licenses

### 3. **release.yml** - 自動リリース
- **トリガー**: `v*` タグプッシュ、workflow_dispatch
- **プロセス**:
  1. バージョン整合性チェック
  2. 品質チェック実行
  3. パッケージビルド
  4. ドキュメント自動更新
  5. GitHub Release作成
  6. PyPI自動公開

## 📋 設定要件

### GitHub Secrets
以下のシークレットを設定してください：

```
PYPI_API_TOKEN - PyPI APIトークン（リリース用）
```

### GitHub Environments
PyPI公開用に `pypi` 環境を作成し、保護ルールを設定することを推奨します。

## 🔧 使用方法

### 開発フロー
```bash
# 開発
git checkout develop
git add -A && git commit -m "feat: new feature"
git push origin develop

# プルリクエスト作成 → CI自動実行

# リリース
git checkout main
git merge develop
git tag v1.0.2
git push origin main --tags  # → 自動リリース実行
```

### 手動リリース
```bash
# GitHub Actionsページから workflow_dispatch を実行
# バージョン番号を入力（例: 1.0.2）
```

## 📊 品質基準

### テストカバレッジ
- **最低要件**: 95%
- **現在**: 98.80%

### セキュリティ
- Bandit: 1件のLow severity（意図的なexcept pass）
- pip-audit: 依存関係の脆弱性なし
- CodeQL: 静的解析パス

### コード品質
- ruff: 全チェックパス
- basedpyright: strict モード、型エラーなし

## 🚨 トラブルシューティング

### よくある問題

1. **テスト失敗**
   ```bash
   uv run pytest tests/ -v
   ```

2. **型エラー**
   ```bash
   uv run basedpyright qt_theme_manager/
   ```

3. **フォーマットエラー**
   ```bash
   uv run ruff format qt_theme_manager/
   ```

4. **セキュリティ警告**
   ```bash
   uv run bandit -r qt_theme_manager/
   ```

### ワークフロー失敗時の対処

1. **Actions**タブでログを確認
2. 該当するジョブの詳細ログを確認
3. ローカルで同じコマンドを実行して再現
4. 修正後、再プッシュで自動再実行

## 📈 メトリクス

### CI実行時間（目安）
- **ci.yml**: 約5-10分（マトリックス並列実行）
- **security.yml**: 約3-5分
- **release.yml**: 約10-15分

### 成功率
- **目標**: 95%以上
- **現在**: 安定稼働中

---

これらのワークフローにより、コード品質の維持、セキュリティの確保、自動リリースが実現されています。
