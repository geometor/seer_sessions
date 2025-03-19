# d10ecb37 • 012 • refine_coder

---
```python
"""
The input grid is divided into four quadrants. For each quadrant, the most frequently occurring color *other than the background color* is determined. A 2x2 output grid is constructed where each cell's color corresponds to the most frequent non-background color in the respective quadrant of the input grid. The background is assumed to be the overall most frequent color of the grid.
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

def most_frequent_non_background_color(grid, background_color):
    """
    Finds the most frequent color in a grid, excluding the background color.

    Args:
        grid: A 2D numpy array representing the grid.
        background_color: background color

    Returns:
        The value (color) that appears most frequently in the grid, or the background color if no other colors.
    """
    # Flatten the grid to 1D and count color occurrences
    counts = Counter(grid.flatten())
    
    # Remove the background color from the counts
    if background_color in counts:
      del counts[background_color]

    # most_common returns a list of tuples (value, count) sorted by count
    if len(counts) > 0:
       most_common_color = counts.most_common(1)[0][0]
    else:
       most_common_color = background_color # if no other colors, return background
    return most_common_color

def get_background(grid):
    """
        Gets the background color
    """
    counts = Counter(grid.flatten())
    # most_common returns a list of tuples (value, count) sorted by count
    most_common_color = counts.most_common(1)[0][0]
    return most_common_color


def transform(input_grid):
    """
    Transforms an input grid into a 2x2 output grid.  Each cell in the output
    grid represents the most frequent color in the corresponding quadrant of
    the input grid.

    Args:
        input_grid: A 2D numpy array representing the input.

    Returns:
        A 2x2 numpy array representing the transformed output.
    """
    # Initialize the output grid as a 2x2 array filled with zeros (or any default value)
    output_grid = np.zeros((2, 2), dtype=int)

    # get background
    background_color = get_background(input_grid)

    # Determine the most frequent color for each quadrant and set the corresponding output cell
    output_grid[0, 0] = most_frequent_non_background_color(get_quadrant(input_grid, 'top_left'), background_color)
    output_grid[0, 1] = most_frequent_non_background_color(get_quadrant(input_grid, 'top_right'), background_color)
    output_grid[1, 0] = most_frequent_non_background_color(get_quadrant(input_grid, 'bottom_left'), background_color)
    output_grid[1, 1] = most_frequent_non_background_color(get_quadrant(input_grid, 'bottom_right'), background_color)

    return output_grid
```
