#!/usr/bin/env python

import codecs

from setuptools import setup, find_packages

version = '4.8'

setup(name='tactic_client_lib',
      version=version,
      install_requires=['six'],
      description='Tactic Client Library',
      author='Roland van Laar',
      author_email='roland@micite.net',
      url='https://github.com/rvanlaar/tactic-client',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      scripts=['bin/get_ticket.py', 'bin/create_project.py'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.7'
      ]
     )
