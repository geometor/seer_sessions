"""
The transformation rule can be described as follows:

1.  Take the input grid.
2.  Reverse the order of the rows.
3.  The resulting grid with reversed rows is the output grid.

Essentially, the output is a vertically flipped version of the input.
Or another way, reverse the order of the array elements, where each element is a row from the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = []

    # reverse the rows of the input and set as the output
    output_grid = input_grid[::-1]

    return output_grid