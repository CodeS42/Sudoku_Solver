def valid_grid_format(columns, lines, s_columns, s_lines):
    if not columns == lines:
        return False
    if not columns in ['4', '6', '8', '9']:
        return False
    elif columns == '4' and not (s_columns == '2' and s_lines == '2'):
        return False
    elif columns == '6' and not ((s_columns == '3' and s_lines == '2') or (s_columns == '2' and s_lines == '3')):
        return False
    elif columns == '8' and not ((s_columns == '2' and s_lines == '4') or (s_columns == '4' and s_lines == '2')):
        return False
    elif columns == '9' and not (s_columns == '3' and s_lines == '3'):
        return False
    return True

def valid_line_content(line, nb_columns):
    if not len(line) == nb_columns:
        return False
    for c in line:
        if not (c.isdigit() or c in ['x', 'X']):
            return False
    return True

def index_line_subgrid(a, i, nb_lines, nb_sublines):
    while a < nb_lines - 1:
        count = 0
        while count < nb_sublines:
            if i == a + count:
                return a
            count += 1
        a += nb_sublines
    return a

def index_column_subgrid(b, j, nb_columns, nb_subcolumns):
    while b < nb_columns - 1:
        count = 0
        while count < nb_subcolumns:
            if j == b + count:
                return b
            count += 1
        b += nb_subcolumns
    return b
