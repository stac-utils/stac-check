"""stac-check setup.py
"""
from setuptools import setup, find_packages

setup(
    name="stac-check",
    version="0.1.0",
    description="Linting and validation tool for STAC assets",
    url="https://github.com/jonhealy1/stac-check",
    packages=find_packages(),
    install_requires=[
        "click"
    ],
    entry_points={
        'console_scripts': ['stac-check=stac-check.main:main']
    },
    author="Jonathan Healy",
    license="MIT"
)