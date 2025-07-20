# Release Workflow

## PyPI更新手順

### 1. 準備段階
```bash
# 現在のGitHubの変更をプル
git pull origin main

# テスト実行
python -m pytest tests/

# パッケージのクリーンビルド
python -m build --clean
```

### 2. バージョン更新
以下のファイルでバージョン番号を更新:
- `setup.py` (line 7)
- `pyproject.toml` (line 7)
- `theme_manager/__init__.py`

### 3. CHANGELOG更新
新機能と変更点を記録:
```markdown
## [0.2.0] - 2025-07-20

### Added
- 高度なテーマエディタ機能
- 色彩理論に基づく色選択
- アクセシビリティ機能
- コンポーネント別詳細設定

### Improved
- テーマ適用のパフォーマンス向上
- UI/UXの改善

### Fixed
- テーマ切り替え時のバグ修正
```

### 4. ビルドとテスト
```bash
# パッケージビルド
python -m build

# テスト用インストール（仮想環境推奨）
pip install dist/qt_theme_manager-0.2.0-py3-none-any.whl

# 機能テスト
python -c "from theme_manager import ThemeController; print('Import successful')"
```

### 5. PyPI公開
```bash
# TestPyPIでテスト（推奨）
twine upload --repository testpypi dist/*

# テストから確認
pip install --index-url https://test.pypi.org/simple/ qt-theme-manager==0.2.0

# 本番PyPIに公開
twine upload dist/*
```

### 6. GitHub側の対応
```bash
# タグ作成
git tag v0.2.0
git push origin v0.2.0

# GitHubリリース作成（手動またはGH CLI）
gh release create v0.2.0 --title "v0.2.0 - Advanced Theme Editor" --notes-file CHANGELOG.md
```

## 自動化への移行（将来的）

### GitHub Actions設定例
`.github/workflows/pypi-publish.yml`:
```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## 推奨リリース頻度

- **マイナーリリース**: 月1回程度（重要機能追加時）
- **パッチリリース**: 必要に応じて（バグ修正時）
- **メジャーリリース**: 半年〜1年（破壊的変更時）
