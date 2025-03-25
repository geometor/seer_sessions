"""
Transforms an input grid into an output grid based on seed colors in the first row.
Seed colors propagate downwards, replacing gray pixels (value 5) within a contiguous block.
Propagation stops when a non-gray pixel or the grid boundary is encountered.  The propagation
expands to orthogonally adjacent pixels (flood fill).
"""

import numpy as np

def get_seed_colors(grid):
    """
    Extracts seed colors and their column indices from the first row of the grid.
    """
    seed_colors = {}
    for col, value in enumerate(grid[0]):
        if value != 0:  # 0 is assumed to be the background/black
            seed_colors[col] = value
    return seed_colors

def flood_fill(grid, row, col, seed_color):
    """
    Recursively fills a contiguous region of gray pixels with the seed color.
    """
    height, width = grid.shape
    if row < 0 or row >= height or col < 0 or col >= width or grid[row, col] != 5:
        return  # Stop if out of bounds or not a gray pixel

    grid[row, col] = seed_color  # Replace gray with seed color

    # Recursively fill adjacent pixels
    flood_fill(grid, row + 1, col, seed_color)  # Down
    flood_fill(grid, row - 1, col, seed_color)  # Up
    flood_fill(grid, row, col + 1, seed_color)  # Right
    flood_fill(grid, row, col - 1, seed_color)  # Left


def transform(input_grid):
    """
    Transforms the input grid according to the seed color propagation rule.
    """
    input_grid = np.array(input_grid)  # Convert to NumPy array
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Identify Seed Colors
    seed_colors = get_seed_colors(input_grid)

    # Column-Based Propagation with Flood Fill
    for col, seed_color in seed_colors.items():
        # Start flood fill from the row below the seed
        # Check the pixel below.  If it's a 5, start the flood fill from *that* location.
        if height > 1 and output_grid[1,col] == 5: #seed pixel is always row 0
            flood_fill(output_grid, 1, col, seed_color)
        # Handles edge case of single row input
        elif height > 1:
            flood_fill(output_grid, 1, col, seed_color)

    return output_grid.tolist()  # return to list format