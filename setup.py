# import modules
# import sys
from setuptools import setup, find_packages

# class VersionError(Exception):

#     def __init__(self, *args, **kwargs):
#         Exception.__init__(self, *args, **kwargs)
#         return


def readme():
    with open('README.md') as f:
        return f.read()


def get_requirements():
    with open('requirements.txt') as f:
        return f.read().split()


setup(
    name='rsgis-toolbox',
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/dghorai',
    license='MIT License',
    author='Debabrata Ghorai, Ph.D.',
    author_email='ghoraideb@gmail.com',
    description='Geospatial utilities for Remote Sensing and GIS application',
    long_description=readme(),
    install_requires=get_requirements()
)
