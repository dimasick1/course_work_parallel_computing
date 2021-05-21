from threading import Thread
from pathlib import Path
from math import ceil
import time

class Indexer:
    def __init__(self):
        self.index_dict = {}

    @staticmethod
    def _parse_file(path: Path) -> set:
        symbols = ['.', ',', ';', '(', ')', '[', ']', ':', '?', '!', '<' '>' '\\', '/', '*', '"']
        text = path.read_text('utf-8').lower()

        for symbol in symbols:
            text = text.replace(symbol, '')

        return set(text.split())

    @staticmethod
    def _generate_file_id(file_path: Path, dir_path_len: int) -> int:
        match_dict = {
            'test': '1',
            'train': '2',
            'neg': '1',
            'pos': '2',
            'unsup': '3',
        }

        d1, d2, file_name = str(file_path)[dir_path_len + 1:].split('/')
        file_id = match_dict[d1] + match_dict[d2] + file_name.split('_')[0]

        return int(file_id)

    def create_index(self, dir_path: Path, list_of_paths: list, num_of_threads: int = 1) -> dict:
        dir_path_len = len(str(dir_path))

        if num_of_threads - 1:
            dicts_list = [dict() for _ in range(num_of_threads)]

            offset = int(ceil(len(list_of_paths) / num_of_threads))
            threads = []

            for i in range(num_of_threads):
                threads.append(Thread(target=self._create_index_dict,
                                      args=(list_of_paths[offset * i: offset * (i + 1)], dir_path_len, dicts_list[i])))

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            self.index_dict = self._merge(dicts_list)
        else:
            self.index_dict = self._create_index_dict(list_of_paths, dir_path_len, {})
            time.sleep(0.5)

        return self.index_dict

    @staticmethod
    def _merge(dicts_list: list) -> dict:
        main_dict = dicts_list[0]

        for dct in dicts_list[1:]:
            for lexeme, files_ids in dct.items():
                try:
                    main_dict[lexeme].update(files_ids)
                except KeyError:
                    main_dict[lexeme] = files_ids

        return main_dict

    def _create_index_dict(self, list_of_paths: list, dir_path_len: int, c_dict: dict) -> dict:
        for path in list_of_paths:
            file_id = self._generate_file_id(path, dir_path_len)
            lexemes = self._parse_file(path)

            for lexeme in lexemes:
                try:
                    c_dict[lexeme].add(file_id)
                except KeyError:
                    c_dict[lexeme] = {file_id, }

        return c_dict
