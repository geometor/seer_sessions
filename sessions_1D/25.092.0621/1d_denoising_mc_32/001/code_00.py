"""
Analyzes the input grid (represented as a list of integers) to find the most frequent non-white (0) color (the "main color").
It then creates an output grid where all non-white pixels that are not the "main color" are replaced with the "main color".
White pixels remain unchanged.
"""

import numpy as np
from collections import Counter

def find_main_color(grid):
    """
    Finds the most frequent non-white color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The value of the most frequent non-white color. 
             Returns -1 if no non-white colors are found.
    """
    # Filter out white pixels (value 0)
    non_white_pixels = grid[grid != 0]

    # Handle case where the grid is all white or empty
    if non_white_pixels.size == 0:
        return -1 # Or handle as appropriate, maybe return 0 if white is considered default?

    # Count frequencies of non-white colors
    color_counts = Counter(non_white_pixels)

    # Find the color with the highest frequency
    main_color = color_counts.most_common(1)[0][0]
    return main_color

def transform(input_grid):
    """
    Replaces less frequent non-white colors with the most frequent non-white color.

    Args:
        input_grid (list): A list of integers representing the input grid pixels.

    Returns:
        list: A list of integers representing the transformed output grid pixels.
    """
    # Convert input list to a numpy array for efficient processing
    grid_np = np.array(input_grid)

    # Find the main color (most frequent non-white color)
    main_color = find_main_color(grid_np)

    # Initialize the output grid as a copy of the input
    output_grid_np = grid_np.copy()

    # Iterate through the grid and replace 'impurity' colors
    for i in range(output_grid_np.size):
        # Check if the pixel is not white and not the main color
        if output_grid_np[i] != 0 and output_grid_np[i] != main_color:
            # Replace it with the main color
            output_grid_np[i] = main_color

    # Convert the numpy array back to a list for the final output
    return output_grid_np.tolist()