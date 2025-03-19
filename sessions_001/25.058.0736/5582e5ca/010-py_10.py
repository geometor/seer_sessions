"""
The transformation rule is to replace all pixels in the input grid with a specific color, determined by the initial color of the input grid:
- If the input grid consists entirely of blue (1) pixels, the output is all maroon (9).
- If the input grid consists entirely of gray (5) pixels, the output is all black (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    - If all input pixels are blue (1), output is all maroon (9).
    - If all input pixels are gray (5), output is all black (0).

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize the output grid with the same shape as the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Check if all pixels are blue (1)
    if np.all(input_grid == 1):
        output_color = 9
    # Check if all pixels are gray (5)
    elif np.all(input_grid == 5):
        output_color = 0
    # Default case (though based on only 2 examples, we don't have a default)
    else:
        output_color = 0  # Placeholder, requires further examples to refine

    # Replace all pixel values in output with the determined output color
    for i in range(rows):
       for j in range(cols):
          output_grid[i,j] = output_color

    return output_grid