#!/usr/bin/env python
from __future__ import unicode_literals
import json


class CutSet:
    def __init__(self, cuts, waste, values_by_size):
        self.cuts = cuts
        self.waste = waste
        self.values_by_size = values_by_size
    
    def cut(self, size, value):
        """
        Cuts a piece from the remaining waste, adding the value to the total
        value of the cuts, and decreasing the amount of waste.
        """
        return CutSet(self.cuts + [size], self.waste - size, self.values_by_size)

    @property
    def value(self):
        return sum((self.values_by_size[size] for size in self.cuts), 0) - self.waste


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
        (
            get_total_value(cuts, waste, cut_options) for cuts, waste in
            (get_optimal_cuts(chunk, cut_options, cache) for chunk in chunks)
        ),
        0
    )


def get_optimal_cuts(chunk, values_by_size, cache):
    # Check if there is an optimal solution in the cache
    if chunk in cache:
        return cache[chunk]
    # Get all possible options that the raw/remaining chunk can be cut
    options = [
        (size, get_optimal_cuts(chunk - size, values_by_size, cache))
        for size, value in values_by_size.items()
        if chunk >= size
    ]
    if not options:
        # Cannot be cut (any more)
        optimal_cuts = ([], chunk)
    else:
        # Get the optimal futher cuts for each option, and pick the one
        # resulting in the lartest total value
        optimal_cuts = max(
            (([size] + cuts, waste) for size, (cuts, waste) in options),
            key=lambda x: get_total_value(x[0], x[1], values_by_size)
        )
    # Save the soution to cache
    cache[chunk] = optimal_cuts
    return optimal_cuts


def get_total_value(cuts, waste, values_by_size):
    return sum((values_by_size[size] for size in cuts), 0) - waste


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
