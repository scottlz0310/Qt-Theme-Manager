# 設計ドキュメント

## 概要

Qt-Theme-Managerライブラリ単独化プロジェクトは、現在のモノリシックな構造から純粋なライブラリアーキテクチャへの移行を実現します。この設計では、コアライブラリ機能を`qt_theme_manager/`パッケージに集約し、GUI関連ツールを`migrate/`フォルダに分離して、後にqt-theme-studioリポジトリへの手動移行を可能にします。

## アーキテクチャ

### 現在の構造
```
qt-theme-manager/
├── theme_manager/          # 現在のコアパッケージ
│   ├── __init__.py
│   ├── main.py
│   ├── cli/               # CLI機能
│   ├── qt/                # Qt統合
│   └── config/            # 設定管理
├── launch_*.py            # GUI起動スクリプト（移行対象）
├── *_editor.py           # エディタ関連（移行対象）
├── examples/             # サンプル（移行対象）
├── scripts/              # ユーティリティ（移行対象）
└── utils/                # ヘルパー（移行対象）
```

### 目標構造
```
qt-theme-manager/
├── qt_theme_manager/      # 新しいコアパッケージ名
│   ├── __init__.py       # パブリックAPI
│   ├── main.py           # エントリーポイント（CLI専用）
│   ├── cli/              # コマンドライン機能
│   ├── qt/               # Qt統合モジュール
│   └── config/           # 設定ファイル処理
├── migrate/              # 移行用フォルダ
│   ├── launch_*.py       # GUI起動スクリプト
│   ├── *_editor.py       # エディタ関連
│   ├── examples/         # サンプルコード
│   ├── scripts/          # ユーティリティスクリプト
│   └── utils/            # ヘルパーモジュール
├── pyproject.toml        # ライブラリ専用設定
├── setup.py              # パッケージング設定
├── MANIFEST.in           # 配布ファイル設定
└── README.md             # ライブラリドキュメント
```

## コンポーネントと インターフェース

### 1. コアライブラリパッケージ (`qt_theme_manager/`)

#### 1.1 パブリックAPI (`__init__.py`)
- **目的**: ライブラリの主要機能を外部に公開
- **主要エクスポート**:
  - `ThemeController`: テーマ制御の中心クラス
  - `apply_theme_to_widget`: ウィジェット適用関数
  - `ThemeLoader`: テーマ読み込み機能
  - `StylesheetGenerator`: スタイルシート生成
- **後方互換性**: 既存のインポートパスを完全に維持

#### 1.2 Qt統合モジュール (`qt/`)
- **controller.py**: テーマ制御ロジック
- **loader.py**: テーマファイル読み込み
- **stylesheet.py**: スタイルシート生成
- **advanced_stylesheet.py**: 高度なスタイル機能
- **preview.py**: プレビュー機能（ライブラリ用）

#### 1.3 CLI機能 (`cli/`)
- **main.py**: CLIエントリーポイント
- **themectl.py**: テーマ制御コマンド
- **機能**: ライブラリとしてのCLI操作のみ

#### 1.4 設定管理 (`config/`)
- **theme_settings.json**: デフォルト設定
- **設定読み込み・保存機能**

### 2. Qt自動検出システム

#### 2.1 検出順序
```python
# 優先順位: PySide6 → PyQt6 → PyQt5
try:
    from PySide6.QtWidgets import QApplication
    QT_FRAMEWORK = "PySide6"
except ImportError:
    try:
        from PyQt6.QtWidgets import QApplication
        QT_FRAMEWORK = "PyQt6"
    except ImportError:
        try:
            from PyQt5.QtWidgets import QApplication
            QT_FRAMEWORK = "PyQt5"
        except ImportError:
            QT_FRAMEWORK = None
```

#### 2.2 エラーハンドリング
- **フレームワーク未検出時**: 明確なエラーメッセージと推奨インストール方法
- **バージョン互換性**: 各フレームワークの最小バージョン要件チェック
- **実行時検証**: インポート時の動的検証

### 3. 移行システム

#### 3.1 ファイル移行戦略
```python
MIGRATION_MAP = {
    # GUI起動スクリプト
    "launch_theme_editor.py": "migrate/launch_theme_editor.py",
    "launch_zebra_theme_editor.py": "migrate/launch_zebra_theme_editor.py",
    "launch_gui_preview.py": "migrate/launch_gui_preview.py",

    # エディタ関連
    "theme_editor_zebra_extension.py": "migrate/theme_editor_zebra_extension.py",
    "zebra_pattern_editor.py": "migrate/zebra_pattern_editor.py",
    "analyze_zebra_colors.py": "migrate/analyze_zebra_colors.py",
    "improve_zebra_colors.py": "migrate/improve_zebra_colors.py",

    # ディレクトリ
    "examples/": "migrate/examples/",
    "scripts/": "migrate/scripts/",
    "utils/": "migrate/utils/"
}
```

#### 3.2 構造保持
- **元の階層維持**: `migrate/`内で元のディレクトリ構造を保持
- **相対パス保持**: ファイル間の相対参照を維持
- **メタデータ保持**: ファイル権限・タイムスタンプの保持

## データモデル

### 1. テーマ設定モデル
```python
@dataclass
class ThemeConfig:
    name: str
    version: str
    colors: Dict[str, str]
    fonts: Dict[str, str]
    styles: Dict[str, str]
    metadata: Dict[str, Any]
```

### 2. ライブラリ設定モデル
```python
@dataclass
class LibraryConfig:
    qt_framework: Optional[str]
    theme_directory: Path
    cache_enabled: bool
    log_level: str
```

### 3. 移行状態モデル
```python
@dataclass
class MigrationStatus:
    files_moved: List[str]
    directories_moved: List[str]
    errors: List[str]
    completed: bool
```

## エラーハンドリング

### 1. Qt検出エラー
```python
class QtFrameworkNotFoundError(ImportError):
    """Qt framework not found error with installation guidance."""

    def __init__(self):
        message = (
            "No Qt framework found. Please install one of:\n"
            "  pip install PySide6  # Recommended\n"
            "  pip install PyQt6\n"
            "  pip install PyQt5"
        )
        super().__init__(message)
```

### 2. 移行エラー
```python
class MigrationError(Exception):
    """File migration error with detailed context."""

    def __init__(self, source: str, destination: str, reason: str):
        message = f"Failed to migrate {source} to {destination}: {reason}"
        super().__init__(message)
```

### 3. 設定エラー
```python
class ConfigurationError(Exception):
    """Configuration loading/saving error."""
    pass
```

## テスト戦略

### 1. 単体テスト
- **カバレッジ目標**: 95%以上
- **テスト対象**:
  - Qt自動検出機能
  - テーマ読み込み・適用
  - CLI機能
  - 設定管理
  - エラーハンドリング

### 2. 統合テスト
- **API互換性テスト**: 既存のパブリックAPIの動作確認
- **クロスプラットフォームテスト**: Windows/macOS/Linux
- **Qtフレームワーク互換性**: PySide6/PyQt6/PyQt5

### 3. 移行テスト
- **ファイル移行テスト**: 正確な移動と構造保持
- **完全性テスト**: 移行後のファイル整合性
- **ロールバックテスト**: 移行失敗時の復旧

## パフォーマンス考慮事項

### 1. インポート時間最適化
- **遅延インポート**: Qt関連モジュールの必要時読み込み
- **キャッシュ機能**: テーマファイルの効率的なキャッシュ
- **メモリ使用量**: 不要なモジュールの読み込み回避

### 2. ファイルI/O最適化
- **バッチ処理**: 複数ファイルの効率的な移行
- **並列処理**: 可能な場合の並列ファイル操作
- **プログレス表示**: 長時間操作の進捗表示

## セキュリティ考慮事項

### 1. ファイル操作セキュリティ
- **パス検証**: ディレクトリトラバーサル攻撃の防止
- **権限チェック**: ファイル操作権限の事前確認
- **安全な移行**: 原子的ファイル操作の実装

### 2. 設定ファイルセキュリティ
- **入力検証**: 設定値の妥当性チェック
- **デフォルト値**: 安全なデフォルト設定
- **エラー情報**: 機密情報の漏洩防止

## 配布とパッケージング

### 1. PyPI配布設定
```toml
[project]
name = "qt-theme-manager"
version = "1.0.0"
description = "A comprehensive theme management library for PyQt5/PyQt6/PySide6 applications"
dependencies = []  # Qt自動検出のため基本依存なし

[project.optional-dependencies]
pyqt5 = ["PyQt5>=5.15.0"]
pyqt6 = ["PyQt6>=6.2.0"]
pyside6 = ["PySide6>=6.0.0"]
dev = ["pytest>=6.0", "pytest-qt>=4.0", "black", "isort", "flake8"]
```

### 2. エントリーポイント
```toml
[project.scripts]
qt-theme-manager = "qt_theme_manager.cli.main:main"
```

### 3. パッケージデータ
```toml
[tool.setuptools.package-data]
qt_theme_manager = ["config/*.json"]
```

## 実装フェーズ

### フェーズ1: 移行準備（1週間）
1. **ファイル移行システム実装**
2. **パッケージ名変更対応**
3. **テスト環境構築**

### フェーズ2: コード品質向上（3日）
1. **PEP 8準拠**
2. **型ヒント追加**
3. **docstring整備**
4. **ログ出力改善**

### フェーズ3: ドキュメント更新（2日）
1. **README更新**
2. **API仕様書更新**
3. **インストールガイド更新**

### フェーズ4: パッケージング最適化（1日）
1. **pyproject.toml更新**
2. **setup.py最適化**
3. **MANIFEST.in調整**

## 成功指標

### 定量的指標
- **コードサイズ**: 30%削減
- **テストカバレッジ**: 95%以上
- **インポート時間**: 現在の速度維持
- **メモリ使用量**: 20%削減

### 定性的指標
- **API互換性**: 100%後方互換
- **ドキュメント品質**: 完全性と明確性
- **コード品質**: PEP 8準拠
- **保守性**: モジュラー設計の実現
