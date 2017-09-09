#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Ustinia Kosheleva

from os import listdir, stat
from os.path import isfile, join
from operator import itemgetter
import sys


def get_file_size(file, dirpath):
    '''
    Finds size of a file, creates tuple of name of the file and it's size.

    Args:
        file: str, name of the file
        dirpath: str, path to the directory

    Returns:
        tuple
    '''
    fileinfo = stat(join(dirpath, file))
    return (file, fileinfo.st_size)


def get_files_sizes(files, dirpath):
    '''
    Finds sizes of files,
    creates a list of tuples (name of a file, size of the file).

    Args:
        files: list
        dirpath: str, path to the directory

    Returns:
        list of tuples
    '''
    files_with_size = []
    for file in files:
        files_with_size.append(get_file_size(file, dirpath))
    return files_with_size


def get_files_with_size(dirpath):
    '''
    Finds all files in a directory (not folders),
    creates a list of tuples (name of a file, size of the file).

    Args:
        dirpath: str, path to the directory

    Returns:
        list of tuples
    '''
    dir_elements = listdir(dirpath)
    files = [el for el in dir_elements if isfile(join(dirpath, el))]
    return get_files_sizes(files, dirpath)


def get_sorted_files_with_sizes(dirpath):
    '''
    Finds all files in a directory and their sizes,
    sorts them by size in descending order.

    Args:
        dirpath: str, path to the directory

    Returns:
        list of tuples

    Test:
    >>> files = [('solution-3.py', 2865),\
                 ('solution-2.py', 2369),\
                 ('test-solution-2.py', 1445),\
                 ('solution-4.py', 1208),\
                 ('solution-1.py', 925),\
                 ('test-solution-4.py', 883),\
                 ('solution-5.py', 731),\
                 ('output.txt', 114),\
                 ('input.txt', 81)]
    >>> get_sorted_files_with_sizes('.') == files
    True
    '''
    files = get_files_with_size(dirpath)
    files.sort(key=itemgetter(0))
    files.sort(key=itemgetter(1), reverse=True)
    return files


def print_sorted_files(dirpath='.'):
    '''
    Prints out all files from directory sorted by size in descending order.

    Args:
        dirpath: str, path to the directory, default -- current directory
    '''
    files = get_sorted_files_with_sizes(dirpath)
    for file in files:
        print(file[0], file[1])


def print_sorted_files_from_directory():
    '''
    Receives a directory from command line,
    prints out all files from the directory sorted by size in descending order.
    If nothing was received, current directory is used.
    '''
    try:
        print_sorted_files(sys.argv[1])
    except:
        print_sorted_files()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
