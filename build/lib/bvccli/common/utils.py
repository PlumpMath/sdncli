from prettytable import PrettyTable


def print_table(text, table, sortkey=None):
        print_table_banner(text)
        print_table_detail(table, sortkey)


def print_table_banner(text):
    print text


def print_table_detail(table, sortkey=None):
    p = PrettyTable()
    p.field_names = table.get(table.keys()[0])[0].keys()
    p.sortby = sortkey
    p.padding_width = 1
    p.align = "l"
    for i in table:
        row = table.get(i)[0].values()
        p.add_row(row)
        # rows = [[row[sortindex]]+row for row in rows]
        #TODO Figure out how to put index column first and have secondary sort key.
    p.add_column('Index', range(len(table)))

    print p
    print("Total Records: {}").format(len(table))


def load_json_config():
    import json
    source = '''
        {"username": "admin",
         "password": "admin",
         "server": "localhost",
         "port": "8181"}
    '''
    return json.loads(source)


# def http_get(self, args):
#     uri = args['<uri>']
#     (retval, status) = self.ctl.http_get(uri)
#     if status:
#         print retval
#     else:
#         print("Houston we have a problem, {}").format(retval)

#             def http_get(self, uri):
#         headers = {'content-type': 'application/xml'}
#         try:
#             retval = self.session.get(uri, auth=self.auth, params=None, headers=headers, timeout=120)
#         except requests.exceptions.ConnectionError:
#             return(("Error connecting to BVC {}").format(self.server), False)
#         if str(retval.status_code)[:1] == "2":
#             try:
#                 data = retval.json()
#             except ValueError, e:
#                 return(("Bad JSON found: {} {}").format(e, retval.text), False)
#             return(data, True)
#         else:
#             return (("Unknown Status Code").format(retval.status_code), False)

# def get_rest_client(manager_ip=None, rest_port=None):

#     if not manager_ip:
#         manager_ip = get_management_server_ip()

#     if not rest_port:
#         rest_port = get_rest_port()

#     username = get_username()
#     password = get_password()
#     headers = create_auth_header(username, password)
#     return Client(host=manager_ip, port=rest_port, headers=headers)


# def create_auth_header(username, password):
#     header = None

#     if username and password:
#         credentials = '{0}:{1}'.format(username, password)
#         header = {AUTHENTICATION_HEADER: base64_encode(credentials)}

#     return header


# def get_rest_port():
#     settings = load_settings()
#     return settings.get_rest_port()


# def get_management_server_ip():
#     settings = load_working_dir_settings()
#     management_ip = settings.get_management_server()
#     if management_ip:
#         return management_ip

#     msg = ("Must either first run 'cfy use' command for a "
#            "management server or provide a management "
#            "server ip explicitly")
#     raise CloudifyCliError(msg)


# def get_username():
#     return os.environ.get(CLOUDIFY_USERNAME_ENV)


# def get_password():
#     return os.environ.get(CLOUDIFY_PASSWORD_ENV)
