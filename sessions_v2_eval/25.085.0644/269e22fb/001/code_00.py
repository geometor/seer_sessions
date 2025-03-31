"""
Creates a 20x20 output grid by tiling four transformed versions of the input grid onto a background determined by the most frequent color in the input.

1.  Analyzes the input grid to find the most frequent color.
2.  Initializes a 20x20 output grid filled with this background color.
3.  Places the original input grid in the top-left corner.
4.  Places a horizontally flipped version of the input grid in the top-right corner.
5.  Places a vertically flipped version of the input grid in the bottom-left corner.
6.  Places a horizontally and vertically flipped version of the input grid in the bottom-right corner.
7.  Later placements overwrite earlier ones in case of overlap.
"""

import numpy as np
from collections import Counter

def find_most_frequent_color(grid):
    """Finds the most frequent color value in the grid."""
    unique, counts = np.unique(grid, return_counts=True)
    most_frequent_index = np.argmax(counts)
    return unique[most_frequent_index]

def flip_horizontal(grid):
    """Flips the grid horizontally."""
    return np.fliplr(grid)

def flip_vertical(grid):
    """Flips the grid vertically."""
    return np.flipud(grid)

def transform(input_grid):
    """
    Transforms the input grid according to the described tiling and flipping rules.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 20x20 numpy array representing the transformed output grid.
    """
    input_h, input_w = input_grid.shape

    # 1. Find the most frequent color in the input grid.
    background_color = find_most_frequent_color(input_grid)

    # 2. Create a new 20x20 grid filled with the background color.
    output_grid = np.full((20, 20), background_color, dtype=input_grid.dtype)

    # 3. Get dimensions for placement calculations.
    h, w = input_h, input_w

    # 4. Place the original input grid in the top-left region.
    output_grid[0:h, 0:w] = input_grid

    # 5. Create a horizontally flipped version and place it in the top-right region.
    flipped_h = flip_horizontal(input_grid)
    output_grid[0:h, 20-w:20] = flipped_h

    # 6. Create a vertically flipped version and place it in the bottom-left region.
    flipped_v = flip_vertical(input_grid)
    output_grid[20-h:20, 0:w] = flipped_v

    # 7. Create a doubly flipped (horizontal and vertical) version and place it in the bottom-right region.
    flipped_hv = flip_horizontal(flip_vertical(input_grid)) # or flip_vertical(flip_horizontal(input_grid))
    output_grid[20-h:20, 20-w:20] = flipped_hv

    # 8. Return the final output grid.
    return output_grid