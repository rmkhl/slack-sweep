# -*- coding: utf-8 -*-
# Copyright © 2021, RMK HAKLAB RY
"""
Setup for slacksweep module
"""
import datetime
import os
from setuptools import setup, find_packages

setup(
    name='slacksweep',
    version='{}.{}'.format(
        datetime.datetime.now().strftime('%Y.%m'),
        os.environ.get('PKG_REVISION', 0)
    ),
    install_requires=[
        "dateparser",
        "slack_sdk",
    ],
    entry_points={
        'console_scripts': [
            'slacksweep = slacksweep.__main__:main',
        ],
    },
    packages=find_packages(exclude=['tests']),
)
