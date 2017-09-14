#!/usr/bin/env python
from __future__ import unicode_literals
import json

def get_solution(material):
    """
    Finds and returns the optimal cuts for the given material (input data).
    Returns a dict where keys are gemstone type and values are the list of optimal cut sizes.
    """
    return {
        gemstone: get_optimal_cuts(info['cuts'], info['rawChunks'])
        for gemstone, info in material.items()
    }


def get_optimal_cuts(cuts, chunks):
    """
    Determines the optimal chunks for the given gemstone type, by using
    the given possible cut sizes/values and the raw chunks.
    """
    # TODO
    return [1,2,3]

if __name__ == '__main__':
    # Read the input data
    with open('./input.json', 'r') as input_file:
        material = json.load(input_file)
    # Print the optimal cuts as an ASCII table
    print("Gemstone  | Cuts")
    print("----------|----------------")
    for gemstone, cuts in get_solution(material).items():
        print("%9s | %s" % (gemstone, ", ".join(str(size) for size in cuts)))
