from setuptools import setup, find_packages
import sdncli
setup(
    name="sdncli",
    version=sdncli.__version__,
    description='SDN Command Line Interface',
    author='Brocade Communications',
    author_email='gberger@brocade.com',
    maintainer='gberger@brocade.com',
    url='https://github.com/gaberger/sdncli',
    include_package_data=True,
    packages=find_packages(),
    install_requires=['docopt',
                      'requests',
                      'prettytable',
                      'singledispatch',
                      'ascii_graph'],
    entry_points={'console_scripts': ['sdncli = sdncli.sdncli:main']},
    platforms='any',
    license='BSD')
