"""
Transforms an input grid into an output grid based on seed colors in the first row.
Seed colors propagate downwards in their respective columns, replacing gray pixels (value 5) within a contiguous block.
Propagation stops when a non-gray pixel or the grid boundary is encountered.
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

def transform(input_grid):
    """
    Transforms the input grid according to the seed color propagation rule.
    """
    input_grid = np.array(input_grid)  # Convert to NumPy array
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Identify Seed Colors
    seed_colors = get_seed_colors(input_grid)

    # Column-Based Propagation
    for col, seed_color in seed_colors.items():
        # Start propagation from the row below the seed pixel
        for row in range(1, height):
            # Stop if we hit a non-gray pixel or the bottom
            if output_grid[row, col] != 5:
                break
            output_grid[row, col] = seed_color  # Replace with seed color

    return output_grid.tolist()  # return to list format
