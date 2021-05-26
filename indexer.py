from pathlib import Path
from math import ceil
from multiprocessing import Process, Manager


class Indexer:
    def __init__(self):
        self.manager = Manager()
        self.index_dict = self.manager.list()

    @staticmethod
    def _parse_file(path):
        symbols = ['.', ',', ';', '(', ')', '[', ']', ':', '?', '!', '<' '>' '\\', '/', '*', '"']
        text = path.read_text('utf-8').lower()

        for symbol in symbols:
            text = text.replace(symbol, '')

        return set(text.split())

    @staticmethod
    def _generate_file_id(file_path, dir_path_len):
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

    def create_index(self, dir_path, list_of_paths, num_of_procs):
        dir_path_len = len(str(dir_path))

        if num_of_procs - 1:
            dicts_list = self.manager.list()

            for i in range(num_of_procs): # with
                dicts_list.append(dict())

            offset = int(ceil(len(list_of_paths) / num_of_procs))
            processes = []

            for i in range(num_of_procs):
                processes.append(Process(target=self._create_index_dict,
                                      args=(list_of_paths[offset * i: offset * (i + 1)], dir_path_len, dicts_list, i)))

            for process in processes:
                process.start()

            for process in processes:
                process.join()

            self.index_dict = self._merge(dicts_list)
        else:
            self.index_dict = self._create_index_dict(list_of_paths, dir_path_len, {}, 1)

        return self.index_dict

    @staticmethod
    def _merge(dicts_list):
        main_dict = dicts_list[0]

        for dct in dicts_list[1:]:
            for lexeme, files_ids in dct.items():
                if main_dict.get(lexeme, False):
                    main_dict[lexeme] += [files_ids]
                else:
                    main_dict[lexeme] = files_ids

        return main_dict

    def _create_index_dict(self, list_of_paths, dir_path_len, dict_list, i):
        local_dict = dict()
        for path in list_of_paths:
            file_id = self._generate_file_id(path, dir_path_len)
            lexemes = self._parse_file(path)

            for lexeme in lexemes:
                if local_dict.get(lexeme, False):
                    local_dict[lexeme].append(file_id)
                else:
                    local_dict[lexeme] = [file_id]

        if i > 1:
            dict_list.append(local_dict)

        return local_dict
