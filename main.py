import argparse
import os

from src.consolidate import consolidate
from src.data_files import DataFiles


def valid_directory(directory_path):
    """Validates that the provided directory exists."""
    if not os.path.isdir(directory_path):
        raise argparse.ArgumentTypeError(
            '`{}` is not a path to a valid directory'.format(directory_path))
    return directory_path


def parse_args():
    """Defines required arguments for program execution."""
    parser = argparse.ArgumentParser(
        description=('Command-line program for consolidating data '
                     'from multiple files into a single file.'))
    parser.add_argument('-i',
                        '--input_directory_path',
                        type=valid_directory,
                        required=True,
                        help='Path to the input directory.')
    parser.add_argument('-o',
                        '--output_file_path',
                        required=True,
                        help='Path to the output file.')
    return parser.parse_args()


def main():
    args = parse_args()
    consolidate(DataFiles(args.input_directory_path, args.output_file_path))


if __name__ == '__main__':
    main()
