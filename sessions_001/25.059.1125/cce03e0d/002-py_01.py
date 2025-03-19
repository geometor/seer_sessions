"""
Transforms a 3x3 input grid into a 9x9 output grid by replicating and positioning the non-zero elements of the input grid in a specific pattern within the output grid.  The input grid's elements are placed in the top-left and bottom-right 3x3 quadrants of the output grid, effectively creating four copies of the input arrangement within the larger grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid into a 9x9 output grid.
    """
    # Initialize a 9x9 output grid filled with 0s.
    output_grid = np.zeros((9, 9), dtype=int)

    # Iterate through the input grid.
    for r in range(3):
        for c in range(3):
            # Check for non-zero elements.
            if input_grid[r, c] != 0:
                # Calculate and set output grid coordinates.
                output_grid[r + (0 * 3), c + (0 * 3)] = input_grid[r, c]  # Top-left
                output_grid[r + (0 * 3), c + (2 * 3)] = input_grid[r, c]  # Top-Right
                output_grid[r + (2 * 3), c + (0 * 3)] = input_grid[r, c]  # Bottom-left
                output_grid[r + (2 * 3), c + (2 * 3)] = input_grid[r, c]  # Bottom-right


    return output_grid