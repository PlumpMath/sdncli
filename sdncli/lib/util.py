from prettytable import PrettyTable


def print_table_dict(fields, table, sortkey=None):
    p = PrettyTable()
    for row in table:
        print row.keys()
        print row.values()
        p.field_names = row.keys()
        p.add_row(row.values())
        p.sortby = sortkey
        p.padding_width = 1
        p.align = "l"
    print p.get_string(fields=fields)


def print_table_col(fieldname, col, sortkey=None):
    p = PrettyTable()
    p.add_column(fieldname, col)
    p.sortby = sortkey
    p.padding_width = 1
    p.align = "l"
    print p


def load_json_file(file):
    import json
    with open(file, "r") as fh:
        return (json.loads(fh.read()))


def remove_keys(d, keys):
    r = dict(d)
    for i in keys:
        if i in r:
            del r[i]
    return r
