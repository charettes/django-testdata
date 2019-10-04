from __future__ import unicode_literals

from setuptools import find_packages, setup

import testdata

with open('README.rst') as file_:
    long_description = file_.read()

setup(
    name='django-testdata',
    version=testdata.__version__,
    description='Django application providing isolation for model instances created during `setUpTestData`.',
    long_description=long_description,
    url='https://github.com/charettes/django-testdata',
    author='Simon Charette.',
    author_email='charette.s+testdata@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['django test testdata'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['Django>=1.11'],
    extras_require={
        'tests': ['tox'],
    },
)
