import heapq


class _LinesMinHeap(object):
    """A min heap for storing (line, filepath) tuples in lexicographical order.

    This convenience class wraps common operations in the heapq module of
    Python's standard library.

    Attributes:
        _heap: The heap storing (line, filepath) tuples.

    Args:
        lines_and_filepaths: List of (line, filepath) tuples to heapify.
    """

    def __init__(self, lines_and_filepaths):
        self._heap = lines_and_filepaths
        heapq.heapify(self._heap)

    def size(self):
        """Returns the current size of the heap."""
        return len(self._heap)

    def pop(self):
        """Returns the minimum (line, filepath) tuple.

        This function maintains the min heap property. File paths, guaranteed
        to be unique, serve as the tiebreaker when determining the minimum
        amongst duplicate lines.
        """
        return heapq.heappop(self._heap)

    def push(self, line, filepath):
        """Pushes a (line, filepath) tuple onto the heap.

        This function maintains the min heap property. File paths, guaranteed
        to be unique, serve as the tiebreaker when ordering duplicate lines.
        """
        heapq.heappush(self._heap, (line, filepath))


def _is_end_of_file(line):
    """Returns whether the line represents the end of a file."""
    return line == ''


def _is_blank_line(line):
    """Returns whether the line is a blank line."""
    return line == '\n'


def _read_next_non_blank_line(file):
    """Returns the next non-blank line in the file."""
    line = None
    while line is None or _is_blank_line(line):
        line = file.readline()
    return line


def _append_new_line_delimiter_to_data_if_not_exists(line):
    """Appends a new line character to a data line if it does not exist.

    Because input files may not end with a new line, we add one to prevent
    multiple data lines from ending up on the same line in the output file.
    """
    if _is_end_of_file(line) or line.endswith('\n'):
        return line
    return '{}\n'.format(line)


def _initialize_lines_to_write_min_heap(files):
    """Returns a min heap containing the first non-blank line from each input file.

    Args:
        files: A dictionary of filepaths to readable file objects.

    Returns:
        A _LinesMinHeap instance that stores tuples of (line, filepath) for
        each data-containing input file.
    """
    lines_to_write = [(_read_next_non_blank_line(file), filepath)
                      for filepath, file in files.items()]
    return _LinesMinHeap(lines_to_write)


def consolidate(data):
    """Consolidates data from 1 or more input files into a single output file.

    Note:
        This function modifies input by closing all passed in data files.

    Args:
        data: A DataFiles instance with references to input and output files.
    """
    lines_min_heap = _initialize_lines_to_write_min_heap(data.input_files)
    latest_written_line = None
    while lines_min_heap.size() > 0:
        (line, filepath) = lines_min_heap.pop()
        line = _append_new_line_delimiter_to_data_if_not_exists(line)
        file = data.input_files[filepath]
        if _is_end_of_file(line):
            file.close()
        elif line == latest_written_line:
            lines_min_heap.push(_read_next_non_blank_line(file), filepath)
        else:
            data.output_file.write(line)
            latest_written_line = line
            lines_min_heap.push(_read_next_non_blank_line(file), filepath)
    data.output_file.close()
