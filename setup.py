import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlcycle",
    version='0.1.6',
    url="http://git01-ifm-min.ad.fh-bielefeld.de/pvserve2/mlcycle",
    author="Cem Basoglu",
    author_email="cem.basoglu@fh-bielefeld.de",
    description="MLCycle client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=setuptools.find_packages(exclude=["*.tests"]),
    install_requires=[
        'requests'
    ],
    tests_require=[
        'httmock'
    ],
    test_suite="mlcycle.tests",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
)
