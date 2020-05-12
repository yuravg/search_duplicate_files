"""Setup file"""

from setuptools import setup, find_packages
import search_duplicate_files

setup(
    name='search_duplicate_files',
    version=search_duplicate_files.__version__,
    description='Search duplicate files',
    url='',
    author='Yuriy VG',
    author_email='yuravg@gmail.com',
    license='MIT',
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    entry_points={
        'console_scripts': [
            'sduplicate = search_duplicate_files.main:main'
        ]
    },
    long_description=open('README.md').read(),
    include_package_data=True,
    packages=find_packages(exclude=['tests']),
    test_suite='tests'
)
