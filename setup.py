"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pydor',
    version='0.2.2',
    description='Python docker registry (distribution) client',
    long_description=long_description,
    url='https://github.com/dohnto/pydor',
    author='Tomas Dohnalek',
    author_email='dohnto@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='docker registry distribution',
    packages=find_packages(exclude=['test']),
    install_requires=['click', "LinkHeader", "requests", "six", "tablib", "urllib3"],
    entry_points = {
        'console_scripts': ['pydor=pydor.commandline:cli'],
    }
)
