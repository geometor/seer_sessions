"""
Iterate through each cell in the input grid. For each cell, check its immediate neighbors (left and right).
If a cell's value is different from both of its neighbors, remove it (change its value to 0).
If a cell's value is the same as *either* of its neighbors, keep it.
Cells at the edges of the grid are considered to *always* have a matching neighbor off the edge, so they are always kept.
Output the updated grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms a 1D grid by removing isolated cells."""

    output_grid = input_grid.copy()
    grid_length = len(input_grid)

    # Iterate over the grid, excluding edge cells
    for i in range(grid_length):
        # Get neighbor values, handling edge cases
        left_neighbor = input_grid[i - 1] if i > 0 else input_grid[i]
        right_neighbor = input_grid[i + 1] if i < grid_length - 1 else input_grid[i]

        # Check if the current cell is different from both neighbors
        if input_grid[i] != left_neighbor and input_grid[i] != right_neighbor:
            output_grid[i] = 0  # Remove the cell (set to 0)

    return output_grid