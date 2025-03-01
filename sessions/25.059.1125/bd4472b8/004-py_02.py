"""
The transformation rule involves identifying the colors in the first two rows of the input grid and then replicating these colors vertically downwards in the output grid. The first row colors (red, blue, and yellow) form a repeating pattern, and the second row color (gray) is also replicated.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replicating the colors from the first two rows vertically downwards.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed output grid.
    """
    # Get the colors from the first two rows
    first_row_colors = input_grid[0]
    second_row_colors = input_grid[1]

    # Initialize the output grid with the same width and adjusted height
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1]), dtype=int)

    # Replicate first_row_colors three times starting at row index 2
    output_grid[2] = first_row_colors
    output_grid[5] = first_row_colors

    # Replicate first_row_colors two times starting at row index 3
    output_grid[3] = second_row_colors
    output_grid[6] = second_row_colors

    #Replicate the pattern down the rows of output grid
    output_grid[4] = first_row_colors
    output_grid[7] = first_row_colors
    
    # Copy first and second row colors
    output_grid[0] = first_row_colors
    output_grid[1] = second_row_colors


    return output_grid