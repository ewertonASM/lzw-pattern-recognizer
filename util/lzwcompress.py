from pathlib import Path
from struct import pack
from tqdm import tqdm
import time
import re

encoding = 'latin-1'

class LzwCompress():

    def __init__(self, file_dir=str, bits_number=int):

        self._file_dir = file_dir
        self._table_edge = pow(2, bits_number)
        self.bytes_dictionary_size = 256
        self._dictionary = {i.to_bytes(1, 'big'):i for i in range(
            self.bytes_dictionary_size)}

    def open_file(self):

        try:
            with open(self._file_dir, 'r', encoding='latin-1') as f:
                data = f.read()
            return data
            
        except:
            print("ERROR: File not found")

    def write_compress_file(self, compressed_data=list):

        Path("output").mkdir(parents=True, exist_ok=True)
        output_dir = f"./output/{re.search(r'[^/]+(?=$)', self._file_dir).group(0)}.lzw"

        with open(output_dir, 'wb') as output:
            for data in compressed_data:
                 output.write(pack('>H', data))

    def start_compress(self, color):

        data = self.open_file()
        string = ""
        compressed_data = []

        start = time.time()
        for character in tqdm(data, colour=color):

            symbol = string + character

            if symbol.encode(encoding) in self._dictionary:
                string = symbol
            else:
                encoded_chr = string.encode(encoding)
                compressed_data.append(self._dictionary[encoded_chr])

                if(len(self._dictionary) <= self._table_edge):
                    self._dictionary[symbol.encode(encoding)] = self.bytes_dictionary_size
                    self.bytes_dictionary_size += 1

                string = character

        if string.encode(encoding) in self._dictionary:
            compressed_data.append(self._dictionary[string.encode(encoding)])

        end = time.time()
        compress_time = end - start

        print(f'Elapsed time is {end - start}s')

        self.write_compress_file(compressed_data)

        return compress_time, len(compressed_data), len(compressed_data)

        
