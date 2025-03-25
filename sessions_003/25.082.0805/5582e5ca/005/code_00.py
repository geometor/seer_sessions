"""
The transformation rule identifies the most frequent value in the input grid.
The output grid has the same dimensions as the input grid, and every cell
in the output grid is filled with the most frequent value from the input grid.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)

    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Find the most frequent value in the input grid.
    counts = Counter(input_grid.flatten())
    most_frequent_value = counts.most_common(1)[0][0]

    # Create a new grid of the same dimensions, filled with the most frequent value.
    output_grid = np.full((rows, cols), most_frequent_value)

    return output_grid.tolist()