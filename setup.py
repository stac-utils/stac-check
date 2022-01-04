"""stac-check setup.py
"""
from setuptools import setup

__version__ = "0.1.12"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stac-check",
    version=__version__,
    description="Linting and validation tool for STAC assets",
    url="https://github.com/jonhealy1/stac-check",
    packages=["stac_check"],
    install_requires=[
        "click>=7.1.2",
        "pystac==1.1.0",
        "jsonschema",
        "pytest>=6.0.0",
        "jsonpointer",
        "importlib-metadata"
    ],
    entry_points={
        'console_scripts': ['stac_check=stac_check.cli:main']
    },
    author="Jonathan Healy",
    author_email="jonatham.d.healy@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    tests_require=["pytest"]
)