import copy
from typing import List


def build_adjacency_matrix(tunnels: List[tuple[int, int]], cave_no: int) -> List[List[int]]:
    matrix = [[0 for _ in range(cave_no)] for _ in range(cave_no)]
    for tunnel in tunnels:
        matrix[tunnel[0]][tunnel[1]] = 1
        matrix[tunnel[1]][tunnel[0]] = 1

    return matrix


def max_ore(matrix: List[List[int]], gold: List[int], repositions: int) -> int:
    count = 0
    # print(matrix)
    if repositions == 0:
        # Special case: If no repositions allowed, only can get from cave 1
        return gold[0]
    for _ in range(repositions + 1):
        res = depth_traverse(matrix, gold, 0, [False for _ in range(len(gold))])
        count += res[0]
        matrix = res[1]
        gold = res[2]
        # print(count, matrix, gold)
    return count


def depth_traverse(matrix: List[List[int]], gold: List[int], curr_cave: int, visited_caves: List[bool])\
        -> tuple[int, List[List[int]], List[int]]:
    # print("Traversing " + str(curr_cave) + " with " + str(matrix))
    can_go = matrix[curr_cave]
    this_gold = gold[curr_cave]
    gold[curr_cave] = 0
    max_gold = 0
    max_matrix = matrix
    max_gold_list = gold
    visited_caves[curr_cave] = True
    for next_cave, tunnel_exists in enumerate(can_go):
        if next_cave == curr_cave:
            # Is this cave, skip
            continue
        if visited_caves[next_cave]:
            # Already visited, skip
            continue
        if tunnel_exists == 0:
            # No tunnel, skip
            continue
        matrix_copy = copy.deepcopy(matrix)
        gold_copy = copy.copy(gold)
        visited_copy = copy.copy(visited_caves)
        # Tunnel is destroyed
        matrix_copy[curr_cave][next_cave] = 0
        matrix_copy[next_cave][curr_cave] = 0
        gold_from_sub_branch = depth_traverse(matrix_copy, gold_copy, next_cave, visited_copy)
        if gold_from_sub_branch[0] > max_gold:
            max_gold = gold_from_sub_branch[0]
            max_matrix = gold_from_sub_branch[1]
            max_gold_list = gold_from_sub_branch[2]
    return this_gold + max_gold, max_matrix, max_gold_list


with open("C2_output.txt", "w+") as of:
    with open("gold_mine_chapter_2_input.txt", "r") as f:
        mines = int(f.readline())
        for i in range(mines):
            caves_and_drills = list(map(int, f.readline().strip().split(" ")))
            caves = caves_and_drills[0]
            drills = caves_and_drills[1]
            tunnel_list = []
            gold_list = list(map(int, f.readline().strip().split(" ")))
            for j in range(caves - 1):
                tunnel_list.append(tuple(map(lambda x: int(x) - 1, f.readline().split(" "))))
            adj_matrix = build_adjacency_matrix(tunnel_list, caves)
            max_ore_count = max_ore(adj_matrix, gold_list, drills)
            if i > 0:
                of.write("\n")
            of.write("Case #{}: {}".format(i + 1, max_ore_count))
