"""
The program performs a color substitution on a pixel grid. It iterates through each cell of the input grid.
If a cell is yellow (4), it's changed to grey (5). If a cell is red (2) or green (3), it's changed to white (0).
All other colors remain unchanged (although no other colors are present in this example).
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified color mapping."""
    # Initialize output_grid with the same dimensions as the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid and apply color changes
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if input_grid[i, j] == 4:  # Yellow to grey
                output_grid[i, j] = 5
            elif input_grid[i, j] == 2 or input_grid[i, j] == 3:  # Red or Green to white
                output_grid[i, j] = 0

    return output_grid