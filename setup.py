# !/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='django-khipu',
    version=__import__("khipu").__version__,
    description='Aplicación para integrar pagos Khipu en Django',
    url="https://github.com/misalabs/django-khipu",
    author='Misa G.',
    author_email="hi@misalabs.com",
    maintainer='Misa G.',
    maintainer_email='hi@misalabs.com',
    license='MIT license',
    platforms=['any'],
    packages=find_packages(),
    package_dir={"khipu": "khipu"},
    install_requires=[
        'Django>=1.6',
        'requests>=2.5.3',
    ],
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Environment :: Web Environment",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
    ],
    include_package_data=True,
    zip_safe=False,
    keywords='django khipu chile',
)
