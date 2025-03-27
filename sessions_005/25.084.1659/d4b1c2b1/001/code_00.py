"""
Transforms an input grid based on the number of unique colors present.

1.  Identify the unique color values in the input grid.
2.  Count the number of unique colors, let this be N.
3.  If N is 1, the output grid is identical to the input grid.
4.  If N is greater than 1, create an output grid by scaling up the input grid.
    Each pixel (r, c) in the input grid with color C is expanded into an N x N block
    of color C in the output grid. The resulting output grid dimensions will be
    (input_height * N) x (input_width * N).
"""

import numpy as np

def transform(input_grid):
    """
    Scales the input grid based on the number of unique colors it contains.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array if it isn't already
    input_grid_np = np.array(input_grid)

    # 1. Identify and count unique colors
    unique_colors = np.unique(input_grid_np)
    scaling_factor = len(unique_colors)

    # 3. If N is 1, return the original grid
    if scaling_factor == 1:
        return input_grid_np

    # 4. If N > 1, scale up the grid
    input_height, input_width = input_grid_np.shape
    output_height = input_height * scaling_factor
    output_width = input_width * scaling_factor

    # Initialize the output grid (e.g., with zeros, will be overwritten)
    output_grid = np.zeros((output_height, output_width), dtype=input_grid_np.dtype)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            color = input_grid_np[r, c]

            # Calculate the top-left corner of the corresponding block in the output grid
            start_row = r * scaling_factor
            start_col = c * scaling_factor

            # Calculate the bottom-right corner (exclusive) of the block
            end_row = start_row + scaling_factor
            end_col = start_col + scaling_factor

            # Fill the N x N block in the output grid with the color
            output_grid[start_row:end_row, start_col:end_col] = color

    return output_grid