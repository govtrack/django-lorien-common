#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = 'django-common',
    description = 'A number of useful django shortcuts and helpers',
    version = '0.1.48',
    author = 'Grigoriy Petukhov',
    author_email = 'lorien@lorien.name',
    url = 'http://bitbucket.org/lorien/django-common/',

    packages = find_packages(),
    include_package_data = True,

    license = "BSD",
    keywords = "django application development shortcuts helpers",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
