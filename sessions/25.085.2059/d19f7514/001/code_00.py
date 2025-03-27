"""
Transforms an input grid based on combining its top and bottom halves.

The input grid's height is twice the output grid's height. The width is the same.
The input grid is conceptually split into a top half (Top_Grid) and a bottom half (Bottom_Grid), each having the same dimensions as the output grid.

The transformation rule operates pixel-wise:
For each coordinate (row, col):
- If the pixel at (row, col) in the Top_Grid is green (3) OR the pixel at (row, col) in the Bottom_Grid is gray (5), then the corresponding pixel in the output grid at (row, col) is set to yellow (4).
- Otherwise, the output pixel at (row, col) is set to white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)

    # Get dimensions
    input_height, input_width = input_array.shape

    # Calculate the height of the output grid (which is half the input height)
    output_height = input_height // 2
    output_width = input_width

    # Split the input grid into top and bottom halves
    top_grid = input_array[:output_height, :]
    bottom_grid = input_array[output_height:, :]

    # Initialize the output grid with white (0) pixels
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel position in the output grid dimensions
    for r in range(output_height):
        for c in range(output_width):
            # Get the corresponding colors from the top and bottom input grids
            top_color = top_grid[r, c]
            bottom_color = bottom_grid[r, c]

            # Apply the transformation logic
            if top_color == 3 or bottom_color == 5:
                # If top is green (3) OR bottom is gray (5), set output to yellow (4)
                output_grid[r, c] = 4
            else:
                # Otherwise, the output remains white (0) (already initialized)
                pass # output_grid[r, c] = 0 is default

    return output_grid.tolist() # Return as list of lists as per ARC standard