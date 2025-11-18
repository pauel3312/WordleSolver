from collections.abc import Generator, Callable
from copy import deepcopy
from typing import Optional
from functools import partial

def next_word() -> Generator[str]:
    f = open('wordle_word_list.txt', 'r')
    current_word = f.readline()
    while current_word:
        yield current_word.rstrip('\n')
        current_word = f.readline()
    f.close()

def criteria_function(word: str,
                      required: str,
                      l_to_max_count: dict[str, int],
                      wrong: list[tuple[str, int]]) -> Optional[str]:
    for i, l in enumerate(required):
        if l == '.':
            continue
        if word[i] != l:
            return None

    wc = wrong.copy()
    lmc_calc = deepcopy(l_to_max_count)
    for i, l in enumerate(word):
        if l in lmc_calc.keys():
            if lmc_calc[l] == 0:
                return None
            if lmc_calc[l] > 0:
                lmc_calc[l] -= 1

        if (l, i) in wrong:
            return None
        j = len(wc) - 1
        while j >= 0:
            if l == wc[j][0]:
                wc.pop(j)
            j -= 1

    if len(wc) != 0:
        return None
    return word


def process_for_all_words(func: Callable[[str], Optional[str]], disp: bool = True) -> list[str]:
    ow = '.....'
    rt = []
    for w in next_word():
        if func(w) is not None:
            rt.append(w)
            if disp:
                if w[0] != ow[0]:
                    print('\n' + w[0], end='\t')
                print(w, end="\t")
                ow = w
    return rt

def word_to_score(word: str, letters_scores: dict[str, int]) -> int:
    s = 0
    for i, l in enumerate(word):
        if l not in word[:i]:
            s += letters_scores[l]
    return s

def sort_relevance(words: list[str]) -> list[str]:
    char_to_n_map: dict[str, int] = {}
    for i in range(26):
        char_to_n_map[chr(i+97)] = 0
    for w in words:
        for c in w:
            char_to_n_map[c] += 1
    key = partial(word_to_score, letters_scores = char_to_n_map)

    return sorted(words, key = key, reverse = True)

if __name__ == '__main__':
    print(sort_relevance(process_for_all_words(lambda w: w, False)))

