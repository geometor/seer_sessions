"""
The function identifies unique colors in the input grid (excluding 0),
orders them based on the top-most, then left-most color, and outputs a list of colors.
"""

import numpy as np

def find_top_left_unique_colors(grid):
    """Finds unique colors, ordered by top-most, then left-most appearance."""
    unique_colors = []
    added_colors = set() # Use a set to track colors that have already been added.

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and color not in added_colors:
                unique_colors.append(color)
                added_colors.add(color)
    return unique_colors


def transform(input_grid):
    """Transforms the input grid into a sequence of unique colors."""
    # Convert to numpy array for easier manipulation.
    grid = np.array(input_grid)

    # Find unique colors, ordered by top-left appearance.
    ordered_colors = find_top_left_unique_colors(grid)
    
    # Convert the list of colors into a nested list (required output format).
    output_grid = [[color] for color in ordered_colors]


    return output_grid