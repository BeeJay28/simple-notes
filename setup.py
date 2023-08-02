from setuptools import setup, find_packages

setup(
    name='simple_notes',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['simple_notes = Main:main'],
    },
)