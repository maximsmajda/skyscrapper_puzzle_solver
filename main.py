# printing puzzle board
def print_board(board_to_print, size):
    for y in range(size):
        for x in range(size):
            print(board_to_print[y][x], end=' ')
        print()


# initialize empty board full o zeroes of given size
def init_board(board_size):
    return [[0 for i in range(board_size)] for j in range(board_size)]


# ---------------------------------------------
# ------------- prefill functions -------------
# ---------------------------------------------
def fill_from_top(board, clue, column, size):
    for y in range(clue):
        nb = (size + 1) - clue + y
        board[y][column] = nb
        if nb_in_row(board, y, column, nb) or nb_in_col(board, y, column, nb):
            return None
    return board


def fill_from_bottom(board, clue, column, size):
    for y in range(clue):
        nb = (size + 1) - clue + y
        board[size - 1 - y][column] = nb
        if nb_in_row(board, size - 1 - y, column, nb) or nb_in_col(board, size - 1 - y, column, nb):
            return None
    return board


def fill_from_left(board, clue, row, size):
    for x in range(clue):
        nb = (size + 1) - clue + x
        board[row][x] = nb
        if nb_in_row(board, row, x, nb) or nb_in_col(board, row, x, nb):
            return None
    return board


def fill_from_right(board, clue, row, size):
    for x in range(clue):
        nb = (size + 1) - clue + x
        board[row][size - 1 - x] = nb
        if nb_in_row(board, row, size - 1 - x, nb) or nb_in_col(board, row, size - 1 - x, nb):
            return None
    return board


# quickly fill boxes that are under 1 or size clue
def prefill_board(board, clues, size):
    for y in range(4):  # iterating trough clues
        for x in range(size):
            if (clues[y][x] == size) or (clues[y][x] == 1):
                if y == 0:  # top clues
                    if fill_from_top(board, clues[y][x], x, size) is None:
                        return None
                elif y == 1:  # bottom clues
                    if fill_from_bottom(board, clues[y][x], x, size) is None:
                        return None
                elif y == 2:  # left clues
                    if fill_from_left(board, clues[y][x], x, size) is None:
                        return None
                elif y == 3:  # right clues
                    if fill_from_right(board, clues[y][x], x, size) is None:
                        return None
    return board

# ----------------------------------------------
# ------------- checking functions -------------
# ----------------------------------------------

# next four functions count number of visible boxes from each side, which we will use in next checking functions
# count visible boxes from top view
def count_visible_top(board, column):
    visible_count = 0
    visible_max = 0
    for y in range(len(board)):
        if board[y][column] > visible_max:
            visible_max = board[y][column]
            visible_count += 1
    return visible_count


# count visible boxes from bottom view
def count_visible_bottom(board, column):
    visible_count = 0
    visible_max = 0
    for y in range(len(board) - 1, -1, -1):
        if board[y][column] > visible_max:
            visible_max = board[y][column]
            visible_count += 1
    return visible_count


# count visible boxes from left view
def count_visible_left(board, row):
    visible_count = 0
    visible_max = 0
    for x in range(len(board)):
        if board[row][x] > visible_max:
            visible_max = board[row][x]
            visible_count += 1
    return visible_count


# count visible boxes from right view
def count_visible_right(board, row):
    visible_count = 0
    visible_max = 0
    for x in range(len(board) - 1, -1, -1):
        if board[row][x] > visible_max:
            visible_max = board[row][x]
            visible_count += 1
    return visible_count


# check if row is full of non-zero numbers
def row_is_full(board, row):
    for x in range(len(board)):
        if board[row][x] == 0:
            return False
    return True


# check if column is full of non-zero numbers
def column_is_full(board, column):
    for y in range(len(board)):
        if board[y][column] == 0:
            return False
    return True


# next two functions work only if row or column is full
# checking if left and right clues are satisfied, number of visible boxes has to be equal to given clue
def check_row_clues(board, clues, row):
    return (count_visible_left(board, row) == clues[2][row]) and (count_visible_right(board, row) == clues[3][row])


# checking if top and bottom clues are satisfied, number of visible boxes has to be equal to given clue
def check_column_clues(board, clues, column):
    return (count_visible_top(board, column) == clues[0][column]) and (count_visible_bottom(board, column) == clues[1][column])


# we are filling board from top left corner, so we can check in process of filling top and left clues
# if there are more visible boxes than it is allowed, functions return False, True otherwise
def check_top_clue(board, clues, column):
    return count_visible_top(board, column) > clues[0][column]


def check_left_clue(board, clues, row):
    return count_visible_left(board, row) > clues[2][row]


# checking if number that we are trying to put in box is already in row
def nb_in_row(board, row, column, nb):
    for x in range(len(board)):
        if board[row][x] == nb and x != column:
            return True
    return False


# checking if number that we are trying to put in box is already in column
def nb_in_col(board, row, column, nb):
    for y in range(len(board)):
        if board[y][column] == nb and y != row:
            return True
    return False


# validation for given number in box with all checking functions above
# if all conditions are satisfied, given number is possible on the position on the board
def validate(board, clues, row, column, nb):
    if nb_in_row(board, row, column, nb):
        return False
    if nb_in_col(board, row, column, nb):
        return False
    if check_top_clue(board, clues, column):
        return False
    if check_left_clue(board, clues, row):
        return False
    if row_is_full(board, row):
        if not check_row_clues(board, clues, row):
            return False
    if column_is_full(board, column):
        if not check_column_clues(board, clues, column):
            return False
    return True


# find first zero box in board, searching from top left corner
def find_zero(board, size):
    for y in range(size):
        for x in range(size):
            if board[y][x] == 0:
                return y, x
    return None


# solving function goes through all zero boxes and tries all possible numbers
def solve(board, clues, size):
    if find_zero(board, size) is None:  # find next zero box
        return board  # if all boxes are filled with non-zero numbers, puzzle is solved
    row, column = find_zero(board, size)
    for nb in range(1, size + 1):
        board[row][column] = nb  # set number on position we are trying to fill
        if validate(board, clues, row, column, nb):  # if number satisfies all conditions, go to next zero box
            if solve(board, clues, size) is not None:
                return board
            board[row][column] = 0
        else:  # if number is not possible on position try another
            board[row][column] = 0
    return None  # if there is no possible combination, that means clues are incorrect and return None


# user input of size of the puzzle and clues
def input_clues():
    while True:
        size = input("Enter size of board: ")
        if size.isdigit():
            size = int(size)
            break
        else:
            print("Invalid character! Please enter number!")

    print(f"Clues for {size}x{size} board")
    clues = [[0 for i in range(size)] for j in range(4)]  # initialize array for clues
    for y in range(4):  # fill array of clues
        if y == 0:
            print("Enter top clues:")
        elif y == 1:
            print("Enter bottom clues:")
        elif y == 2:
            print("Enter left clues:")
        elif y == 3:
            print("Enter right clues:")
        for x in range(size):
            while True:
                nb = input()
                if nb.isdigit():
                    nb = int(nb)
                    if 0 < nb <= size:
                        clues[y][x] = nb
                        break
                    else:
                        print(f"Invalid input! Number is not in range {1} to {size}")
                else:
                    print("Invalid character! Please enter number!")
    return clues


def puzzle_solver():
    clues = input_clues()
    size = len(clues[0])
    board = init_board(size)
    prefilled = prefill_board(board, clues, size)
    if prefilled is None:
        print("Puzzle not possible with given clues :(")
    else:
        solution = solve(prefilled, clues, size)
        if solution is None:
            print("Puzzle not possible with given clues :(")
        else:
            print("Solution")
            print_board(solution, size)


if __name__ == '__main__':
    another = 'y'
    while another == 'y':
        puzzle_solver()
        another = input("Do you want to solve another? Press y for another, any key otherwise\n")
