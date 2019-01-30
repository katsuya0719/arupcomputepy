from setuptools import setup, find_packages

setup(name='arupcomputepy',
    version='0.1.5',
    description='Python library to interact with the Arup Compute API',
    url='https://gitlab.arup.com/arupcompute/arupcomputepy',
    author='Hugh Groves',
    install_requires=['requests','adal','appdirs'],
    packages=find_packages(),
    zip_safe=False)