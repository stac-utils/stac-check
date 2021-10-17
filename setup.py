"""stac-check setup.py
"""
from setuptools import setup, find_packages

setup(
    name="stac_check",
    version="0.1.0",
    description="Linting and validation tool for STAC assets",
    url="https://github.com/jonhealy1/stac-check",
    packages=find_packages(),
    install_requires=[
        "click",
        "stac_validator==2.3.0"
    ],
    dependency_links=[
        "https://test.pypi.org/simple/"
    ],
    entry_points={
        'console_scripts': ['stac_check=stac_check.cli:main']
    },
    author="Jonathan Healy",
    license="MIT"
)