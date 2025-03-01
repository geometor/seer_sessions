"""
1.  **Replace**: Change all red (2) pixels in the input grid to green (3).
2.  **Expansion and Replication**: For each green pixel in the modified input grid, create a 4x4 block of green pixels in the output grid. The top-left corner of each 4x4 block corresponds to a cell that had a value of 2 or 3 in the original input. Empty cells are filled with a value of 0. More precisely, the green and red cells in the input map to the top-left corner of the 4 x 4 green areas in the output.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    input_grid = np.array(input_grid)

    # Replace red (2) with green (3)
    modified_input = np.where(input_grid == 2, 3, input_grid)

    # Initialize output grid with zeros, making it 3 times the size of the input
    output_grid = np.zeros((input_grid.shape[0] * 3, input_grid.shape[1] * 3), dtype=int)

    # Iterate through the modified input grid
    for i in range(modified_input.shape[0]):
        for j in range(modified_input.shape[1]):
            if modified_input[i, j] == 3:
                # Create a 4x4 block of green (3) pixels in the output grid
                output_grid[i * 3 : i * 3 + 4, j * 3: j * 3 + 4] = 3

    return output_grid.tolist()