"""
CLI module for theme management.
Provides command-line interface for theme operations.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Union

# Add parent directory to path for imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from qt.controller import ThemeController
from qt.loader import ThemeLoader


class ThemeCLI:
    """Command-line interface for theme management."""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize ThemeCLI.
        
        Args:
            config_path: Path to theme configuration file
        """
        self.controller = ThemeController(config_path)
        self.loader = ThemeLoader(config_path)
    
    def list_themes(self) -> None:
        """List all available themes."""
        try:
            themes = self.controller.get_available_themes()
            current_theme = self.controller.get_current_theme_name()
            
            print("Available themes:")
            print("-" * 50)
            
            for theme_name, theme_config in themes.items():
                display_name = theme_config.get("display_name", theme_name)
                description = theme_config.get("description", "No description")
                
                marker = " (current)" if theme_name == current_theme else ""
                print(f"  {theme_name}{marker}")
                print(f"    Display Name: {display_name}")
                print(f"    Description: {description}")
                print()
                
        except Exception as e:
            print(f"Error listing themes: {e}")
            sys.exit(1)
    
    def set_theme(self, theme_name: str) -> None:
        """
        Set active theme.
        
        Args:
            theme_name: Name of theme to activate
        """
        try:
            success = self.controller.set_theme(theme_name)
            
            if success:
                print(f"Theme set to '{theme_name}'")
            else:
                print(f"Failed to set theme to '{theme_name}'")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error setting theme: {e}")
            sys.exit(1)
    
    def export_qss(self, theme_name: str, output_path: str) -> None:
        """
        Export QSS stylesheet to file.
        
        Args:
            theme_name: Name of theme to export
            output_path: Path to output file
        """
        try:
            success = self.controller.export_qss(output_path, theme_name)
            
            if success:
                print(f"QSS exported to '{output_path}'")
            else:
                print(f"Failed to export QSS")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error exporting QSS: {e}")
            sys.exit(1)
    
    def show_current(self) -> None:
        """Show current theme information."""
        try:
            current_theme = self.controller.get_current_theme_name()
            themes = self.controller.get_available_themes()
            
            if current_theme in themes:
                theme_config = themes[current_theme]
                display_name = theme_config.get("display_name", current_theme)
                description = theme_config.get("description", "No description")
                
                print(f"Current theme: {current_theme}")
                print(f"Display Name: {display_name}")
                print(f"Description: {description}")
                
                # Show color palette
                print("\nColor Palette:")
                print(f"  Background: {theme_config.get('backgroundColor', 'N/A')}")
                print(f"  Text: {theme_config.get('textColor', 'N/A')}")
                print(f"  Primary: {theme_config.get('primaryColor', 'N/A')}")
                print(f"  Accent: {theme_config.get('accentColor', 'N/A')}")
            else:
                print(f"Current theme '{current_theme}' not found in configuration")
                
        except Exception as e:
            print(f"Error showing current theme: {e}")
            sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ThemeManager CLI - Manage PyQt5/PySide6 application themes",
        prog="themectl"
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to theme configuration file"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    subparsers.add_parser("list", help="List all available themes")
    
    # Set command
    set_parser = subparsers.add_parser("set", help="Set active theme")
    set_parser.add_argument("theme", help="Theme name to activate")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export theme QSS to file")
    export_parser.add_argument("theme", help="Theme name to export")
    export_parser.add_argument("output", help="Output file path")
    
    # Current command
    subparsers.add_parser("current", help="Show current theme information")
    
    # Editor command
    subparsers.add_parser("editor", help="Launch advanced theme editor (GUI)")
    
    # Version command
    subparsers.add_parser("version", help="Show version information")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "version":
        print("ThemeManager CLI v0.0.1")
        print("PyQt5/PySide6 Theme Management Library")
        return
    
    if args.command == "editor":
        print("Starting advanced theme editor...")
        print("注意: この機能にはPyQt5/PyQt6/PySide6が必要です。")
        try:
            from ..qt.theme_editor import launch_theme_editor
            editor = launch_theme_editor(args.config)
            
            if editor is not None:
                from ..qt.theme_editor import qt_available
                if qt_available:
                    try:
                        from PyQt5.QtWidgets import QApplication
                    except ImportError:
                        try:
                            from PyQt6.QtWidgets import QApplication  
                        except ImportError:
                            from PySide6.QtWidgets import QApplication
                    
                    app = QApplication.instance()
                    if app is not None:
                        print("🚀 テーマエディターが起動しました！")
                        sys.exit(app.exec_() if hasattr(app, 'exec_') else app.exec())
        except ImportError as e:
            print(f"❌ テーマエディターの起動に失敗: {e}")
            print("必要な依存関係をインストールしてください:")
            print("  pip install PyQt6  # または PyQt5, PySide6")
            sys.exit(1)
        return
    
    # Initialize CLI with config path
    cli = ThemeCLI(args.config)
    
    # Execute command
    if args.command == "list":
        cli.list_themes()
    elif args.command == "set":
        cli.set_theme(args.theme)
    elif args.command == "export":
        cli.export_qss(args.theme, args.output)
    elif args.command == "current":
        cli.show_current()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
