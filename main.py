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
    while True:
        num_of_threads = input('Enter num of threads or "quit" if you want to see the results: ')

        if num_of_threads == 'quit':
            break

        num_of_threads = int(num_of_threads)

        start = time.time()
        index_dicts.append(indexer.create_index(path, paths, num_of_threads))
        end = time.time() - start

        results.append((num_of_threads, end))

        print(f'Time for {num_of_threads} threads: {end}')
          
    draw_results(results, num_of_files)
    print('Sameness check: ', sameness_dict_check(index_dicts))

    write_index_to_json(index_dicts[0])


if __name__ == '__main__':
    main()

