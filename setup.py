# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in trading/__init__.py
from trading import __version__ as version

setup(
	name='trading',
	version=version,
	description='Trading',
	author='Craft',
	author_email='test@test.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
