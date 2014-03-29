#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='Tron',
    version='1.0',
    description='Cloud Sherpas Builder and Deployer',
    author='Jon Wayne Parrott',
    author_email='jonathan.parrott@cloudsherpas.com',
    url='http://bitbucket.org/cloudsherpas',
    packages=find_packages(),
    install_requires=['distribute', 'jinja2', 'gitpython >= 0.3.2.RC1', 'httplib2', 'appdirs', 'requests'],
    entry_points={
        'console_scripts': [
            'tron = tronlib.cmd:main'
        ]
    }
)
