#!/usr/bin/env python

import codecs

from setuptools import setup, find_packages

version = '0.8.dev0'


def read(filename):
    try:
        with codecs.open(filename, encoding='utf-8') as f:
            return unicode(f.read())
    except NameError:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()


long_description = read('README.rst').encode('utf-8')


setup(name='tactic_client_lib',
      version=version,
      install_requires=['six'],
      description='Tactic Client Library',
      long_description=long_description,
      author='Roland van Laar',
      author_email='roland@micite.net',
      url='https://github.com/rvanlaar/tactic-client',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      python_requires=">=2.7"
      )
