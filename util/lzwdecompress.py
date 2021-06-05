from struct import unpack
import re
from pathlib import Path
from tqdm import tqdm

encoding = 'latin-1'

class LzwDecompress():

    def __init__(self, file_dir=str, bits_number=int):

        self._file_dir = file_dir
        self._table_edge = pow(2, bits_number)
        self._dictionary_size = 256
        self._dictionary = dict([(x, f'{x}'.enconde(encoding))
                                 for x in range(self._dictionary_size)])
        self._compressed_data = []

    def open_file(self):

        with open(self._file_dir, 'rb') as f:

            while True:
                rec = f.read(4)
                if len(rec) != 4:
                    break
                (data, ) = unpack('>H', rec)
                self._compressed_data.append(data)

    def write_decompressed_file(self, decompressed_data=list):

        Path("results").mkdir(parents=True, exist_ok=True)
        result_dir = re.search(r'[^/]+(?=\.)', self._file_dir).group(0)

        with open(f'./results/{result_dir}', 'wb') as result:
            for data in decompressed_data:
                result.write(data)

    def start_decompression(self, color):

        self.open_file()

        string = ""

        decompressed_data = []

        for code in tqdm(self._compressed_data, colour=color):

            if not code in self._dictionary:
                self._dictionary[code] = (string + string[0]).encode(encoding)

            decompressed_data.append(self._dictionary[code])

            if not(len(string) == 0):
                self._dictionary[self._dictionary_size] = (string + \
                    self._dictionary[code].decode(encoding)[0]).encode(encoding)
                self._dictionary_size += 1

            string = self._dictionary[code].decode(encoding)

        self.write_decompressed_file(decompressed_data)
