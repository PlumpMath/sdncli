from prettytable import PrettyTable
from pybvc.common.status import STATUS

def print_table_dict(fields, table, sortkey=None):
    p = PrettyTable()
    for row in table:
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


def isconnected(ctrl,node):
    result = ctrl.check_node_conn_status(node)
    status = result.get_status()
    if (status.eq(STATUS.NODE_CONNECTED)):
        return True
    else:
        return False
