"""
The output is a 2x2 grid. Each cell in the output grid corresponds to a quadrant of the input grid.
If a quadrant contains only one color, that color is used in the output grid. If a quadrant contains
more than one color, check the horizontally mirrored quadrant. If they're the same, output the
most frequent. If the horizontally mirrored quadrant is different, then output the same value as
the mirrored quadrant.
"""

import numpy as np
from collections import Counter

def get_quadrant(grid, quadrant):
    """
    Extracts a specified quadrant from a 2D numpy array.

    Args:
        grid: A 2D numpy array.
        quadrant: A string indicating the desired quadrant ('top_left', 'top_right', 'bottom_left', 'bottom_right').

    Returns:
        A 2D numpy array representing the specified quadrant.
        Raises ValueError if the quadrant string is invalid
    """
    rows, cols = grid.shape
    mid_row = rows // 2
    mid_col = cols // 2

    if quadrant == 'top_left':
        return grid[:mid_row, :mid_col]
    elif quadrant == 'top_right':
        return grid[:mid_row, mid_col:]
    elif quadrant == 'bottom_left':
        return grid[mid_row:, :mid_col]
    elif quadrant == 'bottom_right':
        return grid[mid_row:, mid_col:]
    else:
        raise ValueError("Invalid quadrant specified.")

def most_frequent_color(grid):
    """
    Finds the most frequent color in a grid.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        The value (color) that appears most frequently in the grid.
    """
    # Flatten the grid to 1D and count color occurrences
    counts = Counter(grid.flatten())
    # most_common returns a list of tuples (value, count) sorted by count
    most_common_color = counts.most_common(1)[0][0]
    return most_common_color

def get_unique_colors(grid):
    """Returns a set of unique colors in the grid."""
    return set(grid.flatten())

def transform(input_grid):
    # Initialize the output grid as a 2x2 array filled with zeros.
    output_grid = np.zeros((2, 2), dtype=int)

    # Define quadrant names and their horizontal mirrors
    quadrant_map = {
        'top_left': 'top_right',
        'top_right': 'top_left',
        'bottom_left': 'bottom_right',
        'bottom_right': 'bottom_left'
    }
    quadrant_indices = {
        'top_left': (0, 0),
        'top_right': (0, 1),
        'bottom_left': (1, 0),
        'bottom_right': (1, 1)
    }
    # Iterate through each quadrant
    for quad_name, mirror_name in quadrant_map.items():
        quadrant = get_quadrant(input_grid, quad_name)
        unique_colors = get_unique_colors(quadrant)
        row, col = quadrant_indices[quad_name]

        if len(unique_colors) == 1:
           output_grid[row, col] = list(unique_colors)[0]
        else:
            mirror_quadrant = get_quadrant(input_grid, mirror_name)
            mirror_unique = get_unique_colors(mirror_quadrant)
            if unique_colors == mirror_unique:
               output_grid[row,col] = most_frequent_color(quadrant)
            else:
               mirror_row, mirror_col = quadrant_indices[mirror_name]
               output_grid[row,col] = output_grid[mirror_row, mirror_col] # take from mirrored value

    return output_grid