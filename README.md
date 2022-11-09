# Python script for compressing files in given folder(s)

### Repository structure:
```
.
├── test/
│   ├── __init__.py
│   ├── test.py             - testing script (unittest)
│   └── log_files           - dummy log files used for testing
├── logcompressor/
│   ├── __init__.py
│   └── logcompressor.py    - main script
├── .gitignore              - gitignore file
└── README.md               - readme file with detailed information
```

### Dependencies:
Script uses no 3rd party libraries.

### Usage:
Example of usage in virtual enviroment:
```python logcompressor/logcompressor.py -p 'path1/logs' 'path2/logs' -c 7 -r -d```
This example tells the script to search recursively for log files in folders 'path1/logs' and 'path2/logs' and delete them after compression using level 7 compression. 

Complete usage:
```
usage: logcompressor.py [-h] [-c {1,2,3,4,5,6,7,8,9}] [-p PATHS [PATHS ...]] [-d] [-r]

Script for compressing log files in a given directory

options:
  -h, --help            show this help message and exit
  -c {1,2,3,4,5,6,7,8,9}, --compress {1,2,3,4,5,6,7,8,9}
                        Compression level 1-9 (default: 6)
  -p PATHS [PATHS ...], --paths PATHS [PATHS ...]
                        Path(s) to the folder(s) with logs (default: /var/logs)
  -d                    If set, script deletes log files after compression.
  -r                    If set, script searches for logs in given path(s) recursively
  ```