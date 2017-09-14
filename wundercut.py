#!/usr/bin/env python
"""
A solution to the "Brilliant cut" Wundernut coding challenge on fall 2017 by Wunder Dog.
Just run the script with either Python 2 or 3 in the same directory.

Author: Kimmo Kiiski <kimmo@kii.ski>
"""
from __future__ import unicode_literals
import json


class CutSet:
    """
    Represents a list of cuts and their total value.
    """
    def __init__(self, cuts, value):
        self.cuts = cuts
        self.value = value
    
    def __add__(self, other):
        return CutSet(self.cuts + other.cuts, self.value + other.value)


def get_solution(material):
    """
    Finds the maximum profit from the optimal cuts for the given material (input data).
    Returns a list of (<gemstone name>, <max profit>) tuples.
    """
    return [
        (gemstone, get_max_profit(info['rawChunks'], info['cuts']))
        for gemstone, info in material.items()
    ]


def get_max_profit(chunks, cuts):
    """
    Calculates the maximum profit for the given raw gemstone chunks using
    the given possible cut sizes/values and the raw chunks.
    """
    # Convert cut option dicts to tuples for easier iteration and consistent order
    size_values = [(cut['size'], cut['value']) for cut in cuts]
    # Because the optimal solution is the same to all raw sizes,
    # use a cache dict to remember them.
    cache = {}
    return sum((get_optimal_cuts(chunk, size_values, cache).value for chunk in chunks), 0)


def get_optimal_cuts(chunk, size_values, cache):
    """
    Determines the optimal cuts for the given chunk, using the given allowed
    size-value pairs and the cache dict. Returns a CutSet object, holding
    the `cuts` list and the total `value`.
    """
    # Use any already a known optimal solution from the cache
    if chunk in cache:
        return cache[chunk]
    # Get all possible options that the raw/remaining chunk can be cut
    options = [
        CutSet([size], value) + get_optimal_cuts(chunk - size, size_values, cache)
        for size, value in size_values if chunk >= size
    ]
    if options:
        # Pick the cut with the best value
        cuts = max(options, key=lambda cut: cut.value)
    else:
        # Raw chunk cannot be cut (any more).
        # The value of the remaining waste material raw chunk is negative!
        cuts = CutSet([], -chunk)
    # Save the soution to cache and return it
    cache[chunk] = cuts
    return cuts


if __name__ == '__main__':
    # Read the input data
    with open('input.json', 'r') as input_file:
        material = json.load(input_file)
    # Print the maximum profits nicely formatted as an ASCII table
    print("Gemstone  | Total value")
    print("----------|-------------")
    total_value = 0
    for gemstone, value in get_solution(material):
        print("{:<10}| {:,}".format(gemstone, value))
        total_value += value
    print("----------|-------------")
    print("Total     | {:,}".format(total_value))
