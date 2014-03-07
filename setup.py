# -*- coding: utf-8 -*-
'''
Copyright 2012 Rodrigo Pinheiro Matias <rodrigopmatias@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from setuptools import setup, find_packages

import sketchduino

setup(
    name="sketchduino",
    description=" Arduino Sketch Generator",
    long_description=open('README.rst').read(),
    version=sketchduino.__version__,
    install_requires=[
        'argparse',
        'pyserial'
    ],
    license='Apache 2.0',
    author='Rodrigo Pinheiro Matias',
    author_email='rodrigopmatias@gmail.com',
    platforms='GNU/Linux',
    include_package_data=True,
    packages=['sketchduino'],
    entry_points={
        'console_scripts': [
            'sketchduino = sketchduino:main'
        ]
    }
)
