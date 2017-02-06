from __future__ import absolute_import, division, print_function, unicode_literals

from os import path

from setuptools import setup, find_packages

with open(path.join(path.dirname(__file__), 'README.md'), 'r') as fp:
    long_description = fp.read()

setup(
    name='pylijm',
    version='1.0.0b1',
    description='Python Lightweight JSON Model',
    long_description=long_description,
    url='https://github.com/blake-r/pylijm',
    author='Oleg Blednov',
    author_email='blake-r@mail.ru',
    license='GNUv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    keywords='dict json model document nosql',
    packages=find_packages(exclude=['tests']),
    install_requires=['six'],
    extras_require={
        'tests': ['unittest2', 'ujson']
    }
)
