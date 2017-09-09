import pytest
solution2 = __import__('solution-2')


def test_lines_to_dict():
    lines_to_dict = solution2.lines_to_dict
    lines = ['apple - malum, pomum',
             'punishment - malum, multa']
    dictionary = {'apple': ['malum', 'pomum'],
                  'punishment': ['malum', 'multa']}
    assert lines_to_dict(lines) == dictionary


def test_reverse_dict():
    reverse_dict = solution2.reverse_dict
    dictionary = {'apple': ['malum', 'pomum'],
                  'punishment': ['malum', 'multa']}
    new_dictionary = {'malum': ['apple', 'punishment'],
                      'pomum': ['apple'],
                      'multa': ['punishment']}
    assert reverse_dict(dictionary) == new_dictionary


def test_dict_to_lines():
    dict_to_lines = solution2.dict_to_lines
    dictionary = {'malum': ['apple', 'punishment'],
                  'pomum': ['apple'],
                  'multa': ['punishment']}
    lines = ['malum - apple, punishment',
             'multa - punishment',
             'pomum - apple']
    assert dict_to_lines(dictionary) == lines


def test_create_reversed_dict():
    create_reversed_dict = solution2.create_reversed_dict
    input_lines = ['apple - malum, pomum',
                   'punishment - malum, multa']
    output_lines = ['malum - apple, punishment',
                    'multa - punishment',
                    'pomum - apple']
    assert create_reversed_dict(input_lines) == output_lines
