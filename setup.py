#!/usr/bin/env python
from os import path

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst")) as f:
    long_description = f.read()


def _post_install():
    """Post installation nltk corpus downloads."""
    import nltk

    nltk.download("punkt")
    nltk.download("stopwords")


class PostDevelop(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)
        self.execute(_post_install, [], msg="Running post installation tasks")


class PostInstall(install):
    """Post-installation for production mode."""

    def run(self):
        install.run(self)
        self.execute(_post_install, [], msg="Running post installation tasks")


# Get package and author details.
about = {}
with open(path.join(here, "rake_nltk", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    # Name of the module
    name="rake_nltk",
    # Details
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    # The project's main homepage.
    url=about["__url__"],
    # Author details
    author=about["__author__"],
    author_email=about["__author_email__"],
    # License
    license=about["__license__"],
    packages=["rake_nltk"],
    test_suite="tests",
    keywords="nlp text-mining algorithms development",
    classifiers=[
        # Intended Audience.
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        # License.
        "License :: OSI Approved :: MIT License",
        # Project maturity.
        "Development Status :: 3 - Alpha",
        # Operating Systems.
        "Operating System :: POSIX",
        # Supported Languages.
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        # Topic tags.
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=["nltk"],
    cmdclass={"develop": PostDevelop, "install": PostInstall},
)
