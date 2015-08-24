from singledispatch import singledispatch
from bvccli.drivers.nos import NOS
from bvccli.drivers.vyatta import Vyatta5600


@singledispatch
def get_interfaces():
    raise NotImplementedError("Not Implemented Yet!")


@get_interfaces.register(NOS)
def _(obj):
    result = NOS.get_interfaces(obj)
    return result


@get_interfaces.register(Vyatta5600)
def _(obj):
    result = Vyatta5600.get_interfaces(obj)
    return result


@singledispatch
def map_interfaces():
    raise NotImplementedError("Not Implemented Yet!")


@map_interfaces.register(NOS)
def _(obj):
    result = NOS.maptoietfinterfaces()
    return result


@map_interfaces.register(Vyatta5600)
def _(obj):
    result = Vyatta5600.maptoietfinterfaces()
    return result
