import os
import shutil
import subprocess
from pathlib import Path

def setup_theme_manager_project(project_name="theme_manager_project"):
    # Define paths
    base_dir = Path.cwd() / project_name
    venv_dir = base_dir / "venv"
    config_dir = base_dir / "theme_manager" / "config"
    template_path = Path.cwd() / "config_template" / "theme_settings.json"
    destination_path = config_dir / "theme_settings.json"

    # Create base directory structure
    print(f"Creating project directory at: {base_dir}")
    config_dir.mkdir(parents=True, exist_ok=True)

    # Create virtual environment
    print(f"Creating virtual environment at: {venv_dir}")
    subprocess.run(["python", "-m", "venv", str(venv_dir)], check=True)

    # Copy theme_settings.json template
    if template_path.exists():
        print(f"Copying template from {template_path} to {destination_path}")
        shutil.copy(template_path, destination_path)
    else:
        print(f"Template file not found at {template_path}")

    print("Project setup complete.")

# Run the setup
setup_theme_manager_project()

