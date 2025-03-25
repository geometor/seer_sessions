"""
Iterate through each cell of the input grid. If the color is white (0), keep it as white (0) in the output grid. If the color is yellow (4) or green (3), change it to magenta (6) in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by replacing yellow (4) and green (3) pixels with magenta (6),
    while keeping white (0) pixels unchanged.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)  # Start with a copy to preserve unchanged pixels.

    # Iterate through each cell of the input grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check the color of the current cell.
            if output_grid[i, j] == 4 or output_grid[i, j] == 3:
                # Change yellow (4) or green (3) to magenta (6).
                output_grid[i, j] = 6
            # White (0) remains unchanged, so no 'else' is needed.

    return output_grid