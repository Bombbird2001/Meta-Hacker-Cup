from typing import List


traversals = 0


def get_max_passengers_up_to_2_flights(curr_index: int, target_index: int, passengers: int, step: int,
                                       adj_list: List[List[tuple[int, int]]], all_nodes: List[int]):
    if curr_index == target_index and step > 0:
        # Ignore if traverses back to start index
        return
    if step == 0:
        for destination, max_pass in adj_list[curr_index]:
            # Direct flight - add capacity * 2 for two daily flights
            all_nodes[destination] += max_pass * 2
            # Continue to 2nd step from this destination
            get_max_passengers_up_to_2_flights(destination, target_index, max_pass,
                                               step + 1, adj_list, all_nodes)
    if step == 1:
        for destination, max_pass in adj_list[curr_index]:
            # Reached after 2 flights - add minimum of capacity of first flight and this flight
            all_nodes[destination] += min(passengers, max_pass)


def max_passengers(start_index: int, target_index: int, adj_list: List[List[tuple[int, int]]], cache: dict) -> int:
    list_to_use = []
    # print("----------------\n{} {}".format(start_index, target_index))
    if target_index in cache:
        list_to_use = cache[target_index]
        # print(list_to_use)
        # print(cache)
        # print("Cache found for {}".format(target_index))
        return list_to_use[start_index]
    elif start_index in cache:
        list_to_use = cache[start_index]
        # print(list_to_use)
        # print(cache)
        # print("Cache found for {}".format(start_index))
        return list_to_use[target_index]
    if len(list_to_use) == 0:
        list_to_use = [0 for _ in range(len(adj_list))]
        # Empty list: no cache found, perform search
        get_max_passengers_up_to_2_flights(target_index, target_index, 1000000000, 0, adj_list, list_to_use)
        cache[target_index] = list_to_use
    return list_to_use[start_index]


def traverse(curr_index: int, target_index: int, passengers: int, step: int, adj_list: [List[List[int]]], cache: dict) -> int:
    global traversals
    traversals += 1
    print(traversals)
    if step == 0:
        # At initial departure airport, search through all connected edges
        total_count = 0
        for destination, max_pass in adj_list[curr_index]:
            if destination == target_index:
                total_count += max_pass * 2  # Travel directly to destination from origin, add 2x capacity for 2 flights
            # Will reach an intermediate destination, continue traversing
            total_count += traverse(destination, target_index, min(passengers, max_pass), step + 1, adj_list)
        return total_count
    # Reached an intermediate destination in step 1
    if step == 1:
        for destination, max_pass in adj_list[curr_index]:
            if destination == target_index:
                # Destination reached in 2 steps, return the minimum of the previous flight capacity and this flight
                return min(max_pass, passengers)
    # No destinations found from intermediate airport, return 0
    return 0


with open("D_output.txt", "w+") as of:
    with open("second_flight_validation_input.txt", "r") as f:
        cases = int(f.readline().strip())
        total_cache_hit = 0
        for i in range(cases):
            airports, flights, days = tuple(map(int, f.readline().strip().split(" ")))
            adjacency_list = [[] for _ in range(airports)]
            for j in range(flights):
                start, end, capacity = tuple(map(int, f.readline().strip().split(" ")))
                adjacency_list[start - 1].append((end - 1, capacity))
                adjacency_list[end - 1].append((start - 1, capacity))
            case_cache = {}
            days_res = []
            for k in range(days):
                start, end = tuple(map(int, f.readline().strip().split(" ")))
                # key = "{}-{}".format(start if start < end else end, end if start < end else start)
                # res = None
                # if key in case_cache:
                #     res = case_cache[key]
                #     total_cache_hit += 1
                #     print("Cache hit {}".format(total_cache_hit))
                # if res is None:
                #     res = max_passengers(start - 1, end - 1, adjacency_list, case_cache)
                #     case_cache[key] = res
                res = max_passengers(start - 1, end - 1, adjacency_list, case_cache)
                days_res.append(str(res))
                # print("Day {} done".format(k))
            if i > 0:
                of.write("\n")
            of.write("Case #{}: {}".format(i + 1, " ".join(days_res)))
