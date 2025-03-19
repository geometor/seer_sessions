"""
The output is a 1x1 grid. The color of the single pixel in the output grid is
the most frequent color appearing in the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Finds the most frequent color in the input grid and returns it as a 1x1 grid.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        list of lists: A 1x1 grid containing the most frequent color.
    """
    # Convert input_grid to numpy array for easier manipulation
    input_array = np.array(input_grid)

    # Find the unique colors and their counts
    unique, counts = np.unique(input_array, return_counts=True)

    # Find the index of the most frequent color
    most_frequent_index = np.argmax(counts)

    # Get the most frequent color
    most_frequent_color = unique[most_frequent_index]

    # Create output grid, a 1x1 matrix with the most frequent color
    output_grid = np.array([[most_frequent_color]])

    return output_grid.tolist()