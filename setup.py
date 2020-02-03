from setuptools import setup, find_packages

setup(name='arupcomputepy',
    version='0.2.1',
    description='Python library to interact with the Arup Compute API',
    url='https://gitlab.arup.com/arupcompute/arupcomputepy',
    author='Hugh Groves',
    install_requires=['requests','msal','appdirs'],
    packages=find_packages(),
    zip_safe=False)
