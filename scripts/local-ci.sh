#!/bin/bash
# ローカルCI/CDチェックスクリプト

set -e

echo "🚀 ローカルCI/CDチェックを開始..."

# 色付きの出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 関数定義
run_check() {
    local name="$1"
    local command="$2"

    echo -e "${BLUE}📋 $name${NC}"
    if eval "$command"; then
        echo -e "${GREEN}✅ $name - 成功${NC}"
        return 0
    else
        echo -e "${RED}❌ $name - 失敗${NC}"
        return 1
    fi
}

# 依存関係の確認
echo -e "${YELLOW}📦 依存関係を同期中...${NC}"
uv sync --group dev --group security --group pyside6

# CI/CDチェック実行
echo -e "\n${BLUE}🔍 コード品質チェック${NC}"
run_check "Ruff リント" "uv run ruff check qt_theme_manager/"
run_check "Ruff フォーマット" "uv run ruff format --check qt_theme_manager/"
run_check "MyPy 型チェック" "uv run mypy qt_theme_manager/"

echo -e "\n${BLUE}🧪 テスト実行${NC}"
run_check "PyTest テスト" "uv run pytest tests/ --cov=qt_theme_manager --cov-report=term-missing --cov-fail-under=95"

echo -e "\n${BLUE}🔒 セキュリティスキャン${NC}"
run_check "Bandit セキュリティ" "uv run bandit -r qt_theme_manager/ -q --skip B110"
run_check "Safety 脆弱性" "uv run safety check --output text"

echo -e "\n${GREEN}🎉 全てのチェックが完了しました！${NC}"
echo -e "${YELLOW}💡 このスクリプトはGitHub Actionsのci.ymlとsecurity.ymlと同等のチェックを実行します${NC}"
