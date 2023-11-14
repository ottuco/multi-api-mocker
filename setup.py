#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md") as history_file:
    history = history_file.read()

requirements = ["requests_mock>=1.9.3"]

test_requirements = [
    "pytest>=3",
    "requests_mock>=1.9.3",
]

setup(
    author="Dacian Popute",
    author_email="dacian@ottu.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="A Python library for generating mock API responses for testing.",
    long_description_content_type="text/markdown",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="multi_api_mocker",
    name="multi_api_mocker",
    packages=find_packages(include=["multi_api_mocker", "multi_api_mocker.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/ottuco/multi_api_mocker",
    version="1.0.0",
    zip_safe=False,
)
