from PrettyTable import PrettyTable


def print_table_list(text, table, sortkey=None):
    p = PrettyTable()
    for i in table:
        if i is not None:
            p.field_names = i.keys()
            p.add_row(i.values())
    p.sortby = sortkey
    p.padding_width = 1
    p.align = "l"