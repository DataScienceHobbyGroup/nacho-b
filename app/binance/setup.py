"""
TODO: Add description.

Date: 2021-05-23
Author: Vitali Lupusor
"""

# Import standard modules
import setuptools   # type: ignore

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='binance',
    version='0.0.1',
    author='Vitali Lupusor',
    author_email='VitaliLupusor@gmail.com',
    description='Binance API SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DataScienceHobbyGroup/nacho-b',
    project_urls={
        'Bug Tracker': (
            'https://github.com/DataScienceHobbyGroup/nacho-b/issues'
        ),
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.9',
    install_requires=['requests'],
)
