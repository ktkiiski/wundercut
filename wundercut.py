#!/usr/bin/env python
from __future__ import unicode_literals
import json


class CutSet:
    def __init__(self, cuts, value, waste):
        self.cuts = cuts
        self.value = value
        self.waste = waste
    
    def cut(self, size, value):
        """
        Cuts a piece from the remaining waste, adding the value to the total
        value of the cuts, and decreasing the amount of waste.
        """
        return CutSet(self.cuts + [size], self.value + value, self.waste - size)

    @property
    def total_value(self):
        return self.value - self.waste


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
    cut_options = [(cut['size'], cut['value']) for cut in cuts]
    # As the optimal solution is the same to all raw sizes,
    # use a cache dict to remember them.
    cache = {}
    return sum(
        (
            get_optimal_cuts(CutSet([], 0, chunk), cut_options, cache).total_value
            for chunk in chunks
        ),
        0
    )


def get_optimal_cuts(cut_set, cut_options, cache):
    # Check if there is an optimal solution in the cache
    if cut_set.waste in cache:
        return cache[cut_set.waste]
    # Get all possible options that the raw/remaining chunk can be cut
    options = [
        cut_set.cut(size, value) for size, value in cut_options
        if cut_set.waste >= size
    ]
    if not options:
        # Cannot be cut (any more)
        optimal_cut_set = cut_set
    else:
        # Get the optimal futher cuts for each option, and pick the one
        # resulting in the lartest total value
        optimal_cut_set = max(
            (
                get_optimal_cuts(cut_set, cut_options, cache)
                for cut_set in options
            ),
            key=lambda cut_set: cut_set.total_value
        )
    # Save the soution to cache
    cache[cut_set.waste] = optimal_cut_set
    return optimal_cut_set


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
