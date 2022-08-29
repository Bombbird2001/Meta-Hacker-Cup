import copy
from typing import List
import itertools
import bisect


def get_other_words(code_words: List[str], max_size: int, count_needed: int):
    if max_size <= 0:
        return
    for possible in itertools.product([".", "-"], repeat=max_size):
        possible_word = "".join(possible)
        if not can_be_made_with_existing_code(code_words, possible_word):
            bisect.insort_left(code_words, possible_word, key=lambda x: -len(x))
        if len(code_words) >= count_needed:
            return


def can_be_made_with_existing_code(code_words: List[str], new_word: str) -> bool:
    test_queue = [new_word]
    split_index = 0
    while len(test_queue) > 0:
        to_split = test_queue[0]
        code_to_split = code_words[split_index]
        after_split_words_left = filter(lambda x: len(x) > 0, to_split.split(code_to_split))
        test_queue.pop(0)
        test_queue.extend(after_split_words_left)
        split_index += 1
        if len(test_queue) == 0:
            return True  # Can be formed by a sequence of existing keywords
        if split_index >= len(code_words):
            return False  # No code words can form the sequence


def get_other_possible_code_words(curr_code_word: str, curr_index: int, word_to_modify: List[str],
                                  word_list: List[str], required_count: int) -> List[str]:
    if len(word_list) >= required_count:
        return word_list
    if curr_index >= len(word_to_modify):
        original_word_joined = "".join(word_to_modify)
        if curr_code_word not in original_word_joined:
            word_list.append(original_word_joined)
        return word_list
    word_modified = copy.copy(word_to_modify)
    word_modified[curr_index] = "-"
    get_other_possible_code_words(curr_code_word, curr_index + 1, word_to_modify, word_list, required_count)
    get_other_possible_code_words(curr_code_word, curr_index + 1, word_modified, word_list, required_count)
    return word_list


with open("C1_output.txt", "w+") as of:
    with open("second_meaning_validation_input.txt", "r") as f:
        test_cases = int(f.readline().strip())
        for i in range(test_cases):
            count = int(f.readline().strip())
            word = f.readline().strip()
            res = [word]
            init_count = 10
            while len(res) < count:
                get_other_words(res, init_count, count)
                init_count -= 1
            if i > 0:
                of.write("\n")
            of.write("Case #{}:".format(i + 1))
            res.remove(word)
            for j in range(count - 1):
                of.write("\n")
                of.write(res[j])
