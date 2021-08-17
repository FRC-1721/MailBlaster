#!/usr/bin/env python

# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages

readme = open('README.md').read()

setup(
    name='email-blaster',
    description='A simple tool to forward and email to discord as a blast!',
    author='1721 Tidal Force',
    author_email='concordroboticssteam@gmail.com',
    url='https://github.com/FRC-1721/MailBlaster',
    packages=find_packages(include=['mail_blaster']),
    package_dir={'mail-blaster': 'mail_blaster'},
    entry_points={
        'console_scripts': [
            'mail-blaster=mail_blaster.__main__:main',
        ],
    },

    python_requires='>=3.6.0',
    version='0.0.0',
    long_description=readme,
    include_package_data=True,
    install_requires=[
        'schedule',
    ],
    license='MIT',
)
