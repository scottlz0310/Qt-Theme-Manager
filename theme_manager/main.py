#!/usr/bin/env python3
"""
Main entry point for ThemeManager CLI.
"""

import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from cli.themectl import main

if __name__ == "__main__":
    main()
