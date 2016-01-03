try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  'name': 'python3-mal',
  'description': 'Provides programmatic access to MyAnimeList resources.',
  'author': 'pushrbx',
  'license': 'LICENSE.txt',
  'url': 'https://github.com/shaldengeki/python-mal',
  'download_url': 'https://github.com/pushrbx/python3-mal/archive/master.zip',
  'author_email': 'contact@pushrbx.net',
  'version': '0.2.1',
  'install_requires': ['urllib3', 'requests', 'pytz', 'lxml', 'pyreadline'],
  'tests_require': ['nose'],
  'packages': ['myanimelist']
}

setup(**config)