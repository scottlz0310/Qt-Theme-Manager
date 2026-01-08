from setuptools import setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qt-theme-manager",
    version="1.0.1",
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
        "Documentation": "https://github.com/scottlz0310/Qt-Theme-Manager/"
        "blob/main/README.md",
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
        "Development Status :: 5 - Production/Stable",
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
        "pyqt5": ["PyQt5>=5.15.11"],
        "pyqt6": ["PyQt6>=6.10.2"],
        "pyside6": ["PySide6>=6.10.1"],
        "dev": [
            "pytest>=9.0.2",
            "pytest-qt>=4.5.0",
            "pytest-cov>=7.0.0",
            "black>=25.12.0",
            "isort>=7.0.0",
            "flake8>=7.3.0",
            "basedpyright>=1.37.1",
        ],
        "all": [
            "PyQt5>=5.15.11",
            "PyQt6>=6.10.2",
            "PySide6>=6.10.1",
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
