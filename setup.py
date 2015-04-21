from setuptools import setup, find_packages
setup(
    name="BVCCLI",
    version="0.9.0",
    description='BVC Command Line Interface',
    author='Brocade Communications',
    author_email='gberger@brocade.com',
    maintainer='gberger@brocade.com',
    packages=find_packages(),
    install_requires=['docopt',
                      'requests',
                      'prettytable'],
    entry_points={
        'console_scripts': [
            'bvccli = bvccli.__main__:main',
        ],
    },
    license="Apache License")
