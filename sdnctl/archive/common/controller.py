import requests
from requests.auth import HTTPBasicAuth


class Controller(object):
    def __init__(self, auth, address):
        self.port = auth.get('port', 8181)
        self.auth = HTTPBasicAuth(auth.get('username', 'admin'), auth.get('password', 'admin'))
        self.server = address or auth.get('server')
        self.session = requests.Session()
        self.headers = {'content-type': 'application/json'}
