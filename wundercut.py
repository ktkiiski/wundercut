#!/usr/bin/env python
from __future__ import unicode_literals
import json


class CutSet:
    def __init__(self, cuts, value):
        self.cuts = cuts
        self.value = value
    
    def __add__(self, other):
        return CutSet(self.cuts + other.cuts, self.value + other.value)


def get_solution(material):
    """
    Finds the optimal cuts for the given material (input data).
    Returns a dict where keys are gemstone type and values are maximum profits.
    """
    return {
        gemstone: get_gemstone_solution(info['cuts'], info['rawChunks'])
        for gemstone, info in material.items()
    }


def get_gemstone_solution(cuts, chunks):
    """
    Determines the optimal chunks for the given gemstone type, by using
    the given possible cut sizes/values and the raw chunks.
    """
    # Convert cut option dicts to tuples for easier iteration and consistent order
    cut_options = {cut['size']: cut['value'] for cut in cuts}
    # As the optimal solution is the same to all raw sizes,
    # use a cache dict to remember them.
    cache = {}
    return sum(
        (get_optimal_cuts(chunk, cut_options, cache).value for chunk in chunks),
        0
    )


def get_optimal_cuts(chunk, values_by_size, cache):
    # Check if there is an optimal solution in the cache
    if chunk in cache:
        return cache[chunk]
    # Get all possible options that the raw/remaining chunk can be cut
    options = [
        CutSet([size], value) + get_optimal_cuts(chunk - size, values_by_size, cache)
        for size, value in values_by_size.items()
        if chunk >= size
    ]
    if not options:
        # Cannot be cut (any more)
        # The value of the remaining material raw chunk is negative!
        optimal_cuts = CutSet([], -chunk)
    else:
        # Get the optimal futher cuts for each option, and pick the one
        # resulting in the lartest total value
        optimal_cuts = max(options, key=lambda cut: cut.value)
    # Save the soution to cache
    cache[chunk] = optimal_cuts
    return optimal_cuts


if __name__ == '__main__':
    # Read the input data
    with open('./input.json', 'r') as input_file:
        material = json.load(input_file)
    # Print the optimal cuts as an ASCII table
    print("Gemstone  | Total value")
    print("----------|-------------")
    total_value = 0
    for gemstone, value in get_solution(material).items():
        total_value += value
        print("%9s | %d" % (gemstone, value))
    print("----------|-------------")
    print("Total     | %d" % total_value)
