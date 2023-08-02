from setuptools import setup, find_packages

setup(
    name='simple-notes',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['simple-notes = Main:main'],
    },
)