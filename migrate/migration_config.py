#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI関連ファイル移行設定
移行対象ファイルとディレクトリの定義
"""

from pathlib import Path
from typing import Dict, List


class MigrationConfig:
    """移行設定を管理するクラス"""
    
    # 移行対象ファイルのマッピング
    FILE_MIGRATION_MAP: Dict[str, str] = {
        # GUI起動スクリプト
        "launch_theme_editor.py": "migrate/launch_theme_editor.py",
        "launch_zebra_theme_editor.py": "migrate/launch_zebra_theme_editor.py",
        "launch_gui_preview.py": "migrate/launch_gui_preview.py",
        
        # エディタ関連ファイル
        "theme_editor_zebra_extension.py": "migrate/theme_editor_zebra_extension.py",
        "zebra_pattern_editor.py": "migrate/zebra_pattern_editor.py",
        "analyze_zebra_colors.py": "migrate/analyze_zebra_colors.py",
        "improve_zebra_colors.py": "migrate/improve_zebra_colors.py",
    }
    
    # 移行対象ディレクトリのマッピング
    DIRECTORY_MIGRATION_MAP: Dict[str, str] = {
        "examples": "migrate/examples",
        "scripts": "migrate/scripts",
        "utils": "migrate/utils",
    }
    
    # 移行対象ファイルリスト（要件3.1で定義）
    TARGET_FILES: List[str] = [
        "launch_theme_editor.py",
        "launch_zebra_theme_editor.py",
        "launch_gui_preview.py",
        "theme_editor_zebra_extension.py",
        "zebra_pattern_editor.py",
        "analyze_zebra_colors.py",
        "improve_zebra_colors.py",
    ]
    
    # 移行対象ディレクトリリスト（要件3.1で定義）
    TARGET_DIRECTORIES: List[str] = [
        "examples",
        "scripts", 
        "utils",
    ]
    
    @classmethod
    def get_all_migration_targets(cls) -> Dict[str, str]:
        """すべての移行対象のマッピングを取得"""
        all_targets = {}
        all_targets.update(cls.FILE_MIGRATION_MAP)
        all_targets.update(cls.DIRECTORY_MIGRATION_MAP)
        return all_targets
    
    @classmethod
    def validate_migration_targets(cls, base_path: Path) -> Dict[str, bool]:
        """移行対象の存在確認"""
        validation_results = {}
        
        # ファイルの存在確認
        for source_file in cls.TARGET_FILES:
            source_path = base_path / source_file
            migrate_path = base_path / cls.FILE_MIGRATION_MAP[source_file]
            validation_results[source_file] = {
                "source_exists": source_path.exists(),
                "migrated_exists": migrate_path.exists(),
                "migration_complete": not source_path.exists() and migrate_path.exists()
            }
        
        # ディレクトリの存在確認
        for source_dir in cls.TARGET_DIRECTORIES:
            source_path = base_path / source_dir
            migrate_path = base_path / cls.DIRECTORY_MIGRATION_MAP[source_dir]
            validation_results[source_dir] = {
                "source_exists": source_path.exists(),
                "migrated_exists": migrate_path.exists(),
                "migration_complete": not source_path.exists() and migrate_path.exists()
            }
        
        return validation_results
    
    @classmethod
    def get_migration_summary(cls, base_path: Path) -> Dict[str, int]:
        """移行状況のサマリーを取得"""
        validation_results = cls.validate_migration_targets(base_path)
        
        total_targets = len(cls.TARGET_FILES) + len(cls.TARGET_DIRECTORIES)
        completed_migrations = sum(
            1 for result in validation_results.values() 
            if result["migration_complete"]
        )
        
        return {
            "total_targets": total_targets,
            "completed_migrations": completed_migrations,
            "completion_rate": completed_migrations / total_targets if total_targets > 0 else 0
        }


# 移行設定の定数定義
MIGRATION_CONFIG = MigrationConfig()

# 後方互換性のための定数
FILE_MIGRATION_MAP = MigrationConfig.FILE_MIGRATION_MAP
DIRECTORY_MIGRATION_MAP = MigrationConfig.DIRECTORY_MIGRATION_MAP
TARGET_FILES = MigrationConfig.TARGET_FILES
TARGET_DIRECTORIES = MigrationConfig.TARGET_DIRECTORIES