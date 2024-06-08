#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="tochd",
    version="0.13",
    description="Convert game ISO and archives to CD/DVD CHD for emulation on Linux",
    author="Tuncay",
    author_email="",
    url="https://github.com/thingsiplay/tochd/",
    packages=find_packages(),
    scripts=["tochd.py"],
)
