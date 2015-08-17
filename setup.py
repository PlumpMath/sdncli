from setuptools import setup, find_packages
import sdnctl
setup(
    name="sdncli",
    version=sdnctl.__version__,
    description='SDN Command Line Interface',
    author='Brocade Communications',
    author_email='gberger@brocade.com',
    maintainer='gberger@brocade.com',
    url='https://github.com/gaberger/sdncli',
    packages=find_packages(),
    install_requires=['docopt',
                      'requests',
                      'prettytable',
                      'singledispatch',
                      'ascii_graph'],
    entry_points={'console_scripts': ['sdncli = sdnctl.sdncli:main']},
    include_package_data=True,
    platforms='any',
    license='BSD')
