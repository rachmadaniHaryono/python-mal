try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  'name': 'python3-mal_crawler',
  'description': 'Provides programmatic access to MyAnimeList resources.',
  'author': 'pushrbx',
  'license': 'LICENSE.txt',
  'url': 'https://github.com/shaldengeki/python-mal_crawler',
  'download_url': 'https://github.com/pushrbx/python3-mal_crawler/archive/master.zip',
  'author_email': 'contact@pushrbx.net',
  'version': '0.2.7',
  'install_requires': ['urllib3==1.21.1', 'requests', 'pytz', 'lxml', 'cssselect'],
  'tests_require': ['nose'],
  'packages': ['myanimelist']
}

setup(**config)
