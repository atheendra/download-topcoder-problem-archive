# download-topcoder-problem-archive
Download topcoder problem archives using gettc

Prerequisites:
* Python 2.7.x
* Beautiful Soup for python
* gettc to download topcoder problems. Link: https://github.com/seri/gettc

Installing:
No installation necessary. Just download the script and run it by issuing the following command:
python get_problem_archive.py

Running:
python get_problem_archive.py

Options:
python get_problem_archive.py -h

Notes:
To avoid downloading the same Problem ID multiple times in subsequent runs, a file, say "problem_ids.txt", contains list of completed problem IDs separated by new-lines.

Example:
Contents of problem_ids.txt:
13421
48582

Specifying this file makes sure the program ignores downloading these IDs.
