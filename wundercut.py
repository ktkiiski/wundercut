#!/usr/bin/env python
from __future__ import unicode_literals
import json

def get_optimal_cuts(material):
    """
    Finds and returns the optimal cuts for the given material (input data).
    Returns a dict where keys are gemstone type and values are the list of optimal cut sizes.
    """
    return {'todo': [1,2,3]}


if __name__ == '__main__':
    # Read the input data
    with open('./input.json', 'r') as input_file:
        material = json.load(input_file)
    # Print the optimal cuts as an ASCII table
    print("Gemstone  | Cuts")
    print("----------|----------------")
    for gemstone, cuts in get_optimal_cuts(material).items():
        print("%9s | %s" % (gemstone, ", ".join(str(size) for size in cuts)))
