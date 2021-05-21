 import time

from indexer import Indexer
from utility import *


def main() -> None:
    dir_path = '/home/demon/Desktop/course_work_parallel_computing/datasets/aclImdb'
    path = Path(dir_path)

    pattern = generate_path_pattern()
    paths = generate_list_of_paths(path, pattern)

    num_of_files = len(paths)

    indexer = Indexer()

    results = []
    index_dicts = []
    draw_results(results, num_of_files)
    print('Sameness check: ', sameness_dict_check(index_dicts))

    write_index_to_json(index_dicts[0])


if __name__ == '__main__':
    main()

