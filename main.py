from sudoku_grid import SudokuGrid
import utils_sudoku as us

def get_grid_infos():
    valid_input = False
    while not valid_input:
        columns = input("Enter the number of columns in the Sudoku grid: ")
        lines = input("And the number of rows it contains: ")
        s_columns = input("Enter the number of columns in sub-grids: ")
        s_lines = input("And the number of rows they contain: ")
        if us.valid_grid_format(columns, lines, s_columns, s_lines):
            valid_input = True
        else:
            print("Invalid input. Try again !\n")
    return SudokuGrid(int(columns), int(lines), int(s_columns), int(s_lines))

def main():
    my_sudoku = get_grid_infos()
    my_sudoku.fill_grid()
    new = my_sudoku.algorithm()
    new.display_grid()

if __name__ ==  "__main__":
    main()