import copy
from typing import List

swap_table = [[False for _ in range(26)] for _ in range(26)]


def pre_compute_swap_count(transformation_list):
    travel_graph = [[0 for _ in range(26)] for _ in range(26)]
    # Map all transformations to their start letter
    for trans in transformation_list:
        from_index = ord(trans[0]) - 65
        to_index = ord(trans[1]) - 65
        travel_graph[from_index][to_index] = 1
    for k in range(26):
        traverse_graph(k, k, travel_graph, 0, [False for _ in range(26)], [])


def traverse_graph(start_index, curr_index, travel_graph, steps, travelled_list, travel_queue: List[tuple[int, int]]):
    can_go = travel_graph[curr_index]
    travelled_list[curr_index] = True
    curr_val = swap_table[start_index][curr_index]
    if curr_val == False or curr_val > steps:
        swap_table[start_index][curr_index] = steps
    for to_index, step in enumerate(can_go):
        if step == 0:
            # No path, skip
            continue
        if travelled_list[to_index]:
            # Already traversed, skip
            continue
        travel_queue.append((to_index, steps))
    while len(travel_queue) > 0:
        next_travel = travel_queue[0]
        travel_queue.pop(0)
        traverse_graph(start_index, next_travel[0], travel_graph, next_travel[1] + 1, travelled_list, travel_queue)


def traverse(curr_index, target_index, travel_graph, travelled_list, depth):
    # print("{} {} {} {}".format(curr_index, target_index, depth, travelled_list))
    if swap_table[curr_index][target_index] != False:
        return swap_table[curr_index][target_index]
    if target_index == curr_index:
        # print("Found, returning 0")
        return 0
    if travelled_list[curr_index]:
        # Already travelled, skip
        return None
    min_steps = None
    can_travel = travel_graph[curr_index]
    travelled_list[curr_index] = True
    for to_index, value in enumerate(can_travel):
        if value == 0:
            continue
        # print("Spawning " + str(to_index) + " from depth " + str(depth))
        steps_needed = traverse(to_index, target_index, travel_graph, copy.copy(travelled_list), depth + 1)
        if steps_needed == 0:
            min_steps = 0
            break
        if min_steps is None or (steps_needed is not None and steps_needed < min_steps):
            min_steps = steps_needed
    final_res = None if min_steps is None else 1 + min_steps
    swap_table[curr_index][target_index] = final_res
    return final_res


def make_consistent(string_to_change):
    min_steps = None
    for target_index in range(26):
        cum_steps = 0
        failed = False
        for c in string_to_change:
            curr_index = ord(c) - 65
            if curr_index == target_index:
                continue
            path_steps = swap_table[curr_index][target_index]
            if path_steps == False:
                # No path found, skip this letter
                failed = True
                break
            cum_steps += path_steps
        if failed:
            continue
        if min_steps is None or cum_steps < min_steps:
            min_steps = cum_steps
        print(cum_steps)
    print("Min step: " + str(min_steps))
    return min_steps if min_steps is not None else -1
    # min_steps = None
    # for target_index in range(26):
    #     cum_steps = 0
    #     failed = False
    #     for c in string_to_change:
    #         curr_index = ord(c) - 65
    #         # Search cache first
    #         # res = None
    #         if curr_index == target_index:
    #             continue
    #         if swap_table[curr_index][target_index] == False:
    #             # Cache not found, perform traverse
    #             res = traverse(curr_index, target_index, travel_graph, [False for _ in range(26)], 0)
    #             swap_table[curr_index][target_index] = res
    #             # print("{} to {}: {}".format(curr_index, target_index, res))
    #         else:
    #             res = swap_table[curr_index][target_index]
    #         if res is None:
    #             # Cannot be changed to letter, skip this letter
    #             failed = True
    #             break
    #         cum_steps += res
    #     if failed:
    #         continue
    #     if min_steps is None or cum_steps < min_steps:
    #         min_steps = cum_steps
    # return min_steps if min_steps is not None else -1


with open("A2_output.txt", "w+") as of:
    # TODO pre-compute shortest distance from one letter to another with BFS
    with open("consistency_chapter_2_input.txt") as f:
        no = int(f.readline().strip())
        case = 0
        for i in range(no):
            string = f.readline().strip()
            transNo = int(f.readline().strip())
            transList = []
            for j in range(transNo):
                transList.append(f.readline().strip())
            swap_table = [[False for _ in range(26)] for _ in range(26)]
            pre_compute_swap_count(transList)
            print(swap_table)
            result = make_consistent(string)
            case += 1
            if case > 1:
                of.write("\n")
            of.write("Case #" + str(case) + ": " + str(result))
