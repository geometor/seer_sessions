"""
The transformation "grows" red areas by converting adjacent gray pixels to red, while preserving the black background and un-converted gray pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing gray (5) pixels with red (2) pixels
    based on proximity to existing red pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Initialize the output grid with the same dimensions and values as the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid.
    for i in range(rows):
        for j in range(cols):
            # Conditional Replacement: Check if the pixel is gray (5).
            if input_grid[i, j] == 5:
                # Neighbor Proximity Rule (Adjacency-based).
                # Check for adjacent red (2) pixels in the input grid.
                is_adjacent_to_red = False
                # Check horizontal and vertical neighbors.
                if i > 0 and input_grid[i - 1, j] == 2:  # Up
                    is_adjacent_to_red = True
                if i < rows - 1 and input_grid[i + 1, j] == 2:  # Down
                    is_adjacent_to_red = True
                if j > 0 and input_grid[i, j - 1] == 2:  # Left
                    is_adjacent_to_red = True
                if j < cols - 1 and input_grid[i, j + 1] == 2:  # Right
                    is_adjacent_to_red = True

                # If adjacent to a red pixel, replace with red (2) in the output grid.
                if is_adjacent_to_red:
                    output_grid[i, j] = 2

    return output_grid