#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command.test import test

try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command.test import test


import os

here = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(here,  'README.rst'))
long_description = f.read().strip()
f.close()


setup(
    name='satchmo-braintree',
    version='0.2',
    author='Sumit Chachra',
    author_email='chachra@tivix.com',
    url='http://github.com/tivix/satchmo-braintree',
    description = 'An easy way to integrate Satchmo checkout with Braintree Payment Solutions gateway.',
    packages=find_packages(),
    long_description=long_description,
    keywords = "satchmo django braintree payment ecommerce",
    zip_safe=False,
    install_requires=[
        'Django>=1.2.3',
        'braintree>=2.4.0'
    ],
    # test_suite = 'satchmo_braintree.tests',
    include_package_data=True,
    # cmdclass={},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
