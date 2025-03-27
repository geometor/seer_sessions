"""
The transformation rule involves identifying all distinct, contiguous regions of non-background
pixels, each considered an "object." The background is the most frequent color. These objects are then stacked row-wise
in the output grid, starting from the top row (row 0). The order of stacking is determined by
reading the input grid in *reverse* row order (bottom to top). Within each row band,
the objects' original horizontal (column) positions are preserved.
"""

import numpy as np
from collections import Counter

def find_objects(grid, background_color):
    """
    Finds contiguous objects (same color pixels) in a grid, excluding the background color.

    Args:
        grid (np.array): The input grid.
        background_color: The color of the background

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited and grid[row,col] != background_color:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append(current_object)
    return objects

def get_background_color(grid):
    """
    Determine the background color based on the most frequent color in the grid
    """
    # Flatten the grid and count color occurrences
    color_counts = Counter(grid.flatten())
    # Get the most common color (background color)
    background_color = color_counts.most_common(1)[0][0]
    return background_color

def transform(input_grid):
    """
    Transforms the input grid by stacking objects row-wise from bottom to top.
    """
    input_grid = np.array(input_grid)

    # Determine the background color
    background_color = get_background_color(input_grid)

    output_grid = np.full(input_grid.shape, background_color)  # Initialize with background color

    # Find objects, excluding background
    objects = find_objects(input_grid, background_color)

    # Sort objects by their *maximum* row index in *descending* order (bottom to top)
    objects.sort(key=lambda obj: max(row for row, _ in obj), reverse=True)

    current_row = 0
    for obj in objects:
        # Find the height of this object
        min_obj_row = min(row for row, _ in obj)
        max_obj_row = max(row for row, _ in obj)
        obj_height = max_obj_row - min_obj_row + 1

        # Place the object in the output grid, preserving original column positions
        for row, col in obj:
            output_grid[current_row + row - min_obj_row , col] = input_grid[row, col]

        current_row += obj_height  # Move to the next available row band

    return output_grid.tolist()