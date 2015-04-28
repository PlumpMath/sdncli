from ..common import utils
from uuid import uuid4
import string

import random


def random_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))


def generatemock(size=100):
    interfacedb = {}
    for i in range(size):
        interface = {'device': random_generator(5),
                     'name': 'eth' + random_generator(2, string.digits),
                     'type': 'ianaift:ethernetCsmacd',
                     'admin-status': 'up',
                     'oper-status': 'up',
                     'if-index': random_generator(2, string.digits)}
        interfacedb.setdefault(uuid4(), []).append(interface)
    return interfacedb


def printinterfaces():
    utils.print_table('Interfaces', generatemock(), sortkey=None)
