#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   Copyright 2008-2020 The Open Microscopy Environment, Glencoe Software, Inc.
   All rights reserved.

   Use is subject to license terms supplied in LICENSE.txt

"""

import glob
import os
from setuptools import setup

VERSION = "0.1.0"

url = "https://docs.openmicroscopy.org/latest/omero/developers/Server/FS.html"

packageless = glob.glob("src/*.py", recursive=True)
packageless = [x[4:-3] for x in packageless]


def read(fname):
    """
    Utility function to read the README file.
    :rtype : String
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="omero-pipeline",
    version=VERSION,
    description="OMERO.dropbox server extension for pre-upload conversions via seperately installed file converters and post-upload processing via OMERO.scripts",
    long_description=read("README"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],  # Get strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    author="Michael Barrett",
    author_email="mjbarrett@mcw.edu",
    url=url,
    package_dir={"": "src"},
    package_data={"": ["schema/*.schema.json"]}
    py_modules=packageless,
    install_requires=[
        "omero-dropbox",  # requires omero-py (use wheel for faster installs)
    ],
    python_requires=">=3",
    tests_require=["pytest"],
)
