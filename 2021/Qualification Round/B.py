import copy
from typing import List


def immediate_win(board: List[List[str]]) -> tuple[int, int]:
    min_count = None
    min_boards = []
    for row_index, _ in enumerate(board):
        blank_count = 0
        failed = False
        board_copy = copy.deepcopy(board)
        for column_index, tile in enumerate(board_copy[row_index]):
            if tile == "O":
                # Impossible to win in this row
                failed = True
                break
            if tile == ".":
                # Add to empty count
                blank_count += 1
                # Change to X
                board_copy[row_index][column_index] = "X"
        if not failed:
            # print("Row blank count " + str(blank_count))
            if min_count is None or blank_count < min_count:
                min_count = blank_count
                min_boards.clear()
                complete = get_complete_rows(board_copy)
                min_boards.append(complete)
            elif blank_count == min_count:
                complete = get_complete_rows(board_copy)
                if complete not in min_boards:
                    min_boards.append(complete)
    for column_index in range(len(board)):
        blank_count = 0
        failed = False
        board_copy = copy.deepcopy(board)
        for row_index in range(len(board)):
            tile = board_copy[row_index][column_index]
            if tile == "O":
                # Impossible to win in this column
                failed = True
                break
            if tile == ".":
                # Add to empty count
                blank_count += 1
                # Change to X
                board_copy[row_index][column_index] = "X"
        if not failed:
            # print("Column blank count " + str(blank_count))
            if min_count is None or blank_count < min_count:
                min_count = blank_count
                min_boards.clear()
                complete = get_complete_rows(board_copy)
                min_boards.append(complete)
            elif blank_count == min_count:
                complete = get_complete_rows(board_copy)
                if complete not in min_boards:
                    min_boards.append(complete)
    return min_count, len(min_boards)


def get_complete_rows(board: List[List[str]]) -> str:
    string_rep = ""
    for row_index, row in enumerate(board):
        failed = False
        for tile in row:
            if tile != "X":
                failed = True
                break
        if not failed:
            string_rep += "r" + str(row_index)
    for col_index in range(len(board)):
        failed = False
        for row_index in range(len(board)):
            if board[row_index][col_index] != "X":
                failed = True
                break
        if not failed:
            string_rep += "c" + str(col_index)
    # print(string_rep)
    return string_rep


with open("B_output.txt", "w+") as of:
    with open("xs_and_os_input.txt", "r") as f:
        cases = int(f.readline().strip())
        for i in range(cases):
            board_size = int(f.readline().strip())
            new_board = []
            for j in range(board_size):
                new_board.append(list(f.readline().strip()))
            result = immediate_win(new_board)
            if i > 0:
                of.write("\n")
            if result[0] is None:
                of.write("Case #{}: Impossible".format(i + 1))
            else:
                of.write("Case #{}: {} {}".format(i + 1, result[0], result[1]))
