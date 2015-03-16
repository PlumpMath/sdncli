from setuptools import setup, find_packages
setup(
    name="BVC CLI",
    version="0.0.1",
    description='BVC Command Line Interface',
    author='Brocade Communications',
    author_email='gberger@brocade.com',
    maintainer='gberger@brocade.com',
    packages=find_packages(),
    scripts=['bvc',
             'lib/flow_parse.py'],
    install_requires=['docopt',
                      'ncclient'],
    license="Apache License")
