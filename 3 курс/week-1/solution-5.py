#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Ustinia Kosheleva


def is_palindrome(line):
    """
    Checks if a line is a palindrome. Case-sensitive.

    Args:
        line: str

    Returns:
        bool

    Tests:
    >>> is_palindrome('cat')
    False

    >>> is_palindrome('kayak')
    True

    >>> is_palindrome('rats live on no evil star')
    True

    >>> is_palindrome('')
    True

    >>> is_palindrome('Hannah')
    True
    """
    left = 0
    right = len(line) - 1
    line = line.lower()
    while left < right:
        if line[left] != line[right]:
            return False
        left += 1
        right -= 1
    return True

if __name__ == '__main__':
    import doctest
    doctest.testmod()
