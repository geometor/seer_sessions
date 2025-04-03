"""
Transforms a 1xN grid by identifying patterns [0, C, 0] where C is a non-zero color (1-9).
Each identified [0, C, 0] pattern in the input is replaced by [C, C, C] in the output grid at the same indices.
All other pixels retain their original values from the input.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 1xN NumPy array representing the input sequence.

    Returns:
        A 1xN NumPy array representing the transformed sequence.
    """
    # Ensure input is a 2D numpy array (specifically 1xN)
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Handle unexpected shapes if necessary, but assume 1xN for this task
        raise ValueError("Input grid must have shape 1xN")

    # Get the width of the grid
    width = input_grid.shape[1]

    # Initialize output_grid as a copy of the input_grid
    # This handles the default case where pixels are unchanged
    output_grid = np.copy(input_grid)

    # Iterate through the potential centers of the pattern [0, C, 0]
    # We need to check i-1 and i+1, so the loop runs from index 1 to width-2
    for i in range(1, width - 1):
        # Get the colors of the pixel at i and its neighbors
        color_center = input_grid[0, i]
        color_left = input_grid[0, i - 1]
        color_right = input_grid[0, i + 1]

        # Check if the pattern [0, C, 0] exists, where C is non-zero
        if color_center > 0 and color_left == 0 and color_right == 0:
            # If the pattern is found, update the output grid
            # Replace [0, C, 0] with [C, C, C]
            output_grid[0, i - 1] = color_center
            output_grid[0, i] = color_center
            output_grid[0, i + 1] = color_center
            # Note: We don't need to skip indices here because we are modifying
            # the output grid based on the input grid. The next iteration will
            # correctly check the next potential center position in the input.

    # Return the modified output grid
    return output_grid