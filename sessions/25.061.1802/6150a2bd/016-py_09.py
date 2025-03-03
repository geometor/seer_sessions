"""
The input grid is reflected along its horizontal axis (x-axis). This is equivalent to flipping the grid vertically.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array
    input_grid = np.array(input_grid)

    # Flip the grid vertically (reflect along the x-axis)
    output_grid = np.flipud(input_grid)

    return output_grid.tolist()