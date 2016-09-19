#!/usr/bin/env python
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

NAME = "myanimelist"
package = __import__(NAME)

# handle version
# http://stackoverflow.com/a/7071358
default_version = "0.1.7"
VERSIONFILE="myniftyapp/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    verstr = default_version

config = {
    'name': 'python-mal',
    'description': package.__doc__,
    'author': package.__author__,
    'license': package.__license__,
    'url': 'https://github.com/shaldengeki/python-mal',
    'download_url': 'https://github.com/shaldengeki/python-mal/archive/master.zip',
    'author_email': package.__email__,
    'version': verstr,
    'install_requires': ['beautifulsoup4', 'requests', 'pytz', 'lxml', 'six'],
    'tests_require': ['nose'],
    'packages': [NAME],
}

setup(**config)
