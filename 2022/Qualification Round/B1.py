from typing import List


def have_tree_friends(tree_map: List[str]) -> tuple[bool, List[str]]:
    if len(tree_map) == 1 or len(tree_map[0]) == 1:
        for row in tree_map:
            for tile in row:
                if tile == "^":
                    # Tree found on a 1 x N or N x 1 map, not possible
                    return False, []
        # No trees at all in this map
        return True, tree_map
    # At least size 2 x 2, possible as long as all tiles are filled
    each_row = "^" * len(tree_map[0])
    return True, [each_row for _ in range(len(tree_map))]


with open("B1_output.txt", "w+") as of:
    with open("second_friend_input.txt", "r+") as f:
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
