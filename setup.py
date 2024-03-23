from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


def get_requirements():
    with open('requirements.txt') as f:
        return f.read().split()


setup(
    name='geoutils-rsg',
    version='0.0.3',
    package_dir={"": "geobhumi"},
    packages=find_packages(where='geobhumi'),
    url='https://github.com/dghorai',
    license='MIT License',
    author='Debabrata Ghorai, Ph.D.',
    author_email='ghoraideb@gmail.com',
    description='Geospatial Utilities for Remote Sensing and GIS Application',
    long_description=readme(),
    install_requires=get_requirements()
)
