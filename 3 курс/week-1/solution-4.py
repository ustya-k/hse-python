#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Ustinia Kosheleva

import sys
import math


def factorial(n):
    '''
    Finds a factorial of a number.

    Args:
        n: int

    Returns:
        int

    Tests:
    >>> factorial(5) == 120
    True

    >>> factorial(0) == 1
    True

    >>> r = range(100)
    >>> [factorial(i) for i in r] == [math.factorial(i) for i in r]
    True

    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: Argument n must be non-negative

    >>> factorial([1])
    Traceback (most recent call last):
        ...
    ValueError: Argument n must be an integer

    >>> factorial(tuple([1]))
    Traceback (most recent call last):
        ...
    ValueError: Argument n must be an integer

    >>> factorial('1')
    Traceback (most recent call last):
        ...
    ValueError: Argument n must be an integer
    '''
    if not isinstance(n, int):
        raise ValueError("Argument n must be an integer")

    if n < 0:
        raise ValueError("Argument n must be non-negative")

    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

if __name__ == '__main__':
    import doctest
    doctest.testmod()
