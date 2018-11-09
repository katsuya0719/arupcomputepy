from setuptools import setup, find_packages

setup(name='arupcomputepy',
    version='0.1.1',
    description='Python library to interact with the Arup Compute API',
    url='https://gitlab.arup.com/Bristol/arupcomputepy',
    author='Hugh Groves',
    install_requires=['requests','requests_futures'],
    packages=find_packages(),
    zip_safe=False)