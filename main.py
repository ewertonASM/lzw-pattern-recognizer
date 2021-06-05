from util import lzwcompress, lzwdecompress
from util import paint
from util import reportgenerator

import fire

painter = paint.Paint()

def compress(bits_number, input_file, painter):

    report_generator = reportgenerator.Report_Generator

    compression_times, compressed_sizes, num_indexes = [], [], []

    bits_number_list = [bits_number] if bits_number else [number for number in range(9,17)]
        
    for index, kbit in enumerate(bits_number_list):
        compress = lzwcompress.LzwCompress(input_file, kbit)

        log, color = painter.set_color(f'\nK={kbit}, Dictionary_size={pow(2,kbit)}', index)
        print(log)
        print('COMPRESSING...')

        compress_time, len_compressed_data, compressed_size = compress.start_compress(color)

        compression_times.append(compress_time)
        compressed_sizes.append(compressed_size)
        num_indexes.append(len_compressed_data)

    report_generator(compression_times, num_indexes, input_file, compressed_sizes, kbit)


def decompress(bits_number, input_file, painter):

    decompress = lzwdecompress.LzwDecompress(input_file, bits_number)

    log, color = painter.set_color(f'\nK={bits_number}, Dictionary_size={pow(2,bits_number)}', bits_number)

    print(log)
    print('DECOMPRESSING...')

    decompress.start_decompression(color)


def process(operation=str, input_file=str, bits_number=None):
    
    if operation == 'compress':
        compress(bits_number, input_file, painter)

    elif operation == 'decompress':
        decompress(bits_number, input_file, painter)

if __name__ == '__main__':
    
    try:
        fire.Fire(process)
    except:
        print("---------------------------------------------------------------------------------------------")
        print("Error: Invalid Params")
        print("\nFOR COMPRESS, TRY:")
        print('python main.py -input_file "input/corpus16MB.txt" -bits_number "9" -operation "compress"')
        print("\nFOR DECOMPRESS, TRY:")
        print('python main.py -input_file "output/corpus16MB.txt" -bits_number "9" -operation "decompress"')
        print("---------------------------------------------------------------------------------------------")