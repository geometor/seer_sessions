"""
The program always outputs a 3x3 grid with a central azure stripe, regardless of the input. The input is essentially ignored.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Populate central column with 8 (azure)
    output_grid[:, 1] = 8

    return output_grid