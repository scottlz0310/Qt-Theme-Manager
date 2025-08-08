from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qt-theme-manager",
    version="0.2.4",
    author="scottlz0310",
    author_email="scott.lz0310@gmail.com",
    description=(
        "A comprehensive theme management library for "
        "PyQt5/PyQt6/PySide6 applications with automatic Qt framework "
        "detection"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scottlz0310/Qt-Theme-Manager",
    project_urls={
        "Homepage": "https://github.com/scottlz0310/Qt-Theme-Manager",
        "Documentation": "https://github.com/scottlz0310/Qt-Theme-Manager/blob/main/README.md",
        "Repository": "https://github.com/scottlz0310/Qt-Theme-Manager",
        "Bug Tracker": "https://github.com/scottlz0310/Qt-Theme-Manager/issues",
    },
    packages=[
        "qt_theme_manager",
        "qt_theme_manager.qt",
        "qt_theme_manager.cli",
        "qt_theme_manager.config",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
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
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.9",
    install_requires=[
        # Qt自動検出のため基本依存関係なし
        # ユーザーは必要に応じてQt frameworkをインストール
    ],
    extras_require={
        "pyqt5": ["PyQt5>=5.15.0"],
        "pyqt6": ["PyQt6>=6.2.0"],
        "pyside6": ["PySide6>=6.0.0"],
        "dev": [
            "pytest>=6.0",
            "pytest-qt>=4.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=4.0",
            "mypy>=0.900",
        ],
        "all": [
            "PyQt5>=5.15.0",
            "PyQt6>=6.2.0",
            "PySide6>=6.0.0",
        ],
    },
    include_package_data=True,
    package_data={
        "qt_theme_manager": ["config/*.json"],
    },
    entry_points={
        "console_scripts": [
            "qt-theme-manager=qt_theme_manager.cli.main:main",
        ],
    },
    keywords=[
        "theme",
        "gui",
        "qt",
        "styling",
        "pyside",
        "pyqt",
        "library",
        "ui",
        "desktop",
    ],
    zip_safe=False,
)
