#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Ustinia Kosheleva

import re


def lines_to_dict(lines):
    '''
    Converts a dictionary given as list of lines to dictionary data structure,
    where keys are words and values are lists of meanings.

    Args:
        lines: list

    Returns:
        dict
    '''
    dictionary = {}
    for line in lines:
        res = re.search('(.*?) - (.*?)$', line)
        word = res.group(1)
        meanings = res.group(2).split(', ')
        dictionary[word] = meanings
    return dictionary


def reverse_dict(initial_dict):
    '''
    Reverses a dictionary: it's values are new keys, it's keys are new values.

    Args:
        initial_dict: dict

    Returns:
        dict
    '''
    final_dict = {}
    for word in initial_dict:
        for meaning in initial_dict[word]:
            if meaning in final_dict:
                final_dict[meaning].append(word)
            else:
                final_dict[meaning] = [word]
    return final_dict


def dict_to_lines(dictionary):
    '''
    Sorts words in dictionary in lexicographic order,
    converts a dictionary given as dictionary data structure to list of lines.

    Args:
        dictionary: dict

    Returns:
        list
    '''
    lines = []
    words = sorted(dictionary.keys())
    for word in words:
        line = '%s - %s' % (word, ', '.join(dictionary[word]))
        lines.append(line)
    return lines


def create_reversed_dict(initial_dict_lines):
    '''
    Creates reversed version of a dictionary given as a list of lines,
    new words are meanings of words from initial dictionary,
    their meanings are the words which they were the meanings of.

    Args:
        initial_dict_lines: list of str

    Returns:
        list of str
    '''
    initial_dict = lines_to_dict(initial_dict_lines)
    final_dict = reverse_dict(initial_dict)
    final_dict_lines = dict_to_lines(final_dict)
    return final_dict_lines


def get_reversed_dict():
    '''
    Reads initial dictionary from a file,
    creates reversed version of it,
    saves it to a new file.
    '''
    with open('input.txt', 'r', encoding='utf-8') as f:
        input_dict_lines = f.readlines()

    output_dict_lines = create_reversed_dict(input_dict_lines)

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_dict_lines))
