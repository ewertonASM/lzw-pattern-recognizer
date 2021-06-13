import os
import re
import pickle

from tqdm import tqdm
from util import lzwcompress
import random

import sys


class PatternRecognizer:

    def __init__(self, input_file, kbit=None):

        self.dict_cache_dir = "./dict_cache"
        self.input_file = input_file
        self.lzwcompress = lzwcompress.LzwCompress
        self.train_dictionary = dict()
        self.kbit = kbit
        self.test_data = []

    def train(self, color, train_split):

        for path, _, files in tqdm(list(os.walk(self.input_file))[1:], colour=color):

            compress = self.lzwcompress(bits_number=self.kbit, operation="train")

            split_points = round(len(files)-(len(files)*(train_split/100)))
            tests_files = random.sample(files, split_points)

            self.test_data.extend([os.path.join(path, file) for file in tests_files])
            training_data = list(set(files) - set(tests_files))

            for file in training_data:

                compress._file_dir = os.path.join(path, file)
                compress.start_compress(color=False)

            dict_cache_name = f'{re.split("/(?=s[1-9])", path)[1]}_{self.kbit}'

            with open(f'dict_cache/{dict_cache_name}', 'wb') as dict_cache:
                pickle.dump(compress._dictionary, dict_cache)

            self.train_dictionary[dict_cache_name] = compress._dictionary

        return self.test_data

    def test(self):

        if not self.train_dictionary:
            self.load_dict_cache()
        
        best_compressed_data_len = sys.maxsize

        print("\nTesting files...")

        for label, bytes_dict in tqdm(self.train_dictionary.items()):

            self.kbit = int(label.split('_')[1])

            compress = self.lzwcompress(file_dir=self.input_file,
                                        dict_cache=bytes_dict, bits_number=self.kbit)

            _, _, _, compressed_data = compress.start_compress(color=False)

            if len(compressed_data) < best_compressed_data_len:
                best_settings = label
                best_compression = compressed_data

        compress.write_compress_file(best_compression)
        print(f'\nFile: {self.input_file}')
        print(f'Best compression len: {len(best_compression)}')
        print(f'Best settings: {best_settings}')


    def load_dict_cache(self):

        for path, _, files in list(os.walk(self.dict_cache_dir)):
            for file in files:

                with open(os.path.join(path, file), 'rb') as f:
                    self.train_dictionary[file] = pickle.load(f)

        
