"""
The transformation extracts the leftmost third of the input grid. 
The input grid consists of a pattern repeated horizontally three times. 
The output grid is the first instance of this repeating pattern.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the leftmost third of the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the leftmost third of the input grid.
    """
    # Determine the height (H) and width (W_in) of the input grid.
    input_height, input_width = input_grid.shape

    # Calculate the width of the output grid (W_out), which is one-third of the input width.
    # Use integer division to ensure the width is an integer.
    output_width = input_width // 3

    # Create the output grid by selecting the columns from 0 up to (but not including) output_width.
    # This effectively extracts the leftmost third of the input grid.
    # The height remains the same.
    output_grid = input_grid[:, :output_width]

    # Return the resulting grid.
    return output_grid
