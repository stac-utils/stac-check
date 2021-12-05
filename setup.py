"""stac-check setup.py
"""
from setuptools import setup, find_packages

__version__ = "0.1.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stac_check",
    version=__version__,
    description="Linting and validation tool for STAC assets",
    url="https://github.com/jonhealy1/stac-check",
    packages=find_packages(),
    install_requires=[
        "click",
        "pystac[validation]==1.1.0"
    ],
    entry_points={
        'console_scripts': ['stac_check=stac_check.cli:main']
    },
    author="Jonathan Healy",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/jonhealy1/stac-check/archive/refs/tags/v0.1.0.tar.gz",
    python_requires=">=3.7",
    tests_require=["pytest"]
)