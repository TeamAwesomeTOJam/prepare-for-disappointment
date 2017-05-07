from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Disappointment',
    version='0.1.0',

    description='',
    long_description=long_description,

    url='https://github.com/TeamAwesomeTOJam/prepare-for-disappointment',
    author='Team Awesome',
    author_email='jonathan@jdoda.ca',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    packages=['disappointment'],

    package_data = {
        'disappointment': ['res/*/*'],
    },
    
    entry_points = {
        'gui_scripts' : [
            'disappointment = disappointment.main:go'
        ]
    },

    install_requires=[
        'awesomeengine>=0.0.1'
    ],
)
