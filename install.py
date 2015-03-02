#!/usr/bin/python
"""
Usage:
        bvc install [--ignore] [--path <dir>] [--address]
        bvc upgrade [--ignore] [--path <dir>] [--address]
        bvc start
        bvc stop
        bvc clean
        bvc log

Options:
    -A, --address           Address to bind UI
    -I, --ignore
    -D, --dir               Installation Directory
    -h, --help

"""
from lib.docopt import docopt
from lib.bvcutils import BvcUtil
import os
# import pprint


def install(dir, ignore=None):

    bvc = BvcUtil(".", "bvc-config.json")
    
    if not ignore:
        bvc.check_system

    bvc.initialize_directories()
    ext_basenames = bvc.get_basenames(".extensions", 'zip')
    dep_basenames = bvc.get_basenames(".dependencies", 'zip')
    archive_basenames = bvc.get_basenames(".archive", 'zip')
    versions_basenames = bvc.convert_versionnames(bvc.get_basenames('versions', 'properties'))
    install_base = "bvc-core-odl-controller" in dep_basenames
    install_ui = "bvc-core-odl-web" in dep_basenames
    install_bvc = "bvc-core-bvc-controller" in dep_basenames
    
    if 'bvc-dependencies' not in versions_basenames:
        bvc.logger.error("Please install bvc-dependencies")
        bvc.exit_install



def upgrade():

    # Look for files which alread exist to determine upgrade.
    #TODO might want to check version manifests or some other way to deal with state
    #TODO make update more explicit as a command line option i.e. bvc update/bvc upgrade
    upgrade_names = []
    for bName in ext_basenames:
        if bName in archive_basenames:
            upgrade_names.append(bName)
    for bName in dep_basenames:
        if bName in archive_basenames:
            upgrade_names.append(bName)

    ## Todo



if __name__ == "__main__":
    args = docopt(__doc__)
    if args["install"]:
        if args["--path"]:
            install(["<dir>"])
        else:
            install(os.getcwd())
    if args["upgrade"]:
        upgrade()

#(Pdb) bvcBaseDistName
# 'bvc-core-bvc-controller'
# (Pdb) depBaseNames
# ['bvc-core-odl-controller', 'bvc-core-odl-web', 'bvc-core-bvc-web']
# -> for bName in extBaseNames:
# (Pdb) extBaseNames
# ['bvc-app-pathexplorer-packaging', 'bvc-core-bvc-controller']
