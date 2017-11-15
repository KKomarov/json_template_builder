#!/usr/bin/env python

from setuptools import setup

packages = ['jtb']

requires = [
    'six',
]

setup(
    name='jtb',
    version='0.5',
    description='Simple json builder from json template.',
    long_description='Github: https://github.com/KKomarov/json_template_builder',
    author='Konstantin Komarov',
    author_email='k.komarov1994@mail.ru',
    url='https://github.com/KKomarov/json_template_builder',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'jtb': 'jtb'},
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
)
