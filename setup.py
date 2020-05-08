from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

    
dependencies = []

long_description = """
csvtool is a simple command-line tool to 1) extract statistics, 2) perform regular expression search and, 3) generate output file 
without writing code for such simple tasks for .CSV files.
"""

setup(
    name='csvtool',
    version="0.2",
    url='https://github.com/maroofi/csvtool/',
    author='Sourena Maroofi',
    install_requires=dependencies,
    setup_requires=dependencies,
    author_email='maroofi@gmail.com',
    description='csvtool is an easy to use command-line tool to work with .CSV files.',
    long_description=long_description,
    packages=['csvtool',],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'csvtool = csvtool.csvtool:main',
        ],
    },
    license = "MIT",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Text Processing",
        "Topic :: Education",
        "Environment :: Console",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
    ],
)
