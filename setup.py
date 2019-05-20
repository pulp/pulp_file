#!/usr/bin/env python3

from setuptools import setup, find_packages

requirements = [
    'pulpcore-plugin~=0.1rc2',
]

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='pulp-file',
    version='0.0.1b11',
    description='File plugin for the Pulp Project',
    long_description=long_description,
    license='GPLv2+',
    author='Pulp Project Developers',
    author_email='pulp-dev@redhat.com',
    url='http://www.pulpproject.org/',
    python_requires='>=3.6',
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(exclude=['test']),
    classifiers=(
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
    entry_points={
        'pulpcore.plugin': [
            'pulp_file = pulp_file:default_app_config',
        ]
    }
)
