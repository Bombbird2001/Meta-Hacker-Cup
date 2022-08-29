from typing import List


def have_tree_friends(tree_map: List[str]) -> tuple[bool, List[str]]:
    if len(tree_map) == 1 or len(tree_map[0]) == 1:
        for each_row in tree_map:
            for tile in each_row:
                if tile == "^":
                    # Tree found on a 1 x N or N x 1 map, not possible
                    return False, []
        # No trees at all in this map
        return True, tree_map
    # At least size 2 x 2, fill all non-rock spots with trees and then remove trees without at least 2 friends
    all_rows = []
    for each_row in tree_map:
        row_list = []
        for tile in each_row:
            if tile == "#":
                row_list.append("#")
            else:
                row_list.append("^")
        all_rows.append(row_list)
    # Loop through all tiles and check if any trees have less than 2 friends
    for (row_index, each_row) in enumerate(all_rows):
        for (col_index, tile) in enumerate(each_row):
            check_have_2_or_more_friends(row_index, col_index, all_rows)
    # After removing trees without at least 2 friends, check the original provided map with the new map
    for (row_index, each_row) in enumerate(tree_map):
        for (col_index, tile) in enumerate(each_row):
            if tile == "^" and all_rows[row_index][col_index] != "^":
                return False, []
    return True, list(map("".join, all_rows))


def check_have_2_or_more_friends(row_index: int, col_index: int, tree_map: List[List[str]]):
    if row_index < 0 or row_index >= len(tree_map) or col_index < 0 or col_index >= len(tree_map[0]):
        return  # Ignore out of bounds
    if tree_map[row_index][col_index] != "^":
        return  # Ignore rocks
    friend_count = 0
    if row_index > 0 and tree_map[row_index - 1][col_index] == "^":
        friend_count += 1
    if row_index < len(tree_map) - 1 and tree_map[row_index + 1][col_index] == "^":
        friend_count += 1
    if col_index > 0 and tree_map[row_index][col_index - 1] == "^":
        friend_count += 1
    if col_index < len(tree_map[row_index]) - 1 and tree_map[row_index][col_index + 1] == "^":
        friend_count += 1
    if friend_count >= 2:
        return
    # If less than 2 friends, remove this tree, and check for all surrounding tiles
    tree_map[row_index][col_index] = "."
    check_have_2_or_more_friends(row_index - 1, col_index, tree_map)
    check_have_2_or_more_friends(row_index + 1, col_index, tree_map)
    check_have_2_or_more_friends(row_index, col_index - 1, tree_map)
    check_have_2_or_more_friends(row_index, col_index + 1, tree_map)


with open("B2_output.txt", "w+") as of:
    with open("second_second_friend_input.txt", "r+") as f:
        test_cases = int(f.readline().strip())
        for i in range(test_cases):
            row_col = tuple(map(int, f.readline().strip().split(" ")))
            map_list = []
            for _ in range(row_col[0]):
                map_list.append(f.readline().strip())
            if i > 0:
                of.write("\n")
            res = have_tree_friends(map_list)
            of.write("Case #{}: {}".format(i + 1, "Possible" if res[0] else "Impossible"))
            if res[0]:
                for row in res[1]:
                    of.write("\n" + row)
