"""
Transforms an input grid into an output grid of the same dimensions, 
where the output grid is filled entirely with a single color. 
The color is selected from the last column, specifically the one in the middle row.
"""

import numpy as np

def get_middle_element_from_last_column(grid):
    """Helper function to get the middle element from the last column of a 2D array."""
    last_column = grid[:, -1]
    middle_index = len(last_column) // 2
    return last_column[middle_index]

def transform(input_grid):
    """
    Transforms the input grid based on the described rule.
    """
    # Convert input_grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)

    # Identify Dimensions: Get the dimensions of the input grid
    rows, cols = input_grid.shape

    # Select Color: Determine the output color by picking the middle from last column
    selected_color = get_middle_element_from_last_column(input_grid)

    # Create Output Grid: Initialize an output grid with the same dimensions, filled with the selected color
    output_grid = np.full((rows, cols), selected_color)

    # Return the output grid
    return output_grid.tolist()