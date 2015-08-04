from prettytable import PrettyTable


def print_table_dict(text, table, sortkey=None):
    p = PrettyTable()
    for i in table:
        if i is not None:
            p.field_names = i.keys()
            p.add_row(i.values())
    p.sortby = sortkey
    p.padding_width = 1
    p.align = "l"
    print p


def print_table_list(text, list, sortkey=None):
    p = PrettyTable()
    for i in list:
        if i is not None:
            p.add_row(i)
    p.sortby = sortkey
    p.padding_width = 1
    p.align = "l"
    print p