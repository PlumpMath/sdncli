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


def print_table_list(text, table, sortkey=None):
    p = PrettyTable()
    for i in table:
        if i is not None:
            p.field_names = i.keys()
            p.add_row(i.values())
    p.sortby = sortkey
    p.padding_width = 1
    p.align = "l"

    print text
    print p


def print_table_keys(text, key, table, sortkey=None):
    p = PrettyTable()
    p.field_names = table.keys()
    for v in table[key].keys():
        p.add_row([v])
    p.sortby = key
    p.padding_width = 1
    p.align = "l"

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


def load_json_file(file):
    import json
    with open(file, "r") as fh:
        return (json.loads(fh.read()))


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
    # print "Writing file %s" % filename
    with open(filename, "w") as fh:
        fh.write(data[1:-1])


def print_file(node, directory, data):
    filename = os.path.join(directory, node)
    decode = data.decode('string_escape')
    with open(filename, "w") as fh:
        fh.write(decode[1:-1])


def check_file_and_print(filename):
    if(os.path.exists(filename)):
        with open(filename, 'r') as fh:
            buf = fh.read()
            return (buf, True)
    else:
        return (None, False)

