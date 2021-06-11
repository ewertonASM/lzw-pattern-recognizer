import os
import re
import pickle

from tqdm import tqdm
from util import lzwcompress
from util import lzwdecompress

import sys


class PatternRecognizer:

    def __init__(self, input_file, kbit=None):

        self.dict_cache_dir = "./dict_cache"
        self.input_file = input_file
        self.lzwcompress = lzwcompress.LzwCompress
        self.kbit = kbit

    def train(self, color, train_split):

        for path, _, files in tqdm(list(os.walk(self.input_file))[1:], colour=color):

            compress = self.lzwcompress(bits_number=self.kbit)

            split_point = round(len(files)*(train_split/100))
            training_data = files[:split_point]
            test_data = files[split_point:]

            for file in training_data:

                compress._file_dir = os.path.join(path, file)
                compress.start_compress(color=False)

            dict_cache_name = re.split('/(?=s[1-9])', path)[1]

            with open(f'dict_cache/{dict_cache_name}_{self.kbit}', 'wb') as dict_cache:
                pickle.dump(compress._dictionary, dict_cache)


            for test_file in test_data:
                self.input_file = test_file
                self.test()

    def test(self):

        best_compressed_data_len = sys.maxsize

        for path, _, files in list(os.walk(self.dict_cache_dir)):
            for file in tqdm(files, colour='#F6736C'):

                with open(os.path.join(path, file), 'rb') as f:
                    dict_cache = pickle.load(f)

                self.kbit = int(file.split('_')[1])

                compress = self.lzwcompress(file_dir=self.input_file,
                                            dict_cache=dict_cache, bits_number=self.kbit)

                _, _, _, compressed_data = compress.start_compress(color=False)

                if len(compressed_data) < best_compressed_data_len:
                    best_compression = compressed_data
                    best_compressed_data_len = len(compressed_data)

        compress.write_compress_file(best_compression)
