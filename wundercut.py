#!/usr/bin/env python
from __future__ import unicode_literals
import json

with open('./input.json', 'r') as input_file:
    material = json.load(input_file)

if __name__ == '__main__':
    print(json.dumps(material))
