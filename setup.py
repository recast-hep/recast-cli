from setuptools import setup, find_packages

setup(
  name = 'recast-cli',
  version = '0.1.0',
  description = 'RECAST Command Line Tools',
  url = 'http://github.com/recast-hep/recast-cli',
  author = 'Kyle Cranmer, Lukas Heinrich',
  author_email = 'cranmer@cern.ch, lukas.heinrich@cern.ch',
  packages = find_packages(),
  entry_points = {
    'console_scripts': [
      'recast = recastcli.toplevelcli:recast',
      'recast-old = recastcli.oldcli:cli'
    ]
  },
  install_requires = [
    'recast-api'
  ]
)
