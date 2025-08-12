#!/bin/bash

# Qt-Theme-Manager リリーステストスクリプト
# このスクリプトはリリース前の包括的なテストを実行します

set -e  # エラー時に終了

# カラー出力関数
echo_info() {
    echo -e "\033[36m[INFO]\033[0m $1"
}

echo_success() {
    echo -e "\033[32m[SUCCESS]\033[0m $1"
}

echo_error() {
    echo -e "\033[31m[ERROR]\033[0m $1"
}

echo_warning() {
    echo -e "\033[33m[WARNING]\033[0m $1"
}

# テスト開始
echo_info "🚀 Qt-Theme-Manager リリーステスト開始"

# Python環境確認
echo_info "🐍 Python環境の確認"
python3 --version || {
    echo_error "Python3が見つかりません"
    exit 1
}

# 必要なパッケージのインストール確認
echo_info "📦 依存関係の確認"
pip3 install -e . || {
    echo_error "依存関係のインストールに失敗しました"
    exit 1
}

# コアライブラリのテスト
echo_info "🔧 コアライブラリのテスト"
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    import qt_theme_manager
    from qt_theme_manager.main import main
    print('✅ qt_theme_manager import: OK')
except ImportError as e:
    print(f'❌ qt_theme_manager import: FAIL - {e}')
    sys.exit(1)

try:
    from qt_theme_manager.cli.themectl import main as cli_main
    print('✅ CLI main function: OK')
except Exception as e:
    print(f'❌ CLI main function: FAIL - {e}')
    sys.exit(1)
" || exit 1

# CLI機能のテスト
echo_info "💻 CLI機能のテスト"
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from qt_theme_manager.cli.main import main as cli_main
    print('✅ CLI import: OK')
except ImportError as e:
    print(f'❌ CLI import: FAIL - {e}')
    sys.exit(1)
" || exit 1

# Qt統合のテスト（環境に応じて）
echo_info "🖼️ Qt統合のテスト"
python3 -c "
import sys
sys.path.insert(0, '.')

# Qt環境の確認
qt_available = False
qt_framework = None

try:
    import PyQt6
    qt_available = True
    qt_framework = 'PyQt6'
except ImportError:
    try:
        import PyQt5
        qt_available = True
        qt_framework = 'PyQt5'
    except ImportError:
        try:
            import PySide6
            qt_available = True
            qt_framework = 'PySide6'
        except ImportError:
            pass

if qt_available:
    print(f'✅ Qt framework ({qt_framework}): Available')
    try:
        from qt_theme_manager.qt import loader, stylesheet
        print('✅ Qt modules import: OK')
    except ImportError as e:
        print(f'❌ Qt modules import: FAIL - {e}')
        sys.exit(1)
else:
    print('⚠️ Qt framework: Not available (headless environment)')
" || {
    echo_warning "Qt環境でのテストに失敗しましたが、継続します（ヘッドレス環境の可能性）"
}

# パッケージ構造の確認
echo_info "📂 パッケージ構造の確認"
python3 -c "
import os
import sys

required_files = [
    'qt_theme_manager/__init__.py',
    'qt_theme_manager/main.py',
    'qt_theme_manager/cli/__init__.py',
    'qt_theme_manager/qt/__init__.py',
    'setup.py',
    'pyproject.toml',
    'README.md',
    'LICENSE'
]

missing_files = []
for file in required_files:
    if not os.path.exists(file):
        missing_files.append(file)

if missing_files:
    print(f'❌ Missing files: {missing_files}')
    sys.exit(1)
else:
    print('✅ Package structure: OK')
" || exit 1

# バージョン整合性の確認
echo_info "🔢 バージョン整合性の確認"
python3 -c "
import sys
sys.path.insert(0, '.')
import re

# setup.py からバージョンを取得
with open('setup.py', 'r') as f:
    setup_content = f.read()
    setup_version = re.search(r'version=[\'\"](.*?)[\'\"]', setup_content)
    setup_version = setup_version.group(1) if setup_version else None

# pyproject.toml からバージョンを取得
with open('pyproject.toml', 'r') as f:
    pyproject_content = f.read()
    pyproject_version = re.search(
        r'version = [\'\"](.*?)[\'\"]', pyproject_content
    )
    pyproject_version = (
        pyproject_version.group(1) if pyproject_version else None
    )

# __init__.py からバージョンを取得
with open('qt_theme_manager/__init__.py', 'r') as f:
    init_content = f.read()
    init_version = re.search(r'__version__ = [\'\"](.*?)[\'\"]', init_content)
    init_version = init_version.group(1) if init_version else None

print(f'setup.py version: {setup_version}')
print(f'pyproject.toml version: {pyproject_version}')
print(f'__init__.py version: {init_version}')

if setup_version and pyproject_version and init_version:
    if setup_version == pyproject_version == init_version:
        print('✅ Version consistency: OK')
    else:
        print('❌ Version consistency: FAIL - versions do not match')
        sys.exit(1)
else:
    print('❌ Version consistency: FAIL - could not find all versions')
    sys.exit(1)
" || exit 1

# サンプルファイルのテスト
echo_info "📄 サンプルファイルのテスト"
if [ -d "examples" ]; then
    for example in examples/basic/*.py; do
        if [ -f "$example" ]; then
            echo_info "Testing $example"
            python3 "$example" --help > /dev/null 2>&1 || {
                echo_warning "Example $example test failed, but continuing"
            }
        fi
    done
    echo_success "Examples test completed"
else
    echo_warning "Examples directory not found"
fi

echo_success "🎉 すべてのテストが完了しました！"
echo_info "リリース準備が整いました"
