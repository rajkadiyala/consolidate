import os


def _is_valid_text_file(filename):
    """Returns whether the filename uses a supported text file extension."""
    return filename.endswith('.txt') or filename.endswith('.text')


def _open_text_file_directory(directory_path):
    """Opens each text file in the provided directory.

    Args:
        directory_path: Path to the directory.

    Returns:
        A dictionary of filepaths to readable file objects.

    Raises:
        AssertionError: If provided directory contains non-text files.
    """
    filepath_to_file = {}
    for filename in os.listdir(directory_path):
        assert _is_valid_text_file(
            filename
        ), 'non-text file {} found in provided directory {}'.format(
            filename, directory_path)
        filepath = os.path.join(directory_path, filename)
        filepath_to_file[filepath] = open(filepath, 'r')
    return filepath_to_file


class DataFiles(object):
    """Opens the provided files and stores the corresponding file objects.

    Args:
        input_directory_path: Path to the input directory.
        output_file_path: Path to the output file.

    Attributes:
        input_files: A dictionary of filepaths to readable file objects.
        output_file: A writeable file object.
    """

    def __init__(self, input_directory_path, output_file_path):
        self.input_files = _open_text_file_directory(input_directory_path)
        self.output_file = open(output_file_path, 'w')
