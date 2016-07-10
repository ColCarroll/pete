from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as buff:
    long_description = buff.read()


setup(
    name='pete',
    version='0.0.1',
    description='A simple taskrunner',
    long_description=long_description,
    author='Colin Carroll',
    author_email='colcarroll@gmail.com',
    url='https://github.com/ColCarroll/pete',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=['test']),
    install_requires=[],
    extras_require={
        'dev': ['ipython', 'flake8'],
        'test': ['pytest', 'pytest-cov']
    },
    include_package_data=True,
)
