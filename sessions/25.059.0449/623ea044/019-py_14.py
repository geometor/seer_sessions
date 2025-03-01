"""
1.  **Identify Seed:** Find the single azure (value 8) pixel within the input grid. This is the "seed" pixel.
2.  **Initialize Output:** Create an output grid filled with zeros (black), with the same dimensions as the input grid.
3.  **Place Seed:** Copy the seed pixel (azure) to its corresponding location in the output grid.
4.  **Diagonal Expansion**: From the seed pixel's location, expand the azure color diagonally in all four directions (up-left, up-right, down-left, down-right).
5.  **Boundary Condition:** Continue the diagonal expansion until the edges of the grid are reached in each direction. The expansion does not wrap around.
"""

import numpy as np

def find_seed_pixel(grid):
    # Find the coordinates of the azure (8) pixel.
    rows, cols = np.where(grid == 8)
    if len(rows) > 0:
        return rows[0], cols[0]
    return None

def transform(input_grid):
    # Initialize output_grid as a zero-filled array with the same dimensions as the input.
    output_grid = np.zeros_like(input_grid)

    # Find the seed pixel (azure pixel).
    seed_coords = find_seed_pixel(input_grid)
    if seed_coords is None:
        return output_grid  # Return if no seed pixel is found

    seed_row, seed_col = seed_coords

    # Place the seed pixel in the output grid.
    output_grid[seed_row, seed_col] = 8

    # Get grid dimensions.
    height, width = input_grid.shape

    # Expand diagonally in all four directions.
    for i in range(1, max(height, width)):
        # Up-left
        if seed_row - i >= 0 and seed_col - i >= 0:
            output_grid[seed_row - i, seed_col - i] = 8
        # Up-right
        if seed_row - i >= 0 and seed_col + i < width:
            output_grid[seed_row - i, seed_col + i] = 8
        # Down-left
        if seed_row + i < height and seed_col - i >= 0:
            output_grid[seed_row + i, seed_col - i] = 8
        # Down-right
        if seed_row + i < height and seed_col + i < width:
            output_grid[seed_row + i, seed_col + i] = 8

    return output_grid