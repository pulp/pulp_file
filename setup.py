#!/usr/bin/env python3

from setuptools import setup

setup(
    name='pulp_file',
    version='0.0.0',
    description='File plugin for the Pulp Project',
    author='Pulp Project Developers',
    author_email='pulp-dev@redhat.com',
    url='http://www.pulpproject.org/',
    packages=['pulp_file'],
    entry_points={
        'pulp.plugin': [
            'pulp_file = pulp_file:default_app_config',
        ]
    }
)
