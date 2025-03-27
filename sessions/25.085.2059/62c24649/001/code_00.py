"""
Transforms an input grid by creating a larger output grid (2x height, 2x width)
and tiling it with four versions of the input grid: the original, a horizontal
reflection, a vertical reflection, and a reflection across both axes.

1.  Determine the dimensions (height H and width W) of the input grid.
2.  Create an output grid with dimensions 2*H by 2*W.
3.  Copy the original input grid into the top-left quadrant (rows 0 to H-1, columns 0 to W-1).
4.  Generate a horizontally reflected version of the input grid and copy it into the top-right quadrant (rows 0 to H-1, columns W to 2*W-1).
5.  Generate a vertically reflected version of the input grid and copy it into the bottom-left quadrant (rows H to 2*H-1, columns 0 to W-1).
6.  Generate a version reflected both horizontally and vertically and copy it into the bottom-right quadrant (rows H to 2*H-1, columns W to 2*W-1).
7.  Return the completed output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Creates a 2x2 tiled output grid from the input grid and its reflections.
    """
    # Convert input to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Get input dimensions
    input_height, input_width = input_np.shape

    # Calculate output dimensions
    output_height = input_height * 2
    output_width = input_width * 2

    # Initialize the output grid with zeros (or any default value)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Generate reflected versions
    horizontal_reflection = input_np[:, ::-1]  # Flip columns left-to-right
    vertical_reflection = input_np[::-1, :]    # Flip rows top-to-bottom
    both_reflection = input_np[::-1, ::-1]      # Flip both

    # Place the original input grid in the top-left quadrant
    output_grid[0:input_height, 0:input_width] = input_np

    # Place the horizontally reflected grid in the top-right quadrant
    output_grid[0:input_height, input_width:output_width] = horizontal_reflection

    # Place the vertically reflected grid in the bottom-left quadrant
    output_grid[input_height:output_height, 0:input_width] = vertical_reflection

    # Place the doubly reflected grid in the bottom-right quadrant
    output_grid[input_height:output_height, input_width:output_width] = both_reflection

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()