from solver import criteria_function, process_for_all_words, sort_relevance
from functools import partial

valid_results = 'vwa'

def check_result_valid(rst: str) -> bool:
    for c in rst:
        if c not in valid_results:
            return False
    return True


if __name__ == "__main__":
    guess_number = 0
    guess = '.....'
    result = '.....'
    required = '.....'
    l_to_max_count: dict[str, int] = {}
    wrong: list[tuple[str, int]] = []
    while guess_number < 6 and result != 'vvvvv':
        inh = 1
        while len(guess) != 5 or inh:
            guess = input(f'\nWhat is your {"next "*bool(guess_number)}guess?  ')
            inh=0

        inh = 1
        while len(result) != 5 or inh or not check_result_valid(result):
            result = input(f'What was the result of it (v/w/a)?  ')
            inh = 0

        for i, l in enumerate(result):
            match l:
                case 'v':
                    required = required[:i] + guess[i] + required[i+1:]
                case 'w':
                    wrong.append((guess[i], i))
                case 'a':
                    l_to_max_count[guess[i]] = guess.count(guess[i])
                    for k in range(len(guess)):
                        if result[k] == 'a' and guess[k] == guess[i]:
                            l_to_max_count[guess[i]] -= 1


        func = partial(criteria_function,
                       required=required,
                       l_to_max_count=l_to_max_count,
                       wrong=wrong)

        print("List of possible words:")
        words = sort_relevance(process_for_all_words(func))
        str_nxt = "\n\nBest words for next guess:"
        for w in words[:10]:
            str_nxt += f'\t{w}'
        print(str_nxt)

        guess_number += 1
