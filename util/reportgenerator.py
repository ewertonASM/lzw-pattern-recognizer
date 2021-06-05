import matplotlib.pyplot as plt
from os import stat
import re

class Report_Generator:

    def __init__(self, compression_times, num_of_indexes, input_file, compressed_sizes, num_bits):

        self._compression_times = compression_times
        self._num_of_indexes = num_of_indexes
        self._input_file = input_file
        self._compressed_sizes = compressed_sizes
        self._num_bits = num_bits
        
        rc = self.calculate_size()
        self.graph_generator(rc)


    def calculate_size(self):

        input_size = stat(self._input_file).st_size
        
        compression_ratios = []

        for output_size in self._compressed_sizes:
            compression_ratios.append((input_size*8)/(output_size*self._num_bits)) 

        return compression_ratios
        

    def graph_generator(self, compression_ratios):
        
        kbits = [i for i in range(9, 17)]
        
        input_name = re.search(r'[^/]+(?=\.)', self._input_file).group(0)

        _fig0, ax0 = plt.subplots(nrows=1, ncols=1)

        ax0.set_title('Compression ratios by K-bits')
        ax0.set(xlabel='K-bits', ylabel='Compression Ratios', title='Compression Ratios by K-bits')
        ax0.plot(kbits, compression_ratios)
        plt.savefig(f'./results/graphs/graph_RC({input_name}).png')

        _fig1, ax1 = plt.subplots(nrows=1, ncols=1)
        ax1.set_title('Compression times by K-bits')
        ax1.set(xlabel='K-bits', ylabel='Compression Times', title='Compression Times by K-bits')
        ax1.plot(kbits, self._compression_times)
        plt.savefig(f'./results/graphs/graph_Compression_time({input_name}).png')

        _fig2, ax2 = plt.subplots(nrows=1, ncols=1)
        ax2.set_title('Number of indexes by K-bits')
        ax2.set(xlabel='K-bits', ylabel='Number of indexes', title='Num. of indexes by K-bits')
        ax2.plot(kbits, self._num_of_indexes)
        plt.savefig(f'./results/graphs/graph_indexes({input_name}).png')