#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='bmp280',
    version='0.0.1',
    description='bmp280 driver',
    author='Blue Robotics',
    url='https://github.com/bluerobotics/bmp280-python',
    packages=['bmp280'],
    install_requires=['smbus2'],
)
