#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.rst") as f:
    long_description = f.read()

with open("requirements.txt") as requirements:
    requirements = requirements.readlines()

setup(
    name="pulp-file",
    version="1.9.0",
    description="File plugin for the Pulp Project",
    long_description=long_description,
    license="GPLv2+",
    author="Pulp Project Developers",
    author_email="pulp-dev@redhat.com",
    url="https://pulpproject.org/",
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(exclude=["test"]),
    classifiers=(
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ),
    entry_points={"pulpcore.plugin": ["pulp_file = pulp_file:default_app_config"]},
)
