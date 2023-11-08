# Copyright (C) 2023, NG:ITL
import versioneer
from pathlib import Path
from setuptools import find_packages, setup


def read(fname):
    return open(Path(__file__).parent / fname).read()


setup(
    name="raai_module_sound_server",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="NGITl",
    author_email="calvinteuber7@gmail.com",
    description=("A RAAI Module, which play specific sounds if demanded over a pynng msg"),
    license="GPL 3.0",
    keywords="",
    url="https://github.com/vw-wob-it-edu-ngitl/raai_module_sound_server",
    packages=find_packages(),
    long_description=read("README.md"),
    install_requires=["pynng~=0.7.2", "pygame"],
)
