try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

NAME = "myanimelist"
package = __import__(NAME)

config = {
    'name': 'python-mal',
    'description': package.__doc__ ,
    'author': package.__author__,
    'license': package.__license__,
    'url': 'https://github.com/shaldengeki/python-mal',
    'download_url': 'https://github.com/shaldengeki/python-mal/archive/master.zip',
    'author_email': package.__email__,
    'version': package.__version__,
    'install_requires': ['beautifulsoup4', 'requests', 'pytz', 'lxml'],
    'tests_require': ['nose'],
    'packages': [NAME],
}

setup(**config)
