# Qt-Theme-Manager 開発用Makefile

.PHONY: help install test lint format security ci clean

help: ## ヘルプを表示
	@echo "利用可能なコマンド:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 開発依存関係をインストール
	uv sync --group dev --group security --group pyside6

test: ## テストを実行
	uv run pytest tests/ --cov=qt_theme_manager --cov-report=term-missing

lint: ## リントチェックを実行
	uv run ruff check qt_theme_manager/

format: ## コードフォーマットを実行
	uv run ruff format qt_theme_manager/

format-check: ## フォーマットチェックのみ実行
	uv run ruff format --check qt_theme_manager/

type-check: ## 型チェックを実行
	uv run mypy qt_theme_manager/

security: ## セキュリティスキャンを実行
	uv run bandit -r qt_theme_manager/
	uv run safety check

ci: ## ローカルCI/CDチェックを実行
	./scripts/local-ci.sh

pre-commit-install: ## pre-commitフックをインストール
	uv run pre-commit install

pre-commit-run: ## pre-commitを全ファイルに実行
	uv run pre-commit run --all-files

pre-commit-ci: ## CI相当のpre-commitチェックを実行
	uv run pre-commit run --hook-stage manual ci-tests
	uv run pre-commit run --hook-stage manual security-scan

pre-commit-full: ## 完全なCI/CDチェックをpre-commitで実行
	uv run pre-commit run --hook-stage manual full-ci-check

clean: ## 一時ファイルを削除
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/
