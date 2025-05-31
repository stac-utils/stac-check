"""stac-check setup.py
"""

from setuptools import find_packages, setup

__version__ = "1.7.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stac_check",
    version=__version__,
    description="Linting and validation tool for STAC assets",
    url="https://github.com/stac-utils/stac-check",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    setup_requires=["setuptools"],
    install_requires=[
        "requests>=2.32.3",
        "jsonschema>=4.23.0",
        "click>=8.1.8",
        "stac-validator[pydantic]>=3.7.0",
        "PyYAML",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest",
            "requests-mock",
            "types-setuptools",
        ],
    },
    entry_points={"console_scripts": ["stac-check=stac_check.cli:main"]},
    author="Jonathan Healy",
    author_email="jonathan.d.healy@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    tests_require=["pytest"],
)
