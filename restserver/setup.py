# -*- coding: utf-8 -*-
"""
Setuptools script for pp-jsonpcrud-service (pp.jsonpcrud.service)

"""
from setuptools import setup, find_packages

# Get the version from the source or the cached egg version:
Name = 'pp-jsonpcrud-service'
ProjectUrl = ""
Version = "1.0.0"
Author = ''
AuthorEmail = 'oisin dot mulvihill at gmail dot com'
Maintainer = ''
Summary = 'Tornado REST Application for pp-jsonpcrud-service'
License = ''
Description = Summary
ShortDescription = Summary

needed = [
    'nose',
    "requests",
    'evasion-common==1.0.2',
    'tornado==2.4',
]

test_needed = [
]

test_suite = 'pp.jsonpcrud.service.tests'

EagerResources = [
    'pp',
]

ProjectScripts = [
]

PackageData = {
    '': ['*.*'],
}

# Web Entry points
EntryPoints = {
    'console_scripts': [
        'restserver = pp.jsonpcrud.service.scripts.main:main',
    ],
}

setup(
    url=ProjectUrl,
    name=Name,
    zip_safe=False,
    version=Version,
    author=Author,
    author_email=AuthorEmail,
    description=ShortDescription,
    long_description=Description,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Tornado",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords='web wsgi bfg pylons pyramid',
    license=License,
    scripts=ProjectScripts,
    install_requires=needed,
    tests_require=test_needed,
    test_suite=test_suite,
    include_package_data=True,
    packages=find_packages(),
    package_data=PackageData,
    eager_resources=EagerResources,
    entry_points=EntryPoints,
    namespace_packages=['pp', 'pp.jsonpcrud'],
)
