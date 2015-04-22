from prettytable import PrettyTable
import os


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


def print_table_detail2(text, table, sortkey=None):
    p = PrettyTable()
    p.field_names = table.keys()
    p.sortby = sortkey
    p.padding_width = 1
    p.align = "l"
    row = table.values()
    p.add_row(row)

    print text
    print p


def load_json_config():
    import json
    source = '''
        {"username": "admin",
         "password": "admin",
         "server": "localhost",
         "port": "8181"}
    '''
    return json.loads(source)


def get_home():
    from os.path import expanduser
    home = expanduser("~")
    return home


def get_cachedir():
    return os.path.join(get_home(), '.cache')


def get_configdir():
    return os.path.join(get_home(), '.config')


def get_schemadir():
    return os.path.join(get_home(), '.schema')


def prepare_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_file(node, directory, data):
    try:
        prepare_directory(directory)
    except Exception, e:
        raise e
    filename = os.path.join(directory, node)
    with open(filename, "w") as fh:
        fh.write(data)


def print_file(node, directory, data):
    filename = os.path.join(directory, node)
    decode = data.decode('string_escape')
    with open(filename, "w") as fh:
        fh.write(decode)


def check_file_and_print(filename):
    if(os.path.exists(filename)):
        with open(filename, 'r') as fh:
            buf = fh.read()
            return (buf, True)
    else:
        return (None, False)


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