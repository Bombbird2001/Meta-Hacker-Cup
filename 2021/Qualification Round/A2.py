import copy


cache = [[False for _ in range(26)] for _ in range(26)]


def build_graph(transformation_list):
    travel_graph = [[0 for _ in range(26)] for _ in range(26)]
    # Map all transformations to their start letter
    for trans in transformation_list:
        from_index = ord(trans[0]) - 65
        to_index = ord(trans[1]) - 65
        travel_graph[from_index][to_index] = 1
    # print(travel_graph)
    return travel_graph
    # for k in range(26):
    #    traverse_graph(k, k, travel_graph, 0, [False for _ in range(26)])


def traverse_graph(start_index, curr_index, travel_graph, steps, travelled_list):
    can_go = travel_graph[curr_index]
    for to_index, step in enumerate(can_go):
        if step == 0:
            # No path, skip
            continue
        if travelled_list[to_index]:
            # Already traversed, skip
            continue
        travel_graph[start_index][to_index] = steps + 1
        travelled_list[to_index] = True
        traverse_graph(start_index, to_index, travel_graph, steps + 1, travelled_list)


def traverse(curr_index, target_index, travel_graph, travelled_list, depth):
    # print("{} {} {} {}".format(curr_index, target_index, depth, travelled_list))
    if cache[curr_index][target_index] != False:
        return cache[curr_index][target_index]
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
    cache[curr_index][target_index] = final_res
    return final_res


def make_consistent(string_to_change, travel_graph):
    min_steps = None
    for target_index in range(26):
        cum_steps = 0
        failed = False
        for c in string_to_change:
            curr_index = ord(c) - 65
            # Search cache first
            # res = None
            if curr_index == target_index:
                continue
            if cache[curr_index][target_index] == False:
                # Cache not found, perform traverse
                res = traverse(curr_index, target_index, travel_graph, [False for _ in range(26)], 0)
                cache[curr_index][target_index] = res
                # print("{} to {}: {}".format(curr_index, target_index, res))
            else:
                res = cache[curr_index][target_index]
            if res is None:
                # Cannot be changed to letter, skip this letter
                failed = True
                break
            cum_steps += res
        if failed:
            continue
        if min_steps is None or cum_steps < min_steps:
            min_steps = cum_steps
    return min_steps if min_steps is not None else -1


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
            graph = build_graph(transList)
            cache = [[False for _ in range(26)] for _ in range(26)]
            result = make_consistent(string, graph)
            case += 1
            if case > 1:
                of.write("\n")
            of.write("Case #" + str(case) + ": " + str(result))
