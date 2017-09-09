#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Ustinia Kosheleva


def cutter(seq, a, b):
    """
    Replaces all the out of bounds elements
    with lower bound a if an element is less than lower bound,
    with upper bound b if an element is bigger than upper bound,
    does not change inbound elements.

    Args:
        seq: list of numerals
        a: numeric type, lower bound
        b: numeric type, upper bound

    Returns:
        list of numerals

    Tests:
    >>> seq = [1, 2.06, 3, 4, 1e1]
    >>> cutter(seq, 2, 4)
    >>> seq == [2, 2.06, 3, 4, 4]
    True

    >>> cutter(seq, 1, 5)
    >>> seq == [2, 2.06, 3, 4, 4]
    True

    >>> seq = []
    >>> cutter(seq, 2, 4)
    >>> seq == []
    True
    """
    for i, el in enumerate(seq):
        if el < a:
            seq[i] = a
        elif el > b:
            seq[i] = b

if __name__ == '__main__':
    import doctest
    doctest.testmod()
