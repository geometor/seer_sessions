"""
Transforms a 2D input grid (expected to be 1xN) by identifying isolated foreground pixels horizontally and expanding them. 
Specifically, it finds horizontal sequences of [background, foreground, background] (where background is 0 and foreground is the unique non-zero color C) in the input grid and replaces them with [foreground, foreground, foreground] ([C, C, C]) in the output grid.
Pixels not part of such an identified pattern retain their original color.
The grid dimensions remain unchanged.
"""

import numpy as np

def find_foreground_color(grid_array):
    """
    Finds the single non-white (non-zero) color in the grid array.
    Assumes there is exactly one such color besides white (0).
    Returns None if only white (0) is present or multiple non-zero colors exist.
    """
    unique_colors = np.unique(grid_array)
    foreground_colors = [color for color in unique_colors if color != 0]
    if len(foreground_colors) == 1:
        return foreground_colors[0]
    else:
        # Handle cases with no foreground or multiple foreground colors if necessary
        # Based on examples, we expect exactly one.
        return None

def transform(input_grid):
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid (list of lists): The 2D input grid.

    Returns:
        list of lists: The transformed 2D grid.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    input_array = np.array(input_grid, dtype=int)

    # Check if the input is empty or invalid
    if input_array.size == 0:
        return input_grid # Return original empty list

    # Initialize output_grid as a copy of the input array. Modifications will be made to this copy.
    output_array = input_array.copy()

    # Get the dimensions (rows, columns) of the grid
    rows, cols = input_array.shape

    # Identify the single foreground color (non-zero)
    foreground_color = find_foreground_color(input_array)

    # If no single foreground color exists, or grid is too narrow, return the original grid copy
    if foreground_color is None or cols < 3:
        return output_array.tolist()

    # Iterate through each row of the input array
    for r in range(rows):
        # Iterate through the columns, checking for the horizontal '[0, C, 0]' pattern
        # The loop range ensures we can safely access indices c-1 and c+1.
        for c in range(1, cols - 1):
            # Check if the pattern [0, foreground_color, 0] exists at [r, c-1], [r, c], [r, c+1]
            # Crucially, check the pattern in the *original* input_array
            if (input_array[r, c - 1] == 0 and
                input_array[r, c] == foreground_color and
                input_array[r, c + 1] == 0):

                # If the pattern is found, modify the corresponding pixels in the *output* array
                # Set [r, c-1], [r, c], [r, c+1] to the foreground color
                output_array[r, c - 1] = foreground_color
                output_array[r, c] = foreground_color
                output_array[r, c + 1] = foreground_color

    # Convert the modified NumPy array back to a list of lists before returning
    return output_array.tolist()