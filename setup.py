"""Setup.py module for the aac-doc-mdl plugin."""

# NOTE: It is safe to edit this file.
# This file is only initially generated by aac gen-project, and it won't be overwritten if the file already exists.

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    readme_description = fh.read()

runtime_dependencies = [
    "aac ~= 0.4.11",
    "openai ~= 1.30.5",
    "pydantic ~= 2.8.2"
]

test_dependencies = [
    "nose2 ~= 0.10.0",
    "coverage ~= 6.0",
    "flake8 ~= 4.0",
    "flake8-docstrings ~= 1.6.0",
    "flake8-fixme ~= 1.1.1",
    "flake8-eradicate ~= 1.2.0",
    "flake8-assertive ~= 1.3.0",
]

setup(
    version="0.0.1",
    name="aac-doc-mdl",
    packages=find_packages(where=".", exclude="tests"),
    package_data={"": ["*.aac", "*.jinja2", "*.yaml"]},
    install_requires=runtime_dependencies,
    extras_require={"test": test_dependencies},
    entry_points={
        "aac": ["aac-doc-mdl=aac_doc_mdl"],
    },
)
