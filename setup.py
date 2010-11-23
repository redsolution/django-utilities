# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

# Utility function to read the README file.  
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="redsolutioncms.django-utilities",
    version=__import__('utilities').__version__,
    description=read('DESCRIPTION'),
    license="GPLv3",
    keywords="django utilities",

    author="Alexander Ivanov",
    author_email="alexander.ivanov@redsolution.ru",

    maintainer='Alexander Ivanov',
    maintainer_email='alexander.ivanov@redsolution.ru',

#    url="http://packages.python.org/django-utilities",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Russian',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.5',
        'Topic :: Software Development :: Version Control',
    ],
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
    entry_points={
        'redsolutioncms': ['utilities = utilities.redsolution_setup', ],
    }
)
