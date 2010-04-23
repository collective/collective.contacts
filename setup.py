    # -*- coding: utf-8 -*-
"""This module contains the tool of collective.contacts
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.4.4'

long_description = (
    read('docs', 'README-en.txt')
    + '\n' +
    read('docs', 'HISTORY.txt')
    + '\n' +
    '============\n'
    'Contributors\n'
    '============\n'
    + '\n' +
    read('docs', 'CONTRIBUTORS.txt')
    + '\n' +
    '========\n'
    'Download\n'
    '========\n'
    )

tests_require = ['zope.testing', 'plone.mocktestcase']

setup(name='collective.contacts',
      version=version,
      description="Address book product for Plone",
      long_description=long_description,
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='plone addressbook collective contacts',
      author='Emanuel Sartor, Franco Pellegrini',
      author_email='info@menttes.com',
      maintainer='Franco Pellegrini',
      maintainer_email='frapell@menttes.com',
      url='http://plone.org/products/collective.contacts',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        'Products.ATExtensions',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      #test_suite = 'collective.contacts.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins=['ZopeSkel'],
      )
