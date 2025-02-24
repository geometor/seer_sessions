"""
Counts the number of distinct colors other than white in the input grid. The
output is a 1x1 grid containing this count, represented as a blue pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to output the count of distinct colors other than white.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The output grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Find unique colors in the input grid.
    unique_colors = np.unique(input_array)

    # Exclude white (0) from the count.
    distinct_colors_count = len(unique_colors[unique_colors != 0])
    
    # Create output grid
    output_grid = np.array([[distinct_colors_count]])

    return output_grid