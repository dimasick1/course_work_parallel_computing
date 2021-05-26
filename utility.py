from matplotlib import pyplot
from pathlib import Path
from time import time
import re
import json


def generate_pattern():
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


def generate_paths(path, pattern):
    len_path = len(str(path))
    paths = [file for file in path.rglob('*.txt') if re.search(pattern, str(file)[len_path:])]

    return paths


def draw_results(processes, timestamps):
    figure = pyplot.figure()
    subplot = figure.add_subplot()
    subplot.set_xlabel('Processes')
    subplot.set_ylabel('Time(s)')
    subplot.set_title("Time(process count)", fontsize=15)
    subplot.grid(True)
    subplot.plot(processes, timestamps)
    subplot.plot(processes, timestamps, 'ro', color='pink')
    path = Path(__file__).parent.absolute()
    pyplot.savefig(str(path.parent.absolute()) + f"/Graphs/{time()}.png")


def write_index_to_json(index_dict):
    for key, value in index_dict.items():
        index_dict[key] = list(value)

    c_path = Path.joinpath(Path(), Path('index.json'))
    c_path.write_text(json.dumps(index_dict), encoding='utf-8')
