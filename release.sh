#!/bin/bash
# 
# 自動リリーススクリプト
# 使用方法: ./release.sh <version> [description]
# 例: ./release.sh 0.2.2 "Add new features and bug fixes"
#

set -e  # エラー時に終了

# 色付きメッセージ関数
function echo_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
function echo_success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
function echo_error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }
function echo_warning() { echo -e "\033[1;33m[WARNING]\033[0m $1"; }

# 引数チェック
if [ $# -lt 1 ]; then
    echo_error "使用方法: $0 <version> [description]"
    echo_error "例: $0 0.2.2 'Add new features and bug fixes'"
    exit 1
fi

VERSION=$1
DESCRIPTION=${2:-"Release v$VERSION"}
TAG="v$VERSION"

echo_info "🚀 Qt Theme Manager v$VERSION のリリースを開始します"
echo_info "タグ: $TAG"
echo_info "説明: $DESCRIPTION"

# 現在のブランチ確認
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo_warning "現在のブランチは '$CURRENT_BRANCH' です。mainブランチでリリースすることを推奨します。"
    read -p "続行しますか？ (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo_info "リリースを中止しました。"
        exit 1
    fi
fi

# 変更がないことを確認
if ! git diff-index --quiet HEAD --; then
    echo_error "未コミットの変更があります。先にコミットしてください。"
    exit 1
fi

# テストの実行
echo_info "🧪 テストを実行中..."
if bash test_v0.2.3_release.sh; then
    echo_success "テストが成功しました"
else
    echo_error "テストが失敗しました。修正してから再実行してください。"
    exit 1
fi

# バージョンファイルの更新
echo_info "📝 バージョン番号を更新中..."

# pyproject.toml
sed -i "s/version = \".*\"/version = \"$VERSION\"/" pyproject.toml

# setup.py
sed -i "s/version=\".*\"/version=\"$VERSION\"/" setup.py

# __init__.py
sed -i "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" theme_manager/__init__.py
sed -i "s/Version: .*/Version: $VERSION/" theme_manager/__init__.py

echo_success "バージョン番号を $VERSION に更新しました"

# パッケージのビルドとチェック
echo_info "📦 パッケージのビルドとチェック..."
python -m pip install --upgrade build twine > /dev/null 2>&1
python -m build > /dev/null 2>&1
twine check dist/* > /dev/null 2>&1
echo_success "パッケージのビルドとチェックが完了しました"

# Gitコミットとタグ作成
echo_info "📋 変更をコミット中..."
git add pyproject.toml setup.py theme_manager/__init__.py
git commit -m "🏷️ Bump version to $VERSION

$DESCRIPTION

Auto-updated by release script"

echo_info "🏷️ Gitタグを作成中..."
git tag -a "$TAG" -m "Release $TAG

$DESCRIPTION

Changes:
- Updated version to $VERSION
- Ready for PyPI automatic release via GitHub Actions"

echo_success "Gitタグ '$TAG' を作成しました"

# リモートにプッシュ
echo_info "⬆️ リモートリポジトリにプッシュ中..."
git push origin main
git push origin "$TAG"

echo_success "🎉 リリース完了！"
echo_info ""
echo_info "次のステップ："
echo_info "1. GitHub Actions で自動ビルドとPyPIリリースが実行されます"
echo_info "2. https://github.com/scottlz0310/Qt-Theme-Manager/actions で進行状況を確認"
echo_info "3. 数分後に https://pypi.org/project/qt-theme-manager/ で新バージョンを確認"
echo_info ""
echo_info "📊 進行状況の確認:"
echo_info "   GitHub Actions: https://github.com/scottlz0310/Qt-Theme-Manager/actions"
echo_info "   PyPI: https://pypi.org/project/qt-theme-manager/"
echo_info ""
echo_success "お疲れ様でした！ 🚀"
