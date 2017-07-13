#!/usr/bin/env python3

from setuptools import setup

requirements = [
    'pulpcore-plugin',
]

setup(
    name='pulp-file',
    version='0.0.1a1.dev1',
    description='File plugin for the Pulp Project',
    author='Pulp Project Developers',
    author_email='pulp-dev@redhat.com',
    url='http://www.pulpproject.org/',
    install_requires=requirements,
    include_package_data=True,
    packages=['pulp_file'],
    entry_points={
        'pulpcore.plugin': [
            'pulp_file = pulp_file:default_app_config',
        ]
    }
)
