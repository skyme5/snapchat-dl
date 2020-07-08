#!/usr/bin/env python
"""The setup script."""
from setuptools import find_packages
from setuptools import setup


version = {}
with open("snapchat_dl/version.py") as fp:
    exec(fp.read(), version)

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = list()

with open("requirements.txt", "r") as file:
    requirements = [r for r in file.readlines() if len(r) > 0]

test_requirements = ["pytest"].extend(requirements)

setup(
    name="snapchat-dl",
    version=version["__version__"],
    description="Snapchat Public Stories Downloader.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/skyme5/snapchat-dl",
    author="Aakash Gajjar",
    author_email="skyqutip@gmail.com",
    entry_points={"console_scripts": ["snapchat-dl=snapchat_dl.cli:main",],},
    include_package_data=True,
    install_requires=requirements,
    test_suite="tests",
    tests_require=test_requirements,
    python_requires=">=3.5",
    keywords="snapchat-dl",
    license="MIT license",
    packages=find_packages(include=["snapchat_dl", "snapchat_dl.*"]),
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
