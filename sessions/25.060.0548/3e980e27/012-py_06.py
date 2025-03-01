"""
The transformation rule is to identify 3x3 blocks in the input grid. If a 3x3 block is entirely filled with a non-zero color, and that block is at the edge of the grid, extend that block by one layer (duplicating the edge row or column) if possible, within the boundary of the output grid. The shape of input and output grids are always identical.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extending 3x3 blocks at the edge.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)  # Start with a copy of the input
    rows, cols = input_grid.shape

    for r in range(rows - 2):
        for c in range(cols - 2):
            block = input_grid[r:r+3, c:c+3]
            # Check if the 3x3 block is uniform and non-zero
            if np.all(block) and block[0,0] != 0:
                # Check if it is the upper edge
                if r == 0 and rows > 3:
                    output_grid = np.insert(output_grid, 3, output_grid[2, :], axis = 0)
                    output_grid = np.delete(output_grid, -1, axis = 0)
                # Check if it is the bottom edge
                if r == rows - 3 and rows >3:
                    output_grid = np.insert(output_grid, r, output_grid[r, :], axis = 0)
                    output_grid = np.delete(output_grid, 0, axis = 0)
                # Check if it is the left edge
                if c == 0 and cols > 3:
                    output_grid = np.insert(output_grid, 3, output_grid[:, 2], axis = 1)
                    output_grid = np.delete(output_grid, -1, axis = 1)
                # check if it is the right edge
                if c == cols - 3 and cols > 3:
                    output_grid = np.insert(output_grid, c, output_grid[:, c], axis = 1)
                    output_grid = np.delete(output_grid, 0, axis = 1)

    return output_grid.tolist()