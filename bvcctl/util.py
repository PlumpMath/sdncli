from prettytable import PrettyTable


def print_table_dict(fields, table, sortkey=None):
    p = PrettyTable()
    for row in table:
        print row
        p.field_names = row.keys()
        p.add_row(row.values())
        p.sortby = sortkey
        p.padding_width = 1
        p.align = "l"
    print p.get_string(fields=fields)


def print_table_col(fieldname, col, sortkey=None):
    print fieldname
    print col
    p = PrettyTable()
    p.add_column(fieldname, col)
    p.sortby = sortkey
    p.padding_width = 1
    p.align = "l"
    print p


def print_table_list(fieldnames, listing, sortkey=None):
    p = PrettyTable(header=True)
    p.add_column(fieldnames, listing)
    # for i in listing:
    #     if i is not None:
    #         p.add_row(i)
    p.sortby = sortkey
    p.padding_width = 1
    p.align = "l"
    print p


def load_json_file(file):
    import json
    with open(file, "r") as fh:
        return (json.loads(fh.read()))
