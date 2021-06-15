import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pathlib import Path
from itertools import zip_longest
from os import stat
import re

class Report_Generator:

    def __init__(self, accuracies_dict, times_dict):

        self._accuracies_dict = accuracies_dict
        self._times_dict = times_dict
        self.graph_generator()
        

    def graph_generator(self):
        
        kbits = []
        accuracy_rates = []
        times = []
        persons = []
        for (person, accuracy), (kbit, time) in zip_longest(self._accuracies_dict.items(), self._times_dict.items()):
            kbits.append(kbit)
            accuracy_rates.append(accuracy*100)
            times.append(time)
            persons.append(person)

        _fig0, ax0 = plt.subplots(nrows=1, ncols=1)
        ax0.set_title('Accuracy rates by kbit')
        ax0.set(xlabel='K-bits', ylabel='Accuracy', title='Accuracy rates by kbit')
        ax0.plot(kbits, accuracy_rates)
        ax0.yaxis.set_major_formatter(mtick.PercentFormatter())
        Path("results/graphs").mkdir(parents=True, exist_ok=True)
        plt.savefig(f'./results/graphs/accuracies.png')

        _fig1, ax1 = plt.subplots(nrows=1, ncols=1)
        ax1.set_title('Processing time by K-bits')
        ax1.set(xlabel='K-bits', ylabel='Processing Time (s)', title='Processing time by K-bits')
        ax1.plot(kbits, times)
        plt.savefig(f'./results/graphs/times.png')

        # _fig2, ax2 = plt.subplots(nrows=1, ncols=1)
        # ax2.set_title('Number of indexes by K-bits')
        # ax2.set(xlabel='K-bits', ylabel='Number of indexes', title='Num. of indexes by K-bits')
        # ax2.plot(kbits, self._num_of_indexes)
        # plt.savefig(f'./results/graphs/graph_indexes({input_name}).png')