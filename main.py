import time

def print_board(board_to_print, size):
    for y in range(size):
        for x in range(size):
            print(board_to_print[y][x], end=' ')
        print()


def print_clues(board_to_print, size):
    for y in range(4):
        for x in range(size):
            print(board_to_print[y][x], end=' ')
        print()


def init_board(board_size):
    new_board = [[0 for i in range(board_size)] for j in range(board_size)]
    return new_board


def fill_from_top(board, clue, column, size):
    for y in range(clue):
        board[y][column] = (size + 1) - clue + y


def fill_from_bottom(board, clue, column, size):
    for y in range(clue):
        board[size - 1 - y][column] = (size + 1) - clue + y


def fill_from_left(board, clue, row, size):
    for x in range(clue):
        board[row][x] = (size + 1) - clue + x


def check_column_clues(board, clues, column):
    return (count_visible_top(board, column) == clues[0][column]) and (count_visible_bottom(board, column) == clues[1][column])


def check_top_clue(board, clues, column):
    return count_visible_top(board, column) > clues[0][column]


def check_left_clue(board, clues, row):
    return count_visible_left(board, row) > clues[2][row]


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

def solve(board, clues, size):
    if find_zero(board, size) is None:
        return board
    row, column = find_zero(board, size)
    for nb in range(1, size + 1):
        board[row][column] = nb
        # print_board(board, size)
        # print()
        if validate(board, clues, row, column, nb):
            if solve(board, clues, size) is not None:
                return board
            board[row][column] = 0
        else:
            board[row][column] = 0
    return None


def fill_from_right(board, clue, row, size):
    for x in range(clue):
        board[row][size - 1 - x] = (size + 1) - clue + x


def prefill_board(board, clues):
    for y in range(4):
        for x in range(len(board)):
            if (clues[y][x] == size) or (clues[y][x] == 1):
                if y == 0:
                    fill_from_top(board, clues[y][x], x, size)
                elif y == 1:
                    fill_from_bottom(board, clues[y][x], x, size)
                elif y == 2:
                    fill_from_left(board, clues[y][x], x, size)
                elif y == 3:
                    fill_from_right(board, clues[y][x], x, size)


def find_zero(board, size):
    for y in range(size):
        for x in range(size):
            if board[y][x] == 0:
                return y, x
    return None


def nb_in_row(board, row, column, nb):
    for x in range(len(board)):
        if board[row][x] == nb and x != column:
            return True
    return False


def nb_in_col(board, row, column, nb):
    for y in range(len(board)):
        if board[y][column] == nb and y != row:
            return True
    return False


def count_visible_top(board, column):
    visible_count = 0
    visible_max = 0
    for y in range(len(board)):
        if board[y][column] > visible_max:
            visible_max = board[y][column]
            visible_count += 1
    return visible_count


def count_visible_bottom(board, column):
    visible_count = 0
    visible_max = 0
    for y in range(len(board) - 1, -1, -1):
        if board[y][column] > visible_max:
            visible_max = board[y][column]
            visible_count += 1
    return visible_count


def count_visible_left(board, row):
    visible_count = 0
    visible_max = 0
    for x in range(len(board)):
        if board[row][x] > visible_max:
            visible_max = board[row][x]
            visible_count += 1
    return visible_count


def count_visible_right(board, row):
    visible_count = 0
    visible_max = 0
    for x in range(len(board) - 1, -1, -1):
        if board[row][x] > visible_max:
            visible_max = board[row][x]
            visible_count += 1
    return visible_count


def row_is_full(board, row):
    for x in range(len(board)):
        if board[row][x] == 0:
            return False
    return True


def column_is_full(board, column):
    for y in range(len(board)):
        if board[y][column] == 0:
            return False
    return True


def check_row_clues(board, clues, row):
    return (count_visible_left(board, row) == clues[2][row]) and (count_visible_right(board, row) == clues[3][row])


if __name__ == '__main__':
    start_time = time.time()
    # clues = [[1, 2, 3, 3], [3, 3, 1, 2], [1, 2, 4, 2], [4, 2, 1, 2]]
    clues = [[2, 4, 4, 3, 1, 2, 4, 4, 3], [4, 4, 3, 1, 3, 4, 2, 2, 4], [2, 1, 2, 4, 2, 3, 4, 5, 3], [2, 4, 2, 1, 5, 3, 2, 3, 3]]
    # clues = [[2, 3, 1, 2, 3], [2, 2, 3, 2, 1], [2, 1, 2, 2, 2], [3, 5, 4, 2, 1]]
    # clues = [[2, 4, 2, 3, 5, 1], [2, 2, 2, 3, 1, 4], [3, 1, 3, 3, 2, 2], [1, 4, 2, 2, 3, 2]]  # 6x6
    size = len(clues[0])
    board = init_board(size)
    prefill_board(board, clues)

    #6x6
    # board[0][4] = 2
    # board[2][5] = 2
    # board[3][2] = 6
    # board[3][4] = 4
    # board[5][2] = 2
    # board[5][5] = 3

    #9x9
    board[0][2] = 3
    board[0][5] = 4
    board[0][7] = 2
    board[1][2] = 7
    board[1][3] = 8
    board[2][2] = 4
    board[2][3] = 6
    board[2][4] = 3
    board[2][6] = 5
    board[3][3] = 7
    board[3][4] = 2
    board[3][7] = 4
    board[4][0] = 6
    board[4][5] = 8
    board[5][0] = 2
    board[5][5] = 5
    board[5][6] = 3
    board[6][5] = 2
    board[6][8] = 1
    # board[7][1] = 3
    # board[7][2] = 6




    print_board(solve(board, clues, size), size)
    print("--- %s seconds ---" % (time.time() - start_time))
