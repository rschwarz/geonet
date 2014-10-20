from setuptools import setup, find_packages

setup(
    name='geonet',
    version='0.0.0',
    description='design topology and geometry of networks',
    packages=find_packages(exclude=['tests*']),
    install_requires=['networkx', 'scipy', 'cvxpy'],
)
