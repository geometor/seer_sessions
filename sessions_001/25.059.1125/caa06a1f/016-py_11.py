"""
The transformation rule is to switch the two primary colors of the checkerboard pattern and remove the last row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by swapping the two primary colors of the checkerboard
    pattern and removing the last row.
    """
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    
    # Find the two most frequent colors, excluding the color in the last row (assumed to be an outlier)
    unique_colors, counts = np.unique(input_grid[:-1], return_counts=True)
    sorted_indices = np.argsort(counts)[::-1]  # Indices of colors sorted by frequency (descending)
    color1 = unique_colors[sorted_indices[0]]
    color2 = unique_colors[sorted_indices[1]]

    # Swap the colors
    output_grid[input_grid == color1] = -1  # Temporary value for color1
    output_grid[input_grid == color2] = color1
    output_grid[output_grid == -1] = color2

    # Remove the last row
    output_grid = output_grid[:-1]
    
    return output_grid