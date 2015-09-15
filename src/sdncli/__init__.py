__title__ = 'sdncli'
__version__ = '1.1.1'
__author__ = 'Gary Berger'
__license__ = 'BSD'
__copyright__ = 'Brocade Communications'

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
