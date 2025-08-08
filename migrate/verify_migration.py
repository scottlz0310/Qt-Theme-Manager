#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI関連ファイル移行検証スクリプト
移行対象ファイルの完全性と構造保持を確認します
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple


class MigrationVerifier:
    """移行状況の検証を行うクラス"""
    
    def __init__(self):
        self.migrate_dir = Path(__file__).parent
        self.root_dir = self.migrate_dir.parent
        
        # 移行対象ファイルリスト
        self.target_files = [
            "launch_theme_editor.py",
            "launch_zebra_theme_editor.py", 
            "launch_gui_preview.py",
            "theme_editor_zebra_extension.py",
            "zebra_pattern_editor.py",
            "analyze_zebra_colors.py",
            "improve_zebra_colors.py"
        ]
        
        # 移行対象ディレクトリ
        self.target_directories = [
            "examples",
            "scripts", 
            "utils"
        ]
    
    def verify_file_migration(self) -> Tuple[List[str], List[str]]:
        """ファイル移行の検証"""
        migrated_files = []
        missing_files = []
        
        for file_name in self.target_files:
            migrate_path = self.migrate_dir / file_name
            root_path = self.root_dir / file_name
            
            if migrate_path.exists():
                migrated_files.append(file_name)
                # ルートディレクトリに残っていないかチェック
                if root_path.exists():
                    print(f"警告: {file_name} がルートディレクトリにも存在します")
            else:
                missing_files.append(file_name)
        
        return migrated_files, missing_files
    
    def verify_directory_migration(self) -> Tuple[List[str], List[str]]:
        """ディレクトリ移行の検証"""
        migrated_dirs = []
        missing_dirs = []
        
        for dir_name in self.target_directories:
            migrate_path = self.migrate_dir / dir_name
            root_path = self.root_dir / dir_name
            
            if migrate_path.exists() and migrate_path.is_dir():
                migrated_dirs.append(dir_name)
                # ルートディレクトリに残っていないかチェック
                if root_path.exists():
                    print(f"警告: {dir_name} がルートディレクトリにも存在します")
            else:
                missing_dirs.append(dir_name)
        
        return migrated_dirs, missing_dirs
    
    def verify_structure_integrity(self) -> Dict[str, bool]:
        """構造の整合性検証"""
        integrity_results = {}
        
        # examples ディレクトリの構造確認
        examples_dir = self.migrate_dir / "examples"
        if examples_dir.exists():
            integrity_results["examples_structure"] = (
                (examples_dir / "README.md").exists() and
                (examples_dir / "basic").exists() and
                (examples_dir / "advanced").exists() and
                (examples_dir / "integration").exists()
            )
        else:
            integrity_results["examples_structure"] = False
        
        # scripts ディレクトリの構造確認
        scripts_dir = self.migrate_dir / "scripts"
        if scripts_dir.exists():
            integrity_results["scripts_structure"] = (
                (scripts_dir / "test_qt_framework.py").exists()
            )
        else:
            integrity_results["scripts_structure"] = False
        
        # utils ディレクトリの構造確認
        utils_dir = self.migrate_dir / "utils"
        if utils_dir.exists():
            integrity_results["utils_structure"] = (
                (utils_dir / "setup.py").exists()
            )
        else:
            integrity_results["utils_structure"] = False
        
        return integrity_results
    
    def generate_report(self) -> str:
        """移行検証レポートの生成"""
        migrated_files, missing_files = self.verify_file_migration()
        migrated_dirs, missing_dirs = self.verify_directory_migration()
        integrity_results = self.verify_structure_integrity()
        
        report = []
        report.append("=== GUI関連ファイル移行検証レポート ===\n")
        
        # ファイル移行状況
        report.append("【ファイル移行状況】")
        report.append(f"移行完了: {len(migrated_files)}/{len(self.target_files)}")
        for file_name in migrated_files:
            report.append(f"  ✓ {file_name}")
        
        if missing_files:
            report.append("\n未移行ファイル:")
            for file_name in missing_files:
                report.append(f"  ✗ {file_name}")
        
        # ディレクトリ移行状況
        report.append(f"\n【ディレクトリ移行状況】")
        report.append(f"移行完了: {len(migrated_dirs)}/{len(self.target_directories)}")
        for dir_name in migrated_dirs:
            report.append(f"  ✓ {dir_name}/")
        
        if missing_dirs:
            report.append("\n未移行ディレクトリ:")
            for dir_name in missing_dirs:
                report.append(f"  ✗ {dir_name}/")
        
        # 構造整合性
        report.append(f"\n【構造整合性】")
        for key, result in integrity_results.items():
            status = "✓" if result else "✗"
            report.append(f"  {status} {key}")
        
        # 総合判定
        all_files_migrated = len(missing_files) == 0
        all_dirs_migrated = len(missing_dirs) == 0
        all_structures_intact = all(integrity_results.values())
        
        report.append(f"\n【総合判定】")
        if all_files_migrated and all_dirs_migrated and all_structures_intact:
            report.append("✓ 移行完了 - すべてのファイルとディレクトリが正常に移行されました")
        else:
            report.append("✗ 移行未完了 - 上記の問題を解決してください")
        
        return "\n".join(report)


def main():
    """メイン実行関数"""
    verifier = MigrationVerifier()
    report = verifier.generate_report()
    print(report)
    
    # レポートをファイルに保存
    report_file = Path(__file__).parent / "migration_verification_report.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n詳細レポートが {report_file} に保存されました。")


if __name__ == "__main__":
    main()