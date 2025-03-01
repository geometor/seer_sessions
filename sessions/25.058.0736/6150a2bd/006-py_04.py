"""
The input is a grid (2D array) of numbers, where each number represents a color. The transformation is a 90-degree clockwise rotation of the grid. The output is the rotated grid, with the same color values as the input, but in their new positions.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_np = np.array(input_grid)

    # Rotate the grid 90 degrees clockwise.  NumPy's rot90 function rotates
    # counter-clockwise by default, so we use k=-1 to achieve clockwise rotation.
    output_np = np.rot90(input_np, k=-1)

    # Convert the rotated NumPy array back to a list of lists.
    output_grid = output_np.tolist()

    return output_grid