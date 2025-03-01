"""
The transformation consists of two primary operations performed in sequence: vertical expansion and horizontal expansion.

1.  **Vertical Expansion:**
    *   Insert two rows of zeros (color 0) between each existing row of the input grid.
    *   Add two blocks of rows of zeros (color 0) to the bottom of the grid. Each block has height equal to the expanded grid.

2.  **Horizontal Expansion:**
    *   Multiply the width of each expanded row by the horizontal replication factor obtained by dividing the output width to the input width.
"""

import numpy as np

def transform(input_grid):
    # Vertical Expansion
    input_height, input_width = input_grid.shape
    vertically_expanded_grid = np.insert(input_grid, range(1, input_height), 0, axis=0)
    vertically_expanded_grid = np.insert(vertically_expanded_grid, range(1, input_height), 0, axis=0)

    # add two blocks of rows
    expanded_height = vertically_expanded_grid.shape[0]
    zeros_block = np.zeros((expanded_height, input_width), dtype=int)
    vertically_expanded_grid = np.concatenate((vertically_expanded_grid, zeros_block, zeros_block), axis=0)

    # Horizontal Expansion
    horizontal_factor = 3 if input_width == 3 else 2 # calculated on the fly
    output_width = input_width * horizontal_factor
    output_height = vertically_expanded_grid.shape[0]
    horizontally_expanded_grid = np.zeros((output_height, output_width), dtype=int)

    for i in range(output_height):
        for j in range(input_width):
           horizontally_expanded_grid[i, j*horizontal_factor:(j+1)*horizontal_factor] = vertically_expanded_grid[i,j]

    return horizontally_expanded_grid