# import modules
import sys

class VersionError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

try:
    from setuptools import setup, find_packages
except ImportError:
    raise("Please install setuptools to run setup.py")

def readme():
    with open('README.md') as f:
        return f.read()

def get_requirements():
    with open('requirements.txt') as f:
        return f.read().split()

setup(
    name='rsgis-scripts',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/dghorai83',
    license='MIT License',
    author='Debabrata Ghorai, Ph.D.',
    author_email='ghoraideb@gmail.com',
    description='Geospatial utilities for Remote Sensing and GIS application',
    long_description=readme(),
    install_requires=get_requirements()
    )