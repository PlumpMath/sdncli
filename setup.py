import versioneer
from setuptools import setup, find_packages

setup(
    name="sdncli",
    version=versioneer.getversion(),
    cmdclass=versioneer.get_cmdclass(),
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
                      'ascii_graph',
                      'pybvc'],
    dependency_links=[
        "git+ssh://git@github.com:gaberger/pybvc.git"
    ],
    entry_points={'console_scripts': ['sdncli = sdncli.sdncli:main']},
    platforms='any',
    license='BSD')
