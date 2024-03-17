# Data Files Consolidation Tool

Raj Kadiyala (rkadiya0@uchicago.edu)

- [Data Files Consolidation Tool](#data-files-consolidation-tool)
  - [Overview](#overview)
    - [Assumptions & Constraints Rationale](#assumptions--constraints-rationale)
    - [Chosen Approach](#chosen-approach)
  - [How to Execute](#how-to-execute)
    - [Program / Tool](#program--tool)
    - [Tests](#tests)
  - [Time & Space Complexities](#time--space-complexities)
    - [Time Complexity](#time-complexity)
    - [Space Complexity](#space-complexity)
    - [Alternatives Considered](#alternatives-considered)

## Overview
The Data Files Consolidation Tool is a command-line tool for consolidating one or more lexicographically-ordered text files into a single lexicographically-ordered text file, while removing any duplicate or blank lines present across input files.

### Assumptions & Constraints Rationale
The tool makes the following assumptions to constrain input ambiguities:

| Assumption                                                                                                                                                                               | Constraint Rationale                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| All files in the input directory will be .txt or .text files, lexicographically sorted.                                                                                                  | Avoids need for further validation and handling.                                                              |
| Input files are newline-delimited, but they won't necessarily end with a new line.                                                                                                       | N / A                                                                                                         |
| Blank lines are potentially interspersed throughout each input file.                                                                                                                     | N / A                                                                                                         |
| Duplicate lines can potentially be found within the same input file and across input files.                                                                                              | N / A                                                                                                         |
| The individual(s) executing the tool will have read access to all files in the input directory and write access to the specified output file.                                            | Avoids need for handling permissions-related errors.                                                          |
| A file in the input directory can be arbitrarily large and all of the data in a single file will not necessarily fit into memory.                                                        | N / A                                                                                                         |
| The number of files in the input directory can be arbitrarily large, but we can cherrypick at least one random line from every file and have all the cherrypicked lines fit into memory. | Avoids need for employing a divide-and-conquer approach with intermediate output potentially written to disk. |


### Chosen Approach
In keeping with the above assumptions, the tool works by opening every file in the input directory and storing the first non-blank line in each file in a min heap. The minimum of the min heap is popped off iteratively, written to the specified output file, and replaced in the heap by the next non-blank line in the same input file. Each input file is closed after all of the data in that file has been written to the output file. The output file is closed after all of the input files have been exhausted.

## How to Execute
Both the tool and tests require access to a python3 interpreter for execution. Because neither the tool nor the tests use any modules outside of Python's standard library, you should **not** have to `pip install` anything.

### Program / Tool
In order to execute the tool, you have to specify two command line flags:
- `-i, --input_directory_path`: the path to a valid input directory containing only .txt or .text files
- `-o, --output_file_path`: the path to an output file**

** Note: the output file will be overwritten if it exists. If it does not exist, it will be created.

Examples:

```
python3 main.py \
    --input_directory_path=/path/to/input_directory \ 
    --output_file_path=/path/to/output_file.txt
```

```
python3 main.py \
    -i /path/to/input_directory \ 
    -o /path/to/output_file.txt
```

### Tests
Executing the tests requires you to be in the root directory of the project, i.e. the directory containing `main.py` and `README.md`:

```
cd consolidate
```

Afterwards, you can execute the tests as follows:

```
python3 -m unittest -v tests/test_consolidate.py
```

## Time & Space Complexities
To determine the time and space complexities of the program:
- Let _k_ be the total number of files in the input directory.
- Let _N_ be the total number of lines across all input files.

### Time Complexity
The time complexity of the program is O(_N_ * log _k_).
  - O(_k_) + O(_k_) + O(_N_ * log _k_) => O(_N_ * log _k_).

| Operation                                                                                                                              | Complexity       |
| -------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| Iterating through files in input directory and storing file object references                                                          | O(_k_)           |
| Initializing a min heap with the first non-blank line in each input file                                                               | O(_k_)           |
| Iteratively finding the next line in lexicographical order, including min heap insertion and extraction, until all input is exhausted. | O(_N_ * log _k_) |

### Space Complexity
The space complexity of the program is O(_k_).
  -  O(_k_) + O(1) + O(_k_) => O(_k_).

| Storage                                                                            | Complexity |
| ---------------------------------------------------------------------------------- | ---------- |
| Hashmap of filepath to file object reference for each file in the input directory. | O(_k_)     |
| Variable storing output file path.                                                 | O(1)       |
| Min heap storing the next non-blank line for each file in the input directory.     | O(_k_)     |

### Alternatives Considered
Given the assumptions detailed above, only one alternative was considered at length:

* Initializing _k_ pointers, one for each input file, and incrementing a pointer after writing a line to the output file. The pointer approach was tabled in favor of the min heap approach because the pointer approach has a time complexity of O(_N_ * _k_)--requires iterating through each of the _k_ files' next lines for each of the _N_ total lines--which is worse than O(_N_ * log _k_).
