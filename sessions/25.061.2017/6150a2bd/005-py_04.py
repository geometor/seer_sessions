"""
The transformation involves a 90-degree clockwise rotation of the input grid. The input grid's rows become the output grid's columns, and the input grid's columns become the output grid's rows, but inverted.
"""

import numpy as np
from typing import List, Tuple, Dict

def transform(input_grid):
    # Initialize output grid with swapped dimensions
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((cols, rows), dtype=int)

    # Rotate the grid 90 degrees clockwise
    for i in range(rows):
        for j in range(cols):
            output_grid[j][rows - 1 - i] = input_grid[i][j]

    return output_grid