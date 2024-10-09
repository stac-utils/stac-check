"""stac-check setup.py
"""

from setuptools import find_packages, setup

__version__ = "1.4.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stac_check",
    version=__version__,
    description="Linting and validation tool for STAC assets",
    url="https://github.com/stac-utils/stac-check",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "requests>=2.19.1",
        "jsonschema>=3.1.2",
        "stac-validator>=3.4.0",
        "PyYAML",
        "python-dotenv",
        "setuptools",
    ],
    extras_require={
        "dev": [
            "pytest",
            "types-setuptools",
        ],
    },
    entry_points={"console_scripts": ["stac-check=stac_check.cli:main"]},
    author="Jonathan Healy",
    author_email="jonathan.d.healy@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    tests_require=["pytest"],
)
