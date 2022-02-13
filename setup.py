import os
from setuptools import setup

def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "plogger",
    version = "0.0.1",
    author = "Prashantha TP",
    description = ("Logging Util for Python"),
    license = "MIT",
    keywords = "msys2 gitbash bash pacman",
    url = "https://github.com/PrashanthaTP/plogger",
    #packages=['an_example_pypi_project', 'tests'],
    long_description=read_file('README.md'),
)
