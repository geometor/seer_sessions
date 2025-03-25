"""
The transformation rule involves shifting each row of the input grid down by one position in the output grid. The top row of the input becomes the second row of the output, and the top row of the output is filled with zeros.
"""

import numpy as np

def shift_down(grid):
    """Shifts all rows in the grid down by one position, filling the top row with zeros."""
    rows, cols = grid.shape
    new_grid = np.zeros_like(grid)
    new_grid[1:] = grid[:-1]
    return new_grid

def transform(input_grid):
    """Shifts each row of the input grid down by one position in the output grid. The top row becomes the second, and the top is filled with zeros."""
    # Convert input grid to numpy array
    input_grid = np.array(input_grid)

    # Shift rows down
    output_grid = shift_down(input_grid)

    return output_grid.tolist()