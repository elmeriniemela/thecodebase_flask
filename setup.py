
from setuptools import setup

setup(
    name='thecodebase',
    packages=['thecodebase'],
    include_package_data=True,
    install_requires=[
        'flask', 'passlib', 'mysqlclient',
    ],
)
