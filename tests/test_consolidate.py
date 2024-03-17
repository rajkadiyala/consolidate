import os
import tempfile
import unittest

from src.consolidate import consolidate
from src.data_files import DataFiles

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def _get_testdata_input_directory_path(dirname):
    return os.path.join(TEST_DIR, 'testdata', dirname)


def _get_golden_output_file_path(dirname):
    return os.path.join(TEST_DIR, 'golden', dirname, 'expected.txt')


def _get_expected_consolidation_output(dirname):
    with open(_get_golden_output_file_path(dirname), 'r') as file:
        return file.readlines()


def _consolidate_with_tmp_output(dirname):
    with tempfile.TemporaryDirectory() as output_dir:
        output_file_path = os.path.join(output_dir, 'actual.txt')
        consolidate(
            DataFiles(_get_testdata_input_directory_path(dirname),
                      output_file_path))
        with open(output_file_path, 'r') as output_file:
            return output_file.readlines()


class TestConsolidate(unittest.TestCase):

    def test_duplicate_words(self):
        self._test_consolidate_success('duplicate_words')

    def test_multiple_files(self):
        self._test_consolidate_success('multiple_files')

    def test_single_file(self):
        self._test_consolidate_success('single_file')

    def test_empty_blank_files(self):
        self._test_consolidate_success('empty_blank_files')

    def test_no_new_line_end(self):
        self._test_consolidate_success('no_new_line_end')

    def test_non_ascii(self):
        self._test_consolidate_success('non_ascii')

    def test_numbers(self):
        self._test_consolidate_success('numbers')

    def test_non_text_files(self):
        with self.assertRaises(AssertionError):
            _consolidate_with_tmp_output('non_text_files')

    def _test_consolidate_success(self, dirname):
        self.assertEqual(_get_expected_consolidation_output(dirname),
                         _consolidate_with_tmp_output(dirname))


if __name__ == 'main':
    unittest.main()
