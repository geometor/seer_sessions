"""
The program takes a grid as input.
Change all pixels of input to orange(7).
Output is a single orange cell of value 7.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a 1x1 numpy array with value 7
    output_grid = np.array([[7]])

    return output_grid