"""
The input grid is replicated four times in a 2x2 matrix arrangement.  The replicas have three pixels of spacing between their edges. The output grid dimensions are calculated as follows: width = input_width * 2 + 3, height = input_height * 2 + 3. The space surrounding the replicated grids is filled with white (0).
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = input_height * 2 + 3
    output_width = input_width * 2 + 3

    # Initialize output_grid with zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate and place the input grid in a 2x2 pattern
    for i in range(2):
        for j in range(2):
            # Calculate the starting row and column for each replica
            start_row = i * (input_height + 3)
            start_col = j * (input_width + 3)

            # Place the replica into the output grid
            output_grid[start_row:start_row + input_height, start_col:start_col + input_width] = input_grid

    return output_grid