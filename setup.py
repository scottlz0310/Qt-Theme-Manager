from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qt-theme-manager",
    version="0.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive theme management library for PyQt5/PySide6 applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/Theme-Manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Qt framework (user choice)
        # "PyQt5>=5.12.0",  # or
        # "PySide6>=6.0.0",
    ],
    extras_require={
        "pyqt5": ["PyQt5>=5.12.0"],
        "pyside6": ["PySide6>=6.0.0"],
        "dev": [
            "pytest>=6.0",
            "pytest-qt>=4.0",
        ],
    },
    include_package_data=True,
    package_data={
        "theme_manager": ["config/*.json"],
    },
    entry_points={
        "console_scripts": [
            "theme-manager=theme_manager.cli.main:main",
        ],
    },
)
