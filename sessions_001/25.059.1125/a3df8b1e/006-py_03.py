"""
The transformation creates a checkerboard-like pattern. The input grid is filled with a single color. The output grid uses two colors: the original color and the next color in the sequence (wrapping around from 9 back to 0). These two colors alternate in a checkerboard pattern.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Get the input color
    input_color = input_grid[0, 0]
    # Determine the second color (next in sequence)
    second_color = (input_color + 1) % 10

    # change output pixels 
    for c in range(cols):
        for r in range(rows):
            if c % 2 == 0:  # Even column
                output_grid[r, c] = input_color if r % 2 == 0 else second_color
            else:  # Odd column
                output_grid[r, c] = second_color if r % 2 == 0 else input_color

    return output_grid