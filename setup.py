import os
from setuptools import setup,find_packages

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
    packages = find_packages(),
    long_description=read_file('README.md'),
)
