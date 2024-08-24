import utils_sudoku as us
import copy

class SudokuGrid:

    def __init__(self, columns, lines, s_columns, s_lines):
        self.nb_columns = columns
        self.nb_lines = lines
        self.grid = [[None for _ in range(self.nb_columns)] for _ in range(self.nb_lines)]
        self.sub_columns = s_columns
        self.sub_lines = s_lines
        self.candidates = [[[] for _ in range(self.nb_columns)] for _ in range(self.nb_lines)]
    
    def fill_grid(self):
        print("Enter the numbers on each line, replacing empty boxes with 'x'.")
        for i in range(len(self.grid)):
            valid_input = False
            while not valid_input:
                line = input("Line {}: ".format(i + 1))
                if us.valid_line_content(line, self.nb_columns):
                    valid_input = True
                else:
                    print("Invalid input. Try again !")
            j = 0
            for c in line:
                self.grid[i][j] = c
                j += 1
    
    def display_grid(self):
        i = 0
        s = ""
        while i + 1 < self.nb_columns:
            s += "----"
            i += 1
        print(" " + s + "---")
        for line in self.grid:
            s = "|"
            for nb in line:
                s += " {} |".format(nb)
            print(s)
            i = 0
            s = ""
            for i in range(self.nb_columns - 1):
                s += "----"
            print(" " + s + "---")

    def set_candidates(self):
        numbers = [str(number) for number in range(1, (self.sub_lines * self.sub_columns) + 1)]
        for i in range(self.nb_lines):
            for j in range(self.nb_columns):
                if not self.grid[i][j].isdigit():
                    self.candidates[i][j] = []
                    for nb in numbers:
                        if (self.check_rows(nb, i) and self.check_columns(nb, j) and self.check_subgrids(nb, i, j)):
                            self.candidates[i][j].append(nb)
                    if self.candidates[i][j] == []:
                        return False
                else:
                    self.candidates[i][j] = []
        return True   

    def one_possibility(self):
        change = 0
        numbers = [str(number) for number in range(1, (self.sub_lines * self.sub_columns) + 1)]
        for i in range(self.nb_lines):
            for nb in numbers:
                count = 0
                for j in range(self.nb_columns):
                    if not len(self.candidates[i][j]) == 0:
                        for candidate in self.candidates[i][j]:
                            if candidate == nb:
                                count += 1
                                index = j
                if count == 1:
                    if (self.check_rows(nb, i) and self.check_columns(nb, index) and self.check_subgrids(nb, i, index) and not self.grid[i][index].isdigit()):
                        change += 1
                        self.grid[i][index] = nb
                    else:
                        return -1
                    if self.set_candidates() == False:
                        return -1
        for j in range(self.nb_columns):
            for nb in numbers:
                count = 0
                for i in range(self.nb_lines):
                    if not len(self.candidates[i][j]) == 0:
                        for candidate in self.candidates[i][j]:
                            if candidate == nb:
                                count += 1
                                index = i
                if count == 1:
                    if (self.check_rows(nb, index) and self.check_columns(nb, j) and self.check_subgrids(nb, index, j) and not self.grid[index][j].isdigit()):
                        change += 1
                        self.grid[index][j] = nb
                    else:
                        return -1
                    if self.set_candidates() == False:
                        return -1
        a = 0
        while a < (self.nb_lines / self.sub_lines):
            b = 0
            while b < (self.nb_columns / self.sub_columns):
                for nb in numbers:
                    count = 0
                    for i in range(a * self.sub_lines, self.sub_lines * (a + 1)):
                        for j in range(b * self.sub_columns, self.sub_columns * (b + 1)):
                            if not len(self.candidates[i][j]) == 0:
                                for candidate in self.candidates[i][j]:
                                    if candidate == nb:
                                        count += 1
                                        indexes = [i, j]
                    if count == 1:
                        if (self.check_rows(nb, indexes[0]) and self.check_columns(nb, indexes[1]) and self.check_subgrids(nb, indexes[0], indexes[1]) and not self.grid[indexes[0]][indexes[1]].isdigit()):
                            change += 1
                            self.grid[indexes[0]][indexes[1]] = nb
                        else:
                            return -1
                        if self.set_candidates() == False:
                            return -1
                b += 1
            a += 1
        return change
    
    def one_candidate(self):
        change = 0
        for i in range(self.nb_lines):
            for j in range(self.nb_columns):
                if len(self.candidates[i][j]) == 1:
                    if (self.check_rows(self.candidates[i][j][0], i) and self.check_columns(self.candidates[i][j][0], j) and self.check_subgrids(self.candidates[i][j][0], i, j) and not self.grid[i][j].isdigit()):
                        self.grid[i][j] = self.candidates[i][j][0]
                        change += 1
                    else:
                        return -1
                    if self.set_candidates() == False:
                        return -1
        return change
    
    def remove_elements(self, element, indexes, change):
        for j in range(indexes[1], indexes[3] + 1, indexes[3] - indexes[1]):
            for i in range(self.nb_lines):
                if i == indexes[0] or i == indexes[4]:
                    continue
                if len(self.candidates[i][j]) > 0:
                    if element in self.candidates[i][j]:
                        self.candidates[i][j].remove(element)
                        change += 1
    
    def valid_x_wing(self, indexes):
        if not indexes[1] == indexes[5] or not indexes[3] == indexes[7]:
            return False
        i = us.index_line_subgrid(0, indexes[0], self.nb_lines, self.sub_lines)
        j = us.index_column_subgrid(0, indexes[1], self.nb_columns, self.sub_columns)
        if us.index_line_subgrid(0, indexes[2], self.nb_lines, self.sub_lines) == i \
           and us.index_line_subgrid(0, indexes[4], self.nb_lines, self.sub_lines) == i \
           and us.index_line_subgrid(0, indexes[6], self.nb_lines, self.sub_lines) == i \
           and us.index_line_subgrid(0, indexes[3], self.nb_lines, self.sub_lines) == j \
           and us.index_line_subgrid(0, indexes[5], self.nb_lines, self.sub_lines) == j \
           and us.index_line_subgrid(0, indexes[7], self.nb_lines, self.sub_lines) == j :
            return False;
        return True

    def x_wing(self):
        change = 0
        numbers = [str(number) for number in range(1, (self.sub_lines * self.sub_columns) + 1)]
        for nb in numbers:
            indexes = []
            for i in range(self.nb_lines):
                tmp_indexes = []
                for j in range(self.nb_columns):
                    if nb in self.candidates[i][j]:
                        tmp_indexes.append(i)
                        tmp_indexes.append(j)
                if len(tmp_indexes) == 4:
                    indexes.extend(tmp_indexes)
                if len(indexes) == 8:
                    if self.valid_x_wing(indexes):
                        self.remove_elements(nb, indexes, change)
                    indexes.clear()
        return change
    
    def search_minimum_options(self):
        min = None
        current = 0
        last = 0
        for start_i in range(self.nb_lines):
            for start_j in range(self.nb_columns):
                if not self.grid[start_i][start_j].isdigit():
                    min = [start_i, start_j]
                    last = len(self.candidates[start_i][start_j])
                    break
            if min != None:
                break
        for i in range(start_i, self.nb_lines):
            for j in range(start_j, self.nb_columns):
                if not self.grid[i][j].isdigit():
                    current = len(self.candidates[i][j])
                if current < last and not self.grid[i][j].isdigit():
                    last = current
                    min = [i, j]
        if min == None:
            return None
        return min

    def guess_and_check(self):
        if self.set_candidates() == False:
            return None
        while not (self.filled()):
            change = True
            while change:
                change = False
                result = self.one_possibility()
                while (result > 0):
                    change = True
                    result = self.one_possibility()
                if result < 0:
                    return None
                result = self.one_candidate()
                while (result > 0):
                    change = True
                    result = self.one_candidate()
                if result < 0:
                    return None
                result = self.x_wing()
                while (result > 0):
                    change = True
                    result = self.x_wing()
                if result < 0:
                    return None
            indexes = self.search_minimum_options()
            if indexes == None:
                return self
            res = self.handle_grid(indexes[0], indexes[1])
            if res == None:
                return 
            else:
                self = None
                self = res
            if not self.solved():
                return None
        if self.solved():
            return self
        return None

    def handle_grid(self, i, j):
        if len(self.candidates[i][j]) == 1 and not self.grid[i][j].isdigit():
            if (self.check_rows(self.candidates[i][j][0], i) and self.check_columns(self.candidates[i][j][0], j) and self.check_subgrids(self.candidates[i][j][0], i, j)):
                self.grid[i][j] = self.candidates[i][j][0]
            else:
                return None
            if self.set_candidates() == False:
                return None
        elif len(self.candidates[i][j]) > 1:
            for nb in self.candidates[i][j]:
                copy_obj = None
                copy_obj = copy.deepcopy(self)
                copy_obj.grid[i][j] = nb
                res = copy_obj.guess_and_check()
                if not res == None:
                    return res
        return None
    
    def filled(self):
        for line in self.grid:
            for c in line:
                if not c.isdigit():
                    return False
        return True

    def solved(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] in ['X', 'x']:
                    continue
                elif not (self.valid_row(i, j) and self.valid_column(i, j) and self.valid_subgrid(i, j)):
                    return False
        return True

    def valid_row(self, i, j):
        b = 0
        nb = self.grid[i][j]
        for current_nb in self.grid[i]:
            if (b == j and nb == current_nb):
                b += 1
                continue
            elif nb == current_nb:
                return False
            b += 1
        return True

    def valid_column(self, i, j):
        a = 0
        nb = self.grid[i][j]
        while a < self.nb_lines:
            if (a == i and self.grid[a][j] == nb):
                a += 1
                continue
            elif self.grid[a][j] == nb:
                return False
            a += 1
        return True

    def valid_subgrid(self, i, j):
        a = us.index_line_subgrid(0, i, self.nb_lines, self.sub_lines)
        b = us.index_column_subgrid(0, j, self.nb_columns, self.sub_columns)
        nb = self.grid[i][j]
        for count_a in range(a, a + self.sub_lines):
            for count_b in range(b, b + self.sub_columns):
                if (count_a == i and count_b == j and self.grid[count_a][count_b] == nb):
                    continue
                elif self.grid[count_a][count_b] == nb:
                    return False
        return True
    
    def check_rows(self, nb, i):
        for c in self.grid[i]:
            if c == nb:
                return False
        return True

    def check_columns(self, nb, j):
        i = 0
        while i < self.nb_lines:
            if self.grid[i][j] == nb:
                return False
            i += 1
        return True

    def check_subgrids(self, nb, i, j):
        a = us.index_line_subgrid(0, i, self.nb_lines, self.sub_lines)
        b = us.index_column_subgrid(0, j, self.nb_columns, self.sub_columns)
        for count_a in range(a, a + self.sub_lines):
            for count_b in range(b, b + self.sub_columns):
                if self.grid[count_a][count_b] == nb:
                    return False
        return True
    
    def algorithm(self):
        if not self.solved():
            print("! UNRESOLVABLE !")
            exit(1)
        self.set_candidates()
        while not self.filled():
            change = True
            while change:
                change = False
                while self.one_possibility() > 0:
                    change = True
                while self.one_candidate() > 0:
                    change = True
                while self.x_wing() > 0:
                    change = True
            indexes = self.search_minimum_options()
            if indexes == None:
                return self
            res = self.handle_grid(indexes[0], indexes[1])
            if res != None:
                self = None
                self = res
            else:
                print("! UNRESOLVABLE !")
                exit(1)
        return self