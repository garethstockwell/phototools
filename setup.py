# setup.py

import os
from setuptools import setup

def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="phototools",
    version="0.0.1",
    author="Gareth Stockwell",
    author_email="gareth.stockwell@gmail.com",
    description="Tools for managing photo library",
    long_description=read_file("README.md"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],

    install_requires=[
        line.strip() for line in open("requirements.txt").readlines()],

    packages=["phototools"],

    entry_points={
        "console_scripts": [
            "phototools=phototools.__main__:main",
        ]
    },
)
