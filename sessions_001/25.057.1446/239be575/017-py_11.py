"""
The transformation rule determines the most frequent color in the input grid and returns a 1x1 grid containing that color.
"""

import numpy as np

def transform(input_grid):
    """
    Identifies the most frequent color in the input grid and returns a 1x1 grid with that color.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        list of lists: A 1x1 grid containing the most frequent color.
    """
    # Convert input_grid to numpy array for easier manipulation
    input_array = np.array(input_grid)

    # Count the occurrences of each color
    unique, counts = np.unique(input_array, return_counts=True)
    color_counts = dict(zip(unique, counts))

    # Find the most frequent color
    most_frequent_color = max(color_counts, key=color_counts.get)

    # Create output grid, a 1x1 matrix with the most frequent color
    output_grid = np.array([[most_frequent_color]])

    return output_grid.tolist()