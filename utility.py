from pathlib import Path
from matplotlib import pyplot
import re
import json


def generate_path_pattern() -> str:
    pattern_dir = [r"/\w+/\w{3}/", r"/\w+/\w{5}/", r"_\d+.txt", ]
    pattern_range1 = [r"7[2][5-9]\d", r"7[34]\d{2}", ]
    pattern_range2 = [r"29\d{3}", ]

    pattern = '^'
    for ptr in pattern_range1:
        pattern += '(' + pattern_dir[0] + ptr + pattern_dir[2] + ')' + '|'

    for ptr in pattern_range2:
        pattern += '(' + pattern_dir[1] + ptr + pattern_dir[2] + ')' + '|'

    pattern = pattern[:-1] + '$'

    return pattern


def generate_list_of_paths(path: Path, pattern: str) -> list:
    len_path = len(str(path))
    paths = [file for file in path.rglob('*.txt') if re.search(pattern, str(file)[len_path:])]

    return paths


def draw_results(results: list, num_of_files: int) -> None:
    array_x = [elem[0] for elem in results]
    array_y = [elem[1] for elem in results]

    figure = pyplot.figure()
    ax = figure.add_subplot()
    # ax.set_xticks([num for num in range(len(array_x))])
    # ax.set_yticks(array_y)
    ax.set_xlabel('num of threads')
    ax.set_ylabel('time')
    ax.set_title(str(num_of_files), fontsize=15)
    ax.grid(True)
    ax.plot(array_x, array_y)
    ax.plot(array_x, array_y, 'ro', color='r')
    pyplot.show()


def sameness_dict_check(dicts: list) -> bool:
    c_dict = dicts[0]

    for dct in dicts[1:]:
        if c_dict != dct:
            return False

    return True


def write_index_to_json(index_dict: dict, path: Path = Path()) -> None:
    for key, value in index_dict.items():
        index_dict[key] = list(value)

    c_path = Path.joinpath(path, Path('index.json'))
    c_path.write_text(json.dumps(index_dict), encoding='utf-8')



 
