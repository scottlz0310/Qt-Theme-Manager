#!/usr/bin/env python3
"""
ThemeManager CLI main entry point
"""

import sys
from .themectl import main as themectl_main

def main():
    """Main entry point for theme-manager CLI command"""
    try:
        return themectl_main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
