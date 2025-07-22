from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qt-theme-manager",
    version="0.2.3",
    author="scottlz0310",
    author_email="scott.lz0310@gmail.com",
    description="A comprehensive theme management library for PyQt5/PyQt6/PySide6 applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scottlz0310/Qt-Theme-Manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Desktop Environment",
    ],
    python_requires=">=3.9",
    install_requires=[
        # Base requirements (no Qt framework by default)
    ],
    extras_require={
        "pyqt5": ["PyQt5>=5.15.0"],
        "pyqt6": ["PyQt6>=6.2.0"],
        "pyside6": ["PySide6>=6.0.0"],
        "dev": [
            "pytest>=6.0",
            "pytest-qt>=4.0",
            "black",
            "isort", 
            "flake8",
        ],
        "all": [
            "PyQt5>=5.15.0",
            "PyQt6>=6.2.0", 
            "PySide6>=6.0.0",
        ],
    },
    include_package_data=True,
    package_data={
        "theme_manager": ["config/*.json"],
    },
    entry_points={
        "console_scripts": [
            "theme-manager=theme_manager.cli.main:main",
            "theme-editor=theme_manager.qt.theme_editor:launch_theme_editor",
            "theme-preview=theme_manager.qt.preview:launch_preview",
        ],
    },
)
