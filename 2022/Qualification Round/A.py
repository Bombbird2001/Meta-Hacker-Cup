from typing import List


def can_hold_parts(max_size: int, parts: List[int]) -> bool:
    if len(parts) > 2 * max_size:
        return False
    style_count = [0 for _ in range(100)]
    for part in parts:
        style_count[part - 1] += 1
        if style_count[part - 1] > 2:
            return False
    return True


with open("A_output.txt", "w+") as of:
    with open("second_hands_input.txt", "r") as f:
        test_cases = int(f.readline().strip())
        for i in range(test_cases):
            n_k = list(map(int, f.readline().strip().split(" ")))
            k = n_k[1]
            part_list = list(map(int, f.readline().strip().split(" ")))
            if i > 0:
                of.write("\n")
            of.write("Case #{}: {}".format(i + 1, "YES" if can_hold_parts(k, part_list) else "NO"))
